import streamlit as st
import pandas as pd
from datetime import datetime
from google import genai

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="🌾 AgroNova",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------------------------
# CLEAN PREMIUM GREEN UI
# -------------------------------------------------
st.markdown("""
<style>
* {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #071e14, #0c2f20);
    color: #e8f5ec;
}

.block-container {
    max-width: 1100px;
    padding-top: 2rem;
}

/* Header */
.header-container {
    background: linear-gradient(90deg, #0f3d28, #145c3a);
    padding: 2rem;
    border-radius: 20px;
    margin-bottom: 2rem;
    border: 1px solid rgba(255,255,255,0.08);
}

.header-container h1 {
    font-size: 2.6rem;
    font-weight: 800;
    margin-bottom: 0.3rem;
}

.header-container p {
    opacity: 0.8;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #0d2a1d;
}

/* Cards */
.card {
    background: #0f3d28;
    padding: 1.5rem;
    border-radius: 16px;
    border: 1px solid rgba(255,255,255,0.06);
    margin-bottom: 1.2rem;
}

/* Buttons */
.stButton>button {
    background: linear-gradient(90deg, #22c55e, #16a34a);
    border-radius: 10px;
    border: none;
    font-weight: 600;
    padding: 0.7rem 1.4rem;
    color: white;
}

.stButton>button:hover {
    background: linear-gradient(90deg, #16a34a, #15803d);
}

/* Recommendation Card */
.recommendation {
    background: #0c3323;
    padding: 1.5rem;
    border-radius: 14px;
    border-left: 4px solid #22c55e;
    margin-bottom: 1rem;
    line-height: 1.6;
}

/* Chat */
.user-msg {
    background: #1e3a8a;
    padding: 1rem;
    border-radius: 14px;
    margin-bottom: 0.5rem;
}

.ai-msg {
    background: #0c3323;
    padding: 1rem;
    border-radius: 14px;
    margin-bottom: 0.5rem;
    border-left: 4px solid #22c55e;
}

/* Footer */
.footer {
    text-align: center;
    margin-top: 3rem;
    opacity: 0.7;
    font-size: 0.9rem;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# GEMINI API
# -------------------------------------------------
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("🔐 Add GOOGLE_API_KEY in Streamlit Secrets")
    st.stop()

client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])

MODEL_NAME = "gemini-1.5-flash"   # Stable model

# -------------------------------------------------
# HEADER
# -------------------------------------------------
st.markdown("""
<div class="header-container">
    <h1>🌾 AgroNova</h1>
    <p>AI-Powered Smart Farming Intelligence • Global & Region-Aware</p>
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------
# SIDEBAR SETTINGS
# -------------------------------------------------
with st.sidebar:
    st.header("Farm Configuration")

    country = st.selectbox(
        "Country",
        ["India", "Ghana", "Canada", "USA", "Brazil", "Australia"]
    )

    location = st.text_input("State / Province")

    crop_stage = st.selectbox(
        "Crop Stage",
        ["Planning", "Sowing", "Growing", "Harvesting", "Storage"]
    )

    priorities = st.multiselect(
        "Goals",
        ["High Yield", "Low Cost", "Organic", "Water Saving",
         "Pest Control", "Soil Health"]
    )

    temperature = st.slider(
        "AI Creativity",
        0.2, 0.8, 0.4,
        help="Lower = safer advice | Higher = creative suggestions"
    )

# -------------------------------------------------
# SESSION STATE
# -------------------------------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# -------------------------------------------------
# MAIN TABS
# -------------------------------------------------
tab1, tab2 = st.tabs(["Farm Plan", "Chat Assistant"])

# =================================================
# TAB 1 — FARM PLAN
# =================================================
with tab1:

    st.subheader("Generate Smart Farm Plan")

    if st.button("Generate Recommendations"):

        if not location:
            st.warning("Please enter your state/province.")
        else:
            try:
                with st.spinner("Analyzing farm conditions..."):

                    prompt = f"""
You are an expert agricultural advisor.

Farmer Context:
Country: {country}
State: {location}
Crop Stage: {crop_stage}
Goals: {', '.join(priorities) if priorities else 'General productivity'}

Provide EXACTLY 3 farming recommendations.

Format strictly:

Recommendation 1:
• Action:
• Why:

Recommendation 2:
• Action:
• Why:

Recommendation 3:
• Action:
• Why:

Use simple language.
Be region-specific.
Avoid unsafe chemical instructions.
"""

                    response = client.models.generate_content(
                        model=MODEL_NAME,
                        contents=prompt,
                        config={
                            "temperature": temperature,
                            "max_output_tokens": 900
                        }
                    )

                    if hasattr(response, "text") and response.text:
                        recommendations = response.text.split("\n\n")
                    else:
                        recommendations = ["⚠️ No response received."]

                    st.success("Farm plan ready!")

                    for rec in recommendations[:3]:
                        if rec.strip():
                            st.markdown(f"""
                            <div class="recommendation">
                            {rec}
                            </div>
                            """, unsafe_allow_html=True)

            except Exception:
                st.error("⚠️ AI service temporarily unavailable.")

# =================================================
# TAB 2 — CHAT ASSISTANT
# =================================================
with tab2:

    st.subheader("Ask AgroNova")

    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f'<div class="user-msg"><b>You:</b> {msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="ai-msg"><b>AgroNova:</b> {msg["content"]}</div>', unsafe_allow_html=True)

    user_input = st.text_input("Ask your farming question")

    if st.button("Send") and user_input:

        st.session_state.chat_history.append({"role": "user", "content": user_input})

        try:
            with st.spinner("AgroNova is thinking..."):

                prompt = f"""
You are AgroNova, an agricultural AI assistant.

Farmer Context:
Country: {country}
State: {location}
Crop Stage: {crop_stage}
Goals: {', '.join(priorities) if priorities else 'General'}

Answer clearly and simply.
Avoid unsafe instructions.
Focus on practical advice.

User question:
{user_input}
"""

                response = client.models.generate_content(
                    model=MODEL_NAME,
                    contents=prompt,
                    config={
                        "temperature": temperature,
                        "max_output_tokens": 800
                    }
                )

                if hasattr(response, "text") and response.text:
                    reply = response.text
                else:
                    reply = "I could not generate a response."

                st.session_state.chat_history.append({"role": "assistant", "content": reply})
                st.rerun()

        except Exception:
            st.session_state.chat_history.append(
                {"role": "assistant", "content": "⚠️ AI service busy. Try again."}
            )
            st.rerun()

    if st.session_state.chat_history:
        if st.button("Clear Chat"):
            st.session_state.chat_history = []
            st.rerun()

# -------------------------------------------------
# FOOTER
# -------------------------------------------------
st.markdown(f"""
<div class="footer">
AgroNova • AI Smart Farming Assistant • {datetime.now().year}
</div>
""", unsafe_allow_html=True)
