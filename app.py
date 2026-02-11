import streamlit as st
import pandas as pd
from datetime import datetime
from google import genai

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="FarmaBuddy 🌱",
    page_icon="🌾",
    layout="wide"
)

# ---------------- API KEY & CLIENT ----------------
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("⚠️ GOOGLE_API_KEY missing in Streamlit Secrets")
    st.stop()

api_key = st.secrets["GOOGLE_API_KEY"]

# Use stable v1 client
client = genai.Client(api_key=api_key)

# ---------------- HEADER ----------------
st.markdown(
    """
    <h1 style='text-align:center;'>🌱 FarmaBuddy</h1>
    <h4 style='text-align:center;'>AI-Powered Smart Farming Assistant</h4>
    <p style='text-align:center;'>Built using Gemini | Deployed with Streamlit</p>
    <hr>
    """,
    unsafe_allow_html=True
)

# ---------------- USER INPUTS ----------------
st.sidebar.header("🌍 Farmer Inputs")

region = st.sidebar.selectbox(
    "Select Region",
    ["India", "Ghana", "Canada"]
)

location = st.sidebar.text_input(
    "Enter Location (State / Province)"
)

crop_stage = st.sidebar.selectbox(
    "Crop Stage",
    ["Planning", "Sowing", "Growing", "Harvesting"]
)

priority = st.sidebar.multiselect(
    "Your Priorities",
    ["Low Water Use", "High Yield", "Organic Farming", "Low Cost"]
)

temperature = st.sidebar.slider(
    "AI Creativity Level",
    0.2,
    0.9,
    0.5
)

# ---------------- PROMPT ENGINE ----------------
def build_prompt():
    return f"""
You are a professional agricultural advisor helping farmers.

Farmer Profile:
Country/Region: {region}
Location: {location}
Crop Stage: {crop_stage}
Priorities: {', '.join(priority) if priority else "General Best Practices"}

INSTRUCTIONS:
- Provide EXACTLY 3 clear farming recommendations.
- Format each recommendation using this structure:

Recommendation 1:
• Action:
• Why:

Recommendation 2:
• Action:
• Why:

Recommendation 3:
• Action:
• Why:

- Keep language simple and practical.
- Make advice region-specific.
- Avoid unsafe chemical instructions.
- Ensure full explanation.
"""

# ---------------- SAFE RESPONSE EXTRACTOR ----------------
def extract_text(response):
    # Primary extraction
    if hasattr(response, "text") and response.text:
        return response.text
    
    # Fallback extraction
    if hasattr(response, "candidates"):
        try:
            return response.candidates[0].content.parts[0].text
        except:
            return "⚠️ Could not parse full response."

    return "⚠️ No content returned."

# ---------------- MAIN ACTION ----------------
if st.button("🌾 Get Smart Advice"):

    if not location:
        st.warning("Please enter your location.")
    else:
        try:
            response = client.models.generate_content(
                model="gemini-3-flash-preview",  # Stable and widely supported
                contents=build_prompt(),
                config={
                    "temperature": temperature,
                    "max_output_tokens": 1024  # Increased to avoid truncation
                }
            )

            full_output = extract_text(response)

            st.success("Here’s your AI-generated farming advice:")
            st.markdown(full_output)

        except Exception as e:
            st.error("⚠️ AI service temporarily unavailable.")
            st.code(str(e))

# ---------------- FEEDBACK CHECKLIST ----------------
st.markdown("## ✅ AI Output Validation Checklist")

feedback = {
    "Region-specific advice": st.checkbox("Advice is specific to my region"),
    "Logical reasoning": st.checkbox("Suggestions include valid reasoning"),
    "Simple language": st.checkbox("Language is easy to understand"),
    "Actionable steps": st.checkbox("Advice can be applied practically"),
    "Safe & ethical": st.checkbox("No unsafe or misleading information")
}

if st.button("📊 Submit Feedback"):
    score = sum(feedback.values())
    st.info(f"Feedback Score: {score}/5")

# ---------------- USAGE LOG ----------------
st.markdown("## 📈 Usage Snapshot")

log_data = {
    "Time": datetime.now().strftime("%Y-%m-%d %H:%M"),
    "Region": region,
    "Crop Stage": crop_stage
}

st.dataframe(pd.DataFrame([log_data]))

# ---------------- FOOTER ----------------
st.markdown(
    "<hr><p style='text-align:center; font-size:14px;'>FA-2 Project | 2026</p>",
    unsafe_allow_html=True
)
