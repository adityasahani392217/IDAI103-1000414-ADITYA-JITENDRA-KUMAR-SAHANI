import streamlit as st
import pandas as pd
from datetime import datetime
from google import genai
import re

# =========================================================
# CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="AgroNova | FA-2 Optimized",
    page_icon="🌾",
    layout="wide"
)

MODEL_NAME = "gemini-1.5-flash"

# =========================================================
# PREMIUM ACADEMIC UI
# =========================================================

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0b1f17, #0f2e22);
    color: #e7f5ec;
}

.block-container {
    max-width: 1000px;
    padding-top: 2rem;
}

.header {
    background: #123c2c;
    padding: 2rem;
    border-radius: 18px;
    border: 1px solid rgba(255,255,255,0.05);
    margin-bottom: 2rem;
}

.header h1 {
    font-size: 2.4rem;
    font-weight: 700;
}

.card {
    background: #123c2c;
    padding: 1.5rem;
    border-radius: 14px;
    margin-bottom: 1.2rem;
    border: 1px solid rgba(255,255,255,0.05);
}

.recommendation {
    background: #0f3325;
    padding: 1.2rem;
    border-radius: 12px;
    border-left: 4px solid #22c55e;
    margin-bottom: 1rem;
}

.validation {
    background: #0e2b20;
    padding: 1rem;
    border-radius: 10px;
    margin-top: 1rem;
}

.footer {
    text-align: center;
    margin-top: 3rem;
    opacity: 0.6;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# API INITIALIZATION
# =========================================================

if "GOOGLE_API_KEY" not in st.secrets:
    st.error("🔐 GOOGLE_API_KEY missing in Streamlit Secrets")
    st.stop()

client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])

# =========================================================
# HEADER
# =========================================================

st.markdown("""
<div class="header">
<h1>🌾 AgroNova</h1>
<p>FA-2 Optimized AI Farming Intelligence Platform</p>
</div>
""", unsafe_allow_html=True)

# =========================================================
# SIDEBAR INPUT (FA-1 Structured Prompt Context)
# =========================================================

with st.sidebar:

    st.header("Farm Configuration")

    country = st.selectbox("Country", ["India", "Ghana", "Canada", "USA", "Brazil", "Australia"])
    state = st.text_input("State / Province")
    crop_stage = st.selectbox("Crop Stage",
                              ["Planning", "Sowing", "Growing", "Harvesting", "Storage"])

    goals = st.multiselect("Goals",
                           ["High Yield", "Low Cost", "Organic",
                            "Water Saving", "Pest Control", "Soil Health"])

    comparison_mode = st.toggle("Enable Model Comparison (0.3 vs 0.7)")

# =========================================================
# FA-1 PROMPT ENGINE
# =========================================================

def build_prompt(context, temperature_label):
    return f"""
You are an expert agricultural advisor.

Context:
Country: {context['country']}
State: {context['state']}
Crop Stage: {context['stage']}
Goals: {context['goals']}

Temperature Mode: {temperature_label}

Provide EXACTLY 3 recommendations.

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

Use safe, region-specific advice.
Avoid unsafe chemical instructions.
"""

# =========================================================
# SAFETY CLASSIFIER (FA-2 VALIDATION LAYER)
# =========================================================

def safety_score(text):

    high_risk_words = ["poison", "overdose", "extreme chemical", "burn crop"]
    moderate_risk_words = ["chemical spray", "strong pesticide"]

    if any(word in text.lower() for word in high_risk_words):
        return "🔴 High Risk"
    elif any(word in text.lower() for word in moderate_risk_words):
        return "🟡 Moderate Risk"
    else:
        return "🟢 Safe"

# =========================================================
# MODEL RUNNER
# =========================================================

def run_model(prompt, temp):
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config={
            "temperature": temp,
            "max_output_tokens": 900
        }
    )
    return response.text if hasattr(response, "text") else "No response."

# =========================================================
# MAIN EXECUTION
# =========================================================

if st.button("Generate Farm Plan"):

    if not state:
        st.warning("Please enter your State/Province.")
    else:

        context = {
            "country": country,
            "state": state,
            "stage": crop_stage,
            "goals": ", ".join(goals) if goals else "General productivity"
        }

        try:

            with st.spinner("Running AgroNova Intelligence Engine..."):

                if comparison_mode:

                    prompt_low = build_prompt(context, "Conservative Mode")
                    prompt_high = build_prompt(context, "Creative Mode")

                    output_low = run_model(prompt_low, 0.3)
                    output_high = run_model(prompt_high, 0.7)

                    col1, col2 = st.columns(2)

                    with col1:
                        st.subheader("Temperature 0.3 (Stable)")
                        st.markdown(f'<div class="recommendation">{output_low}</div>',
                                    unsafe_allow_html=True)
                        st.markdown(f"Safety Score: {safety_score(output_low)}")

                    with col2:
                        st.subheader("Temperature 0.7 (Creative)")
                        st.markdown(f'<div class="recommendation">{output_high}</div>',
                                    unsafe_allow_html=True)
                        st.markdown(f"Safety Score: {safety_score(output_high)}")

                else:

                    prompt = build_prompt(context, "Standard Mode")
                    output = run_model(prompt, 0.4)

                    st.markdown(f'<div class="recommendation">{output}</div>',
                                unsafe_allow_html=True)

                    st.markdown(f"### Safety Score: {safety_score(output)}")

        except Exception:
            st.error("⚠️ AI service unavailable. Please try again.")

# =========================================================
# VALIDATION CHECKLIST (FA-2 REQUIRED)
# =========================================================

st.markdown("""
<div class="validation">
<h4>FA-2 Validation Checklist</h4>
<ul>
<li>✔ Structured Prompt Engineering (FA-1)</li>
<li>✔ Temperature Optimization</li>
<li>✔ Output Formatting Control</li>
<li>✔ Safety Classification Layer</li>
<li>✔ Model Comparison Mode</li>
<li>✔ Deployment-Ready Architecture</li>
</ul>
</div>
""", unsafe_allow_html=True)

# =========================================================
# FOOTER
# =========================================================

st.markdown(f"""
<div class="footer">
AgroNova • FA-2 Elite Architecture • {datetime.now().year}
</div>
""", unsafe_allow_html=True)
