import streamlit as st
from google import genai
from datetime import datetime
import pandas as pd

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Smart Farming Assistant",
    page_icon="🌱",
    layout="wide"
)

# ---------------- CLEAN MODERN UI STYLE ----------------
st.markdown("""
<style>

/* Background */
.stApp {
    background: linear-gradient(to bottom right, #eef7f0, #dff1e3);
    color: #102216;
}

/* Force all text to be dark */
html, body, [class*="css"]  {
    color: #102216 !important;
}

/* Header */
.main-header {
    background: linear-gradient(90deg, #0f3d1f, #145c2c);
    color: #ffffff;
    padding: 2rem;
    border-radius: 20px;
    text-align: center;
    margin-bottom: 2rem;
}

/* Step cards */
.step-card {
    background: #ffffff;
    padding: 2rem;
    border-radius: 20px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.08);
    margin-bottom: 1.5rem;
    color: #102216;
}

/* Advice card */
.advice-card {
    background: #ffffff;
    padding: 2rem;
    border-radius: 20px;
    box-shadow: 0 12px 30px rgba(0,0,0,0.08);
    border-left: 6px solid #22c55e;
    margin-top: 1.5rem;
    color: #102216;
}

/* Labels & inputs */
label, .stSelectbox label, .stRadio label, .stTextInput label, .stTextArea label {
    color: #102216 !important;
    font-weight: 600;
}

/* Buttons */
.stButton>button {
    background-color: #22c55e;
    color: #102216;
    font-weight: 700;
    border-radius: 12px;
    padding: 0.8rem 1.5rem;
    border: none;
}

.stButton>button:hover {
    background-color: #16a34a;
    color: white;
}

/* Radio button text */
div[role="radiogroup"] label {
    color: #102216 !important;
}

/* Footer */
.footer {
    background: linear-gradient(90deg, #0f3d1f, #145c2c);
    color: #ffffff;
    padding: 1.5rem;
    border-radius: 20px;
    text-align: center;
    margin-top: 2rem;
}

</style>
""", unsafe_allow_html=True)
# ---------------- API ----------------
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("🔐 GOOGLE_API_KEY missing in Streamlit Secrets")
    st.stop()

client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])

# ---------------- SESSION STATE ----------------
if "step" not in st.session_state:
    st.session_state.step = 1
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ---------------- HEADER ----------------
st.markdown("""
<div class="main-header">
<h1>🌱 Smart Farming Assistant</h1>
<p>AI-powered, region-aware advisory for farmers worldwide</p>
</div>
""", unsafe_allow_html=True)

# =====================================================
# STEP 1 – LANGUAGE
# =====================================================
if st.session_state.step == 1:
    st.markdown('<div class="step-card">', unsafe_allow_html=True)
    st.subheader("Step 1: Select Language")

    language = st.radio("Choose Language", ["English", "Hindi"])

    voice = st.toggle("Enable Voice Guidance")

    if st.button("Next →"):
        st.session_state.language = language
        st.session_state.voice = voice
        st.session_state.step = 2
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# =====================================================
# STEP 2 – LOCATION
# =====================================================
elif st.session_state.step == 2:
    st.markdown('<div class="step-card">', unsafe_allow_html=True)
    st.subheader("Step 2: Location & Crop")

    country = st.selectbox("Country",
                           ["India", "Canada", "Ghana", "USA", "Brazil", "Australia"])

    state = st.text_input("State / Province")

    crop = st.selectbox("Crop",
                        ["Wheat", "Rice", "Maize", "Cotton", "Vegetables", "Other"])

    if st.button("Next →"):
        st.session_state.country = country
        st.session_state.state = state
        st.session_state.crop = crop
        st.session_state.step = 3
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# =====================================================
# STEP 3 – CROP DETAILS
# =====================================================
elif st.session_state.step == 3:
    st.markdown('<div class="step-card">', unsafe_allow_html=True)
    st.subheader("Step 3: Crop Details")

    stage = st.selectbox("Crop Stage",
                         ["Sowing", "Growing", "Flowering", "Harvesting"])

    severity = st.radio("Problem Severity",
                        ["Low", "Medium", "High"])

    preferences = st.multiselect("Farming Preferences",
                                  ["Organic", "Low Cost", "Quick Results", "Minimal Labor"])

    if st.button("Next →"):
        st.session_state.stage = stage
        st.session_state.severity = severity
        st.session_state.preferences = preferences
        st.session_state.step = 4
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# =====================================================
# STEP 4 – ASK QUESTION
# =====================================================
elif st.session_state.step == 4:
    st.markdown('<div class="step-card">', unsafe_allow_html=True)
    st.subheader("Step 4: Ask Your Question")

    question = st.text_area("Describe your farming problem")

    if st.button("Get AI Advice"):
        st.session_state.question = question
        st.session_state.step = 5
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# =====================================================
# STEP 5 – AI RESPONSE
# =====================================================
elif st.session_state.step == 5:

    st.subheader("🌾 AI-Generated Farming Advice")

    try:
        prompt = f"""
You are an expert agricultural advisor.

Farmer Context:
Country: {st.session_state.country}
State: {st.session_state.state}
Crop: {st.session_state.crop}
Crop Stage: {st.session_state.stage}
Severity: {st.session_state.severity}
Preferences: {', '.join(st.session_state.preferences)}

Question:
{st.session_state.question}

Instructions:
- Provide clear bullet-point advice.
- Each recommendation must include WHY.
- Keep language simple.
- Make it region-specific.
"""

        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt,
            config={
                "temperature": 0.4,
                "max_output_tokens": 2000
            }
        )

        output_text = response.text

        st.markdown(f"""
        <div class="advice-card">
        {output_text}
        </div>
        """, unsafe_allow_html=True)

    except Exception as e:
        st.error("AI service temporarily unavailable.")
        st.code(str(e))

    if st.button("🔄 Start Over"):
        st.session_state.step = 1
        st.rerun()

# =====================================================
# FOOTER
# =====================================================
st.markdown(f"""
<div class="footer">
Smart Farming Assistant • Gemini Powered • {datetime.now().year}
</div>
""", unsafe_allow_html=True)
