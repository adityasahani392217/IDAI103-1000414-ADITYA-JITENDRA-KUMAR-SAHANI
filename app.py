import streamlit as st
import requests
import pandas as pd
from datetime import datetime
from google import genai
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Paragraph
from reportlab.platypus import Spacer
from reportlab.lib.styles import getSampleStyleSheet
import tempfile
import os

# -----------------------------------
# CONFIG
# -----------------------------------
st.set_page_config(page_title="🌾 AgroNova Elite", layout="wide")

MODEL_NAME = "gemini-1.5-flash"

# -----------------------------------
# GEMINI SETUP
# -----------------------------------
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("Add GOOGLE_API_KEY in Streamlit Secrets")
    st.stop()

client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])

# -----------------------------------
# WEATHER API FUNCTION
# -----------------------------------
def get_weather(location):
    try:
        url = f"https://geocoding-api.open-meteo.com/v1/search?name={location}"
        geo = requests.get(url).json()
        lat = geo["results"][0]["latitude"]
        lon = geo["results"][0]["longitude"]

        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=rain_sum&timezone=auto"
        weather = requests.get(weather_url).json()
        rainfall = weather["daily"]["rain_sum"][0]
        return rainfall
    except:
        return None

# -----------------------------------
# SAFETY CLASSIFIER
# -----------------------------------
def safety_score(text):
    danger_words = ["overdose", "toxic", "high chemical", "spray heavily"]
    score = 0

    for word in danger_words:
        if word in text.lower():
            score += 1

    if score == 0:
        return "🟢 Safe"
    elif score == 1:
        return "🟡 Review"
    else:
        return "🔴 Risky"

# -----------------------------------
# PDF EXPORT
# -----------------------------------
def generate_pdf(content):
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    doc = SimpleDocTemplate(temp_file.name)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("AgroNova Farm Report", styles["Heading1"]))
    elements.append(Spacer(1, 0.3 * inch))
    elements.append(Paragraph(content, styles["Normal"]))

    doc.build(elements)
    return temp_file.name

# -----------------------------------
# UI
# -----------------------------------
st.title("🌾 AgroNova Elite Smart Farming AI")

col1, col2 = st.columns(2)

with col1:
    country = st.selectbox("Country", ["India", "Ghana", "Canada", "USA"])
    location = st.text_input("State / Province")
    crop_stage = st.selectbox("Crop Stage", ["Planning", "Sowing", "Growing", "Harvesting"])
    priorities = st.multiselect("Goals", ["High Yield", "Low Cost", "Organic"])

with col2:
    model_compare = st.checkbox("Enable Model Comparison Mode")
    image = st.file_uploader("Upload Crop Image (Pest Detection)", type=["jpg","png"])
    user_question = st.text_area("Ask Farming Question")

# -----------------------------------
# GENERATE
# -----------------------------------
if st.button("Generate Smart Plan"):

    rainfall = get_weather(location)
    rainfall_text = f"Expected rainfall today: {rainfall} mm." if rainfall else "Weather unavailable."

    base_prompt = f"""
You are AgroNova AI.

Country: {country}
Location: {location}
Crop Stage: {crop_stage}
Goals: {', '.join(priorities)}
Weather: {rainfall_text}

Question:
{user_question}

Provide 3 clear recommendations with:
• Action
• Why
"""

    # MODEL 1
    response_safe = client.models.generate_content(
        model=MODEL_NAME,
        contents=base_prompt,
        config={"temperature": 0.3}
    )

    text_safe = response_safe.text if hasattr(response_safe, "text") else ""

    if model_compare:
        response_creative = client.models.generate_content(
            model=MODEL_NAME,
            contents=base_prompt,
            config={"temperature": 0.7}
        )
        text_creative = response_creative.text

        colA, colB = st.columns(2)
        with colA:
            st.subheader("🛡 Conservative AI (0.3)")
            st.write(text_safe)

        with colB:
            st.subheader("🎨 Creative AI (0.7)")
            st.write(text_creative)

    else:
        st.subheader("📋 Recommendations")
        st.write(text_safe)

    # SAFETY SCORE
    score = safety_score(text_safe)
    st.markdown(f"### Safety Classification: {score}")

    # PDF EXPORT
    pdf_path = generate_pdf(text_safe)
    with open(pdf_path, "rb") as f:
        st.download_button("Download Farm Report (PDF)", f, file_name="AgroNova_Report.pdf")

# -----------------------------------
# IMAGE ANALYSIS
# -----------------------------------
if image is not None:
    st.image(image)
    st.write("Analyzing image...")

    image_bytes = image.read()

    response_img = client.models.generate_content(
        model=MODEL_NAME,
        contents=[
            {"role": "user", "parts": [{"text": "Analyze this crop image for pest or disease."},
                                       {"inline_data": {"mime_type": "image/png", "data": image_bytes}}]}
        ]
    )

    st.write(response_img.text)

# -----------------------------------
# FOOTER
# -----------------------------------
st.markdown("---")
st.markdown(f"AgroNova Elite • {datetime.now().year}")
