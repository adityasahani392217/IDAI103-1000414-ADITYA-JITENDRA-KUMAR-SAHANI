import streamlit as st
import google.generativeai as genai
import pandas as pd

# =====================================================
# PAGE CONFIGURATION
# =====================================================
st.set_page_config(
    page_title="AgroNova | Smart Farming Assistant",
    page_icon="🌾",
    layout="wide"
)

# =====================================================
# SECURE GEMINI CONFIGURATION
# =====================================================
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("⚠️ GOOGLE_API_KEY missing in Streamlit Secrets")
    st.stop()

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

model = genai.GenerativeModel(
    model_name="gemini-3-flash-preview",
    generation_config={
        "temperature": 0.2,        # Low hallucination risk
        "max_output_tokens": 300
    }
)

# =====================================================
# HEADER
# =====================================================
st.markdown("""
## 🌱 AgroNova – Smart Farming Assistant  
**AI-powered, region-aware advisory for farmers in India, Canada, and Ghana**
""")

# =====================================================
# USER INPUTS (FA-2 STEP 4)
# =====================================================
col1, col2, col3 = st.columns(3)

with col1:
    country = st.selectbox("Country", ["India", "Canada", "Ghana"])

with col2:
    location = st.text_input("Region / Province / State", placeholder="e.g., Uttar Pradesh")

with col3:
    crop = st.text_input("Crop", placeholder="e.g., Wheat")

stage = st.selectbox(
    "Crop Stage",
    ["Land Preparation", "Sowing", "Growth Stage", "Flowering", "Harvest"]
)

preferences = st.text_area(
    "Farming Preferences",
    placeholder="e.g., low-cost, organic methods preferred"
)

query = st.text_input(
    "Farmer Question",
    placeholder="e.g., What should I do if pest attack occurs at growth stage?"
)

# =====================================================
# BUTTON ACTION
# =====================================================
if st.button("🌾 Get AI Farming Advice"):

    if not query.strip():
        st.warning("Please enter a farming question.")
        st.stop()

    # =====================================================
    # PROMPT ENGINEERING (FA-1 + FA-2)
    # =====================================================
    prompt = f"""
You are an agricultural expert assisting farmers globally.

Context:
Country: {country}
Region: {location}
Crop: {crop}
Crop Stage: {stage}
Preferences: {preferences}

Task:
Provide clear, actionable farming advice.

Output Rules:
- Use bullet points
- Each suggestion must include a short justification ("why")
- Avoid chemical dosages
- Keep language simple and farmer-friendly
- Ensure advice is region-specific

Farmer Question:
{query}
"""

    with st.spinner("Analyzing best practices..."):
        response = model.generate_content(prompt)

    # =====================================================
    # OUTPUT FORMATTING (FA-2 STEP 4)
    # =====================================================
    st.markdown("### ✅ AI-Generated Farming Advice")
    st.markdown(response.text)

    # =====================================================
    # FEEDBACK CHECKLIST (FA-2 STEP 5)
    # =====================================================
    st.markdown("### 🧪 AI Output Validation Checklist")

    colA, colB = st.columns(2)
    with colA:
        st.checkbox("Region-specific advice", value=True)
        st.checkbox("Actionable steps provided", value=True)
        st.checkbox("Language is simple", value=True)

    with colB:
        st.checkbox("Clear reasoning provided", value=True)
        st.checkbox("No unsafe recommendations", value=True)
        st.checkbox("Avoids over-generalization", value=True)

    st.caption(
        "This checklist is used during testing to validate and improve prompt quality and model reliability."
    )
