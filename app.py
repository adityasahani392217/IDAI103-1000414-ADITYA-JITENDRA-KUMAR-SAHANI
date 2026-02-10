import streamlit as st
import google.generativeai as genai

# =====================================================
# PAGE CONFIGURATION
# =====================================================
st.set_page_config(
    page_title="🌱 AgroNova – Smart Farming Assistant",
    page_icon="🌾",
    layout="wide"
)

# =====================================================
# GEMINI CONFIGURATION (STABLE)
# =====================================================
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("⚠️ GOOGLE_API_KEY missing in Streamlit Secrets")
    st.stop()

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

model = genai.GenerativeModel(
    "models/gemini-pro",
    generation_config={
        "temperature": 0.2,
        "max_output_tokens": 800
    }
)

# =====================================================
# SESSION STATE FOR MULTI-STEP UX
# =====================================================
if "step" not in st.session_state:
    st.session_state.step = 1

def next_step():
    st.session_state.step += 1

def prev_step():
    st.session_state.step -= 1

# =====================================================
# HEADER
# =====================================================
st.markdown("""
## 🌱 AgroNova – Smart Farming Assistant  
**AI-powered, global, region-aware advisory for farmers**
""")

# =====================================================
# STEP 1 – LANGUAGE
# =====================================================
if st.session_state.step == 1:
    st.subheader("🌐 Select Language / भाषा चुनें")

    st.session_state.language = st.radio(
        "Choose your preferred language:",
        ["English", "Hindi"],
        horizontal=True
    )

    st.button("Next ➜", on_click=next_step)

# =====================================================
# STEP 2 – LOCATION & CROP
# =====================================================
elif st.session_state.step == 2:
    st.subheader("📍 Location & Crop Details")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.session_state.country = st.selectbox(
            "Country",
            ["India", "Canada", "Ghana"]
        )

    with col2:
        st.session_state.region = st.text_input(
            "State / Province / Region",
            placeholder="e.g., Uttar Pradesh"
        )

    with col3:
        st.session_state.crop = st.text_input(
            "Crop",
            placeholder="e.g., Wheat"
        )

    colA, colB = st.columns(2)
    colA.button("⬅ Back", on_click=prev_step)
    colB.button("Next ➜", on_click=next_step)

# =====================================================
# STEP 3 – FARM DETAILS
# =====================================================
elif st.session_state.step == 3:
    st.subheader("🌾 Crop Stage & Preferences")

    st.session_state.stage = st.selectbox(
        "Crop Stage",
        ["Land Preparation", "Sowing", "Growth Stage", "Flowering", "Harvest"]
    )

    st.session_state.severity = st.radio(
        "Problem Severity",
        ["Low", "Medium", "High"],
        horizontal=True
    )

    prefs = st.multiselect(
        "Farming Preferences",
        ["Low cost", "Organic", "Minimal chemicals", "Quick results"]
    )
    st.session_state.preferences = ", ".join(prefs)

    colA, colB = st.columns(2)
    colA.button("⬅ Back", on_click=prev_step)
    colB.button("Next ➜", on_click=next_step)

# =====================================================
# STEP 4 – FARMER QUESTION
# =====================================================
elif st.session_state.step == 4:
    st.subheader("❓ Ask Your Farming Question")

    st.session_state.query = st.text_area(
        "Type your question here:",
        placeholder="e.g., What should I do if pest attack occurs during growth stage?"
    )

    colA, colB = st.columns(2)
    colA.button("⬅ Back", on_click=prev_step)
    colB.button("Get AI Advice ➜", on_click=next_step)

# =====================================================
# STEP 5 – AI OUTPUT + VALIDATION
# =====================================================
elif st.session_state.step == 5:
    st.subheader("✅ AI-Generated Farming Advice")

    # ---------------- PROMPT ENGINEERING ----------------
    if st.session_state.language == "Hindi":
        prompt = f"""
आप एक अनुभवी कृषि विशेषज्ञ हैं।

किसान की जानकारी:
देश: {st.session_state.country}
राज्य/क्षेत्र: {st.session_state.region}
फसल: {st.session_state.crop}
फसल अवस्था: {st.session_state.stage}
समस्या की गंभीरता: {st.session_state.severity}
किसान की प्राथमिकताएँ: {st.session_state.preferences}

निर्देश:
- उत्तर अधूरा न हो
- केवल अभिवादन पर समाप्त न करें
- बिंदुओं में उत्तर दें
- हर सुझाव के साथ कारण दें
- सरल भाषा का प्रयोग करें
- रासायनिक दवाओं की मात्रा न बताएं

उत्तर का प्रारूप:
1. समस्या की समझ  
2. तुरंत क्या करें (कारण सहित)  
3. आगे से बचाव  
4. कम लागत उपाय  
5. कब विशेषज्ञ से संपर्क करें  

किसान का प्रश्न:
{st.session_state.query}

उत्तर केवल हिंदी में दें।
"""
    else:
        prompt = f"""
You are an experienced agricultural expert.

Farmer Context:
Country: {st.session_state.country}
Region: {st.session_state.region}
Crop: {st.session_state.crop}
Crop Stage: {st.session_state.stage}
Problem Severity: {st.session_state.severity}
Preferences: {st.session_state.preferences}

Instructions:
- Do NOT stop at greetings
- Provide complete advice
- Use bullet points
- Explain the reason for each suggestion
- Avoid chemical dosage values
- Keep language simple and practical

Response Structure:
1. Problem Understanding  
2. Immediate Actions (with reasons)  
3. Preventive Measures  
4. Low-cost Options  
5. When to Consult an Expert  

Farmer Question:
{st.session_state.query}
"""

    # ---------------- GENERATION ----------------
    try:
        with st.spinner("🌾 Analyzing best practices..."):
            response = model.generate_content(prompt)
            st.markdown(response.text)
    except Exception as e:
        st.error("⚠️ AI service temporarily unavailable.")
        st.exception(e)

    # ---------------- VALIDATION CHECKLIST ----------------
    st.markdown("### 🧪 AI Output Validation Checklist")

    col1, col2 = st.columns(2)
    with col1:
        st.checkbox("Region-specific advice")
        st.checkbox("Actionable steps")
        st.checkbox("Simple language")

    with col2:
        st.checkbox("Clear reasoning")
        st.checkbox("No unsafe recommendations")
        st.checkbox("Avoids over-generalization")

    st.caption(
        "This checklist is used to validate and improve prompt quality and model reliability."
    )

    st.button("🔄 Start New Query", on_click=lambda: st.session_state.update(step=1))
