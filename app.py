import streamlit as st
import pandas as pd
from datetime import datetime
from google import genai

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="FarmaBuddy 🌱",
    page_icon="🌾",
    layout="wide"
)

# ---------------- CLEAN UI STYLE ----------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(to bottom right, #f4fff6, #e8f5e9);
}

/* Header */
.header-container {
    background: linear-gradient(135deg, #1b5e20, #2e7d32);
    padding: 2.5rem;
    border-radius: 18px;
    color: white;
    text-align: center;
    margin-bottom: 2rem;
    box-shadow: 0 10px 30px rgba(0,0,0,0.15);
}
.title-text {
    font-size: 3rem;
    font-weight: 800;
}
.subtitle-text {
    font-size: 1.1rem;
    opacity: 0.9;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #43a047, #2e7d32);
    color: white;
    border-radius: 12px;
    font-weight: 600;
    padding: 0.8rem 1.5rem;
    border: none;
}
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 18px rgba(0,0,0,0.2);
}

/* Cards */
.recommendation-card {
    background: white;
    padding: 1.8rem;
    border-radius: 16px;
    margin: 1.2rem 0;
    box-shadow: 0 8px 20px rgba(0,0,0,0.08);
    border-left: 6px solid #43a047;
}
.chat-container {
    background: white;
    border-radius: 16px;
    padding: 1.5rem;
    box-shadow: 0 8px 20px rgba(0,0,0,0.08);
    max-height: 450px;
    overflow-y: auto;
}
.user-message {
    background: #e3f2fd;
    padding: 1rem;
    border-radius: 16px;
    margin: 0.8rem 0;
}
.ai-message {
    background: #e8f5e9;
    padding: 1rem;
    border-radius: 16px;
    margin: 0.8rem 0;
}
.footer {
    background: linear-gradient(135deg, #1b5e20, #2e7d32);
    color: white;
    padding: 2rem;
    border-radius: 18px;
    text-align: center;
    margin-top: 2.5rem;
}
</style>
""", unsafe_allow_html=True)

# ---------------- API SETUP ----------------
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("🔐 GOOGLE_API_KEY missing in Streamlit Secrets")
    st.stop()

api_key = st.secrets["GOOGLE_API_KEY"]
client = genai.Client(api_key=api_key)

# ---------------- HEADER ----------------
st.markdown("""
<div class="header-container">
    <h1 class="title-text">🌱 FarmaBuddy</h1>
    <h4 class="subtitle-text">AI-Powered Smart Farming Assistant</h4>
    <p>Region-aware • Practical Advice • Built with Gemini</p>
</div>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.header("🌍 Farm Configuration")

    region = st.selectbox("Country / Region",
                          ["India", "Ghana", "Canada", "USA", "Australia", "Brazil"])

    location = st.text_input("State / Province")

    crop_stage = st.selectbox("Crop Stage",
                              ["Planning", "Sowing", "Growing", "Harvesting"])

    priorities = st.multiselect("Priorities",
                                ["Low Water Use", "High Yield", "Organic Farming", "Low Cost"])

    temperature = st.slider("AI Creativity", 0.2, 0.8, 0.4)

# ---------------- SESSION STATE ----------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ---------------- TABS ----------------
tab1, tab2 = st.tabs(["🌾 Recommendations", "💬 Chat Assistant"])

# =====================================================
# TAB 1 - RECOMMENDATIONS
# =====================================================
with tab1:

    if st.button("🚀 Generate Smart Recommendations"):

        if not location:
            st.warning("Please enter your location.")
        else:
            try:
                with st.spinner("Analyzing farm data..."):

                    prompt = f"""
You are a professional agricultural advisor.

Farmer Context:
Country: {region}
Location: {location}
Crop Stage: {crop_stage}
Priorities: {', '.join(priorities) if priorities else 'General'}

Provide EXACTLY 3 detailed recommendations.

Format:
Recommendation 1:
• Action:
• Why:

Recommendation 2:
• Action:
• Why:

Recommendation 3:
• Action:
• Why:

Keep advice:
- Practical
- Region-specific
- Safe
- Easy to understand
"""

                    response = client.models.generate_content(
                        model="gemini-1.5-flash",
                        contents=prompt,
                        config={
                            "temperature": temperature,
                            "max_output_tokens": 1500
                        }
                    )

                    output_text = response.text

                    st.success("✅ Recommendations Generated")

                    # Show FULL OUTPUT (no truncation)
                    st.markdown(f"""
                    <div class="recommendation-card">
                        {output_text}
                    </div>
                    """, unsafe_allow_html=True)

            except Exception as e:
                st.error("⚠️ AI service temporarily unavailable")
                st.code(str(e))

# =====================================================
# TAB 2 - CHAT
# =====================================================
with tab2:

    st.markdown('<div class="chat-container">', unsafe_allow_html=True)

    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f'<div class="user-message"><b>You:</b> {msg["content"]}</div>',
                        unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="ai-message"><b>FarmaBuddy:</b> {msg["content"]}</div>',
                        unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    user_input = st.text_input("Ask your farming question:")

    if st.button("Send") and user_input:

        st.session_state.chat_history.append(
            {"role": "user", "content": user_input})

        try:
            chat_prompt = f"""
You are FarmaBuddy, an agricultural assistant.

Farmer Context:
Country: {region}
Location: {location}
Crop Stage: {crop_stage}

User Question:
{user_input}

Provide:
- Clear
- Practical
- Region-specific
- Actionable advice
"""

            response = client.models.generate_content(
                model="gemini-1.5-flash",
                contents=chat_prompt,
                config={
                    "temperature": temperature,
                    "max_output_tokens": 1500
                }
            )

            ai_reply = response.text

        except:
            ai_reply = "⚠️ Unable to connect to AI service."

        st.session_state.chat_history.append(
            {"role": "assistant", "content": ai_reply})

        st.rerun()

# ---------------- FEEDBACK ----------------
st.markdown("---")
st.subheader("✅ Quality Checklist")

c1, c2, c3 = st.columns(3)

with c1:
    f1 = st.checkbox("Region-specific")
    f2 = st.checkbox("Logical reasoning")

with c2:
    f3 = st.checkbox("Simple language")
    f4 = st.checkbox("Actionable steps")

with c3:
    f5 = st.checkbox("Safe advice")

if st.button("Submit Feedback"):
    score = sum([f1, f2, f3, f4, f5])
    st.success(f"Feedback Score: {score}/5 ⭐")

# ---------------- SESSION LOG ----------------
st.markdown("---")
st.subheader("📊 Session Log")

log_df = pd.DataFrame([{
    "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "Region": region,
    "Location": location,
    "Crop Stage": crop_stage,
    "Chat Messages": len(st.session_state.chat_history)
}])

st.dataframe(log_df, use_container_width=True)

# ---------------- FOOTER ----------------
st.markdown(f"""
<div class="footer">
FarmaBuddy AI • FA-2 Project • {datetime.now().strftime("%Y")}  
Built with Gemini 1.5 Flash
</div>
""", unsafe_allow_html=True)
