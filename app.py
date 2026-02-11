import streamlit as st
from google import genai
from datetime import datetime

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="AgroNova – Smart Farming Assistant",
    page_icon="🌱",
    layout="centered"
)

# =====================================================
# CUSTOM UI STYLING (Professional Dark Green Theme)
# =====================================================
st.markdown("""
<style>

/* -------- GLOBAL BACKGROUND -------- */
.stApp {
    background: linear-gradient(135deg, #062e16 0%, #0b3a1d 50%, #041e0f 100%);
    color: #e8f5ec;
}

/* Container width */
.block-container {
    max-width: 820px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* -------- HEADER -------- */
.main-header {
    background: rgba(15, 55, 28, 0.85);
    padding: 1.6rem 2rem;
    border-radius: 14px;
    border: 1px solid rgba(255,255,255,0.06);
    margin-bottom: 2rem;
}

.main-header h1 {
    font-size: 1.9rem;
    font-weight: 700;
    margin-bottom: 0.3rem;
}

.main-header p {
    font-size: 0.9rem;
    opacity: 0.75;
}

/* -------- STEP CARD -------- */
.step-card {
    background: rgba(18, 60, 30, 0.85);
    padding: 1.6rem;
    border-radius: 14px;
    border: 1px solid rgba(255,255,255,0.05);
    margin-bottom: 1.5rem;
}

/* -------- INPUTS -------- */
label {
    font-weight: 600 !important;
    color: #e8f5ec !important;
}

.stSelectbox > div,
.stTextInput > div,
.stTextArea > div,
.stMultiSelect > div {
    background-color: #0f3d1f !important;
    border-radius: 8px !important;
    border: 1px solid #1d5b2c !important;
}

/* -------- BUTTON -------- */
.stButton>button {
    background: linear-gradient(90deg, #22c55e, #16a34a);
    color: white;
    font-weight: 600;
    border-radius: 8px;
    padding: 0.6rem 1.2rem;
    border: none;
    transition: 0.2s ease-in-out;
}

.stButton>button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 18px rgba(34,197,94,0.4);
}

/* -------- ADVICE CARD -------- */
.advice-card {
    background: #0f3d1f;
    padding: 1.8rem;
    border-radius: 14px;
    border-left: 4px solid #22c55e;
    margin-top: 1.5rem;
    line-height: 1.6;
}

/* -------- FOOTER -------- */
.footer {
    text-align: center;
    margin-top: 3rem;
    opacity: 0.6;
    font-size: 0.8rem;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# API CONFIGURATION
# =====================================================
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("🔐 GOOGLE_API_KEY missing in Streamlit Secrets")
    st.stop()

client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])

# =====================================================
# SESSION STATE
# =====================================================
if "step" not in st.session_state:
    st.session_state.step = 1

# =====================================================
# HEADER
# =====================================================
st.markdown("""
<div class="main-header">
<h1>🌱 AgroNova – Smart Farming Assistant</h1>
<p>AI-powered, region-aware advisory for farmers worldwide</p>
</div>
""", unsafe_allow_html=True)

# Progress indicator
st.progress(st.session_state.step / 5)

# =====================================================
# STEP 1 – LANGUAGE
# =====================================================
if st.session_state.step == 1:

    st.markdown('<div class="step-card">', unsafe_allow_html=True)

    st.markdown("### 🌍 Step 1 — Language Preference")
    st.caption("Choose how the assistant should communicate.")

    language = st.radio("Language", ["English", "Hindi"])
    voice = st.toggle("Enable Voice Guidance")

    if st.button("Continue"):
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

    st.markdown("### 📍 Step 2 — Farm Location")
    st.caption("Location helps generate region-specific advice.")

    country = st.selectbox("Country",
        ["India", "USA", "Canada", "Brazil", "Australia", "Ghana"])

    state = st.text_input("State / Province")
    crop = st.selectbox("Crop",
        ["Wheat", "Rice", "Maize", "Cotton", "Vegetables", "Other"])

    if st.button("Continue"):
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

    st.markdown("### 🌾 Step 3 — Crop Condition")
    st.caption("Tell us about your crop situation.")

    stage = st.selectbox("Crop Stage",
        ["Sowing", "Growing", "Flowering", "Harvesting"])

    severity = st.radio("Problem Severity",
        ["Low", "Medium", "High"])

    preferences = st.multiselect("Farming Preferences",
        ["Organic", "Low Cost", "Quick Results", "Minimal Labor"])

    if st.button("Continue"):
        st.session_state.stage = stage
        st.session_state.severity = severity
        st.session_state.preferences = preferences
        st.session_state.step = 4
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# =====================================================
# STEP 4 – QUESTION
# =====================================================
elif st.session_state.step == 4:

    st.markdown('<div class="step-card">', unsafe_allow_html=True)

    st.markdown("### 💬 Step 4 — Describe the Problem")
    st.caption("Be specific for better advice.")

    question = st.text_area("Your Question")

    if st.button("Generate Advice"):
        st.session_state.question = question
        st.session_state.step = 5
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# =====================================================
# STEP 5 – AI RESPONSE
# =====================================================
elif st.session_state.step == 5:

    st.markdown("### 🌾 AI-Generated Farming Advice")

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
- Provide bullet-point advice.
- Each point must explain WHY.
- Keep language simple and practical.
- Make advice region-specific.
"""

        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt,
            config={
                "temperature": 0.4,
                "max_output_tokens": 1500
            }
        )

        st.markdown(f"""
        <div class="advice-card">
        {response.text}
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
AgroNova • Gemini Powered • {datetime.now().year}
</div>
""", unsafe_allow_html=True)
