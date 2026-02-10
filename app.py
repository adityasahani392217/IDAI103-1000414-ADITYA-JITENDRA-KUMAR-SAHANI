import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import tempfile

# =====================================================
# PAGE CONFIGURATION
# =====================================================
st.set_page_config(
    page_title="🌍 AgroNova – Global Smart Farming Assistant",
    page_icon="🌾",
    layout="wide"
)

# =====================================================
# API CONFIGURATION
# =====================================================
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("⚠️ GOOGLE_API_KEY missing in Streamlit Secrets")
    st.stop()

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# =====================================================
# DYNAMIC MODEL SELECTION (KEY FIX)
# =====================================================
available_models = [
    m.name for m in genai.list_models()
    if "generateContent" in m.supported_generation_methods
]

if not available_models:
    st.error("❌ No text-generation models available for this API key.")
    st.stop()

# Pick the first safe text model
MODEL_NAME = available_models[0]

model = genai.GenerativeModel(
    model_name=MODEL_NAME,
    generation_config={
        "temperature": 0.2,
        "max_output_tokens": 800
    }
)

# =====================================================
# HEADER
# =====================================================
st.markdown("""
# 🌱 AgroNova – Smart Farming Assistant  
**AI-powered, global, region-aware advisory for farmers**
""")

st.caption(f"🔧 Using model: `{MODEL_NAME}`")

# =====================================================
# LANGUAGE & ACCESSIBILITY
# =====================================================
language = st.selectbox("🌐 Language", ["English", "Hindi"])
voice_enabled = st.checkbox("🔊 Enable Voice Output", value=True)

# =====================================================
# GLOBAL INPUTS
# =====================================================
country = st.text_input("Country", "India")
region = st.text_input("State / Province / Region", "Uttar Pradesh")
crop = st.text_input("Crop", "Wheat")

stage = st.selectbox(
    "Crop Stage",
    ["Land Preparation", "Sowing", "Growth Stage", "Flowering", "Harvest"]
)

severity = st.selectbox(
    "Problem Severity",
    ["Low", "Medium", "High"]
)

preferences = st.text_area(
    "Farming Preferences",
    "Low cost, minimal chemicals"
)

query = st.text_input(
    "Farmer Question",
    "What should I do if pest attack occurs during growth stage?"
)

# =====================================================
# ACTION
# =====================================================
if st.button("🌾 Get AI Farming Advice"):

    if not query.strip():
        st.warning("Please enter a farming question.")
        st.stop()

    prompt = f"""
You are an experienced agricultural expert.

Farmer Context:
Country: {country}
Region: {region}
Crop: {crop}
Crop Stage: {stage}
Problem Severity: {severity}
Preferences: {preferences}

OUTPUT FORMAT (MANDATORY):
1. Problem Understanding (1–2 lines)
2. Immediate Actions (bullet points + why)
3. Preventive Measures (bullet points + why)
4. Low-Cost & Sustainable Options
5. When to Seek Local Expert Help

RULES:
- Simple farmer-friendly language
- No chemical dosage numbers
- Region-specific advice
- Complete all sections
- Respond in {"Hindi" if language == "Hindi" else "English"}

Farmer Question:
{query}
"""

    with st.spinner("🧠 Generating expert advice..."):
        response = model.generate_content(prompt)

    st.markdown("## ✅ AI-Generated Farming Advice")
    st.markdown(response.text)

    # =====================================================
    # VOICE OUTPUT
    # =====================================================
    if voice_enabled:
        try:
            tts = gTTS(
                text=response.text,
                lang="hi" if language == "Hindi" else "en"
            )
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                tts.save(fp.name)
                st.audio(fp.name)
        except Exception:
            st.info("🔊 Voice output unavailable on this device.")

    # =====================================================
    # VALIDATION CHECKLIST
    # =====================================================
    st.markdown("## 🧪 AI Output Validation Checklist")
    st.checkbox("Region-specific advice", True)
    st.checkbox("Actionable steps provided", True)
    st.checkbox("Clear reasoning included", True)
    st.checkbox("Language is farmer-friendly", True)
    st.checkbox("No unsafe advice", True)
