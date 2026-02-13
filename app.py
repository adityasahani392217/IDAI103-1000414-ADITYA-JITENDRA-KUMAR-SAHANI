import streamlit as st
import pandas as pd
from datetime import datetime
from google import genai

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="🌾 AgroNova Elite",
    page_icon="🌱",
    layout="wide"
)

# =========================================================
# CLEAN PROFESSIONAL UI
# =========================================================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #071e14, #0c2f20);
    color: #e8f5ec;
}
.block-container {
    max-width: 1100px;
}
.header {
    background: linear-gradient(90deg,#0f3d28,#145c3a);
    padding: 2rem;
    border-radius: 18px;
    margin-bottom: 2rem;
}
.card {
    background: #0f3d28;
    padding: 1.5rem;
    border-radius: 14px;
    margin-bottom: 1.2rem;
    border: 1px solid rgba(255,255,255,0.06);
}
.recommendation {
    background: #0c3323;
    padding: 1.3rem;
    border-radius: 12px;
    border-left: 4px solid #22c55e;
    margin-bottom: 1rem;
}
.stButton>button {
    background: linear-gradient(90deg,#22c55e,#16a34a);
    color: white;
    border-radius: 10px;
    border: none;
    font-weight: 600;
}
.footer {
    text-align: center;
    margin-top: 3rem;
    opacity: 0.6;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# API SETUP
# =========================================================
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("🔐 Add GOOGLE_API_KEY to Streamlit Secrets")
    st.stop()

client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
MODEL_NAME = "gemini-1.5-flash"

# =========================================================
# HEADER
# =========================================================
st.markdown("""
<div class="header">
<h1>🌾 AgroNova Elite</h1>
<p>Context-Aware AI Farming Intelligence System</p>
</div>
""", unsafe_allow_html=True)

# =========================================================
# CONTEXT ENGINE
# =========================================================
def build_context(country, location, stage):
    climate_note = ""

    if country == "India":
        climate_note = "Monsoon-driven seasonal agriculture."
    elif country == "Canada":
        climate_note = "Cold climate, short growing cycles."
    elif country == "Ghana":
        climate_note = "Tropical humid agricultural system."
    else:
        climate_note = "Mixed climatic agricultural region."

    risk_flag = "Low"
    if not location:
        risk_flag = "Moderate – Missing region detail"

    return climate_note, risk_flag


# =========================================================
# CONFIDENCE MODEL
# =========================================================
def confidence_score(location, priorities):
    score = 0
    if location: score += 1
    if priorities: score += 1

    if score == 2:
        return "High"
    elif score == 1:
        return "Moderate"
    else:
        return "Low"


# =========================================================
# OUTPUT VALIDATOR
# =========================================================
def validate_output(text):
    issues = []

    if "Recommendation" not in text:
        issues.append("Format deviation")

    if len(text) < 200:
        issues.append("Output too short")

    if "dosage" in text.lower():
        issues.append("Potential unsafe instruction")

    return issues


# =========================================================
# SIDEBAR CONFIG
# =========================================================
with st.sidebar:
    st.header("Farm Configuration")

    country = st.selectbox(
        "Country",
        ["India", "Ghana", "Canada", "USA", "Brazil", "Australia"]
    )

    location = st.text_input("State / Province")

    stage = st.selectbox(
        "Crop Stage",
        ["Planning", "Sowing", "Growing", "Harvesting", "Storage"]
    )

    priorities = st.multiselect(
        "Goals",
        ["High Yield", "Low Cost", "Organic",
         "Water Saving", "Pest Control", "Soil Health"]
    )

    temperature = st.slider("AI Creativity", 0.2, 0.8, 0.4)

# =========================================================
# SESSION STATE
# =========================================================
if "logs" not in st.session_state:
    st.session_state.logs = []

# =========================================================
# MAIN TABS
# =========================================================
tab1, tab2 = st.tabs(["Farm Plan Generator", "Chat Assistant"])

# =========================================================
# TAB 1 — FARM PLAN
# =========================================================
with tab1:

    st.subheader("Generate Intelligent Farm Plan")

    if st.button("Generate Plan"):

        if not location:
            st.warning("Please enter state/province.")
        else:

            climate_note, risk_flag = build_context(country, location, stage)

            prompt = f"""
SYSTEM ROLE:
You are AgroNova Elite, a professional agricultural advisor.

FARM CONTEXT:
Country: {country}
Location: {location}
Climate Insight: {climate_note}
Crop Stage: {stage}
Goals: {', '.join(priorities) if priorities else 'General productivity'}

RULES:
- Provide exactly 3 recommendations
- Each must include Action and Why
- Avoid unsafe chemicals
- Be region specific

FORMAT STRICTLY:

Recommendation 1:
• Action:
• Why:

Recommendation 2:
• Action:
• Why:

Recommendation 3:
• Action:
• Why:
"""

            with st.expander("🔍 View Generated Prompt"):
                st.code(prompt)

            try:
                with st.spinner("Analyzing farm intelligence..."):

                    response = client.models.generate_content(
                        model=MODEL_NAME,
                        contents=prompt,
                        config={
                            "temperature": temperature,
                            "max_output_tokens": 900
                        }
                    )

                    result = response.text if hasattr(response, "text") else "No response."

                    issues = validate_output(result)

                    if issues:
                        st.warning(f"⚠️ AI Output Review: {', '.join(issues)}")

                    st.success("Farm Plan Generated")

                    recommendations = result.split("\n\n")

                    for rec in recommendations[:3]:
                        if rec.strip():
                            st.markdown(f"""
                            <div class="recommendation">
                            {rec}
                            </div>
                            """, unsafe_allow_html=True)

                    # Confidence
                    st.info(f"AI Confidence Level: {confidence_score(location, priorities)}")
                    st.info(f"Risk Flag: {risk_flag}")

                    # Logging
                    st.session_state.logs.append({
                        "Time": datetime.now(),
                        "Country": country,
                        "Stage": stage,
                        "Confidence": confidence_score(location, priorities)
                    })

            except Exception:
                st.error("⚠️ AI service unavailable.")

# =========================================================
# TAB 2 — CHAT ASSISTANT
# =========================================================
with tab2:

    if "chat" not in st.session_state:
        st.session_state.chat = []

    st.subheader("Ask AgroNova Elite")

    for msg in st.session_state.chat:
        role = "You" if msg["role"] == "user" else "AgroNova"
        st.markdown(f"**{role}:** {msg['content']}")

    user_q = st.text_input("Ask your farming question")

    if st.button("Send") and user_q:

        st.session_state.chat.append({"role": "user", "content": user_q})

        climate_note, _ = build_context(country, location, stage)

        chat_prompt = f"""
You are AgroNova Elite.

Context:
Country: {country}
Location: {location}
Climate: {climate_note}
Stage: {stage}

Rules:
- Practical advice
- No unsafe chemicals
- Simple language

User Question:
{user_q}
"""

        try:
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=chat_prompt,
                config={
                    "temperature": temperature,
                    "max_output_tokens": 800
                }
            )

            reply = response.text if hasattr(response, "text") else "No response."
            st.session_state.chat.append({"role": "assistant", "content": reply})
            st.rerun()

        except Exception:
            st.session_state.chat.append(
                {"role": "assistant", "content": "AI service busy. Try again."}
            )
            st.rerun()

# =========================================================
# ANALYTICS PANEL
# =========================================================
if st.session_state.logs:
    st.markdown("### 📊 Session Analytics")
    st.dataframe(pd.DataFrame(st.session_state.logs), use_container_width=True)

# =========================================================
# FOOTER
# =========================================================
st.markdown(f"""
<div class="footer">
AgroNova Elite • AI Farming Intelligence • {datetime.now().year}
</div>
""", unsafe_allow_html=True)
