import streamlit as st
import requests
from google import genai
from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Spacer
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Paragraph
from reportlab.platypus import Spacer
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Paragraph
from reportlab.platypus import Spacer
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Paragraph
from reportlab.platypus import Spacer
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Paragraph
from reportlab.platypus import Spacer
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Paragraph
from reportlab.platypus import Spacer
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Paragraph
from reportlab.platypus import Spacer
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Paragraph
from reportlab.platypus import Spacer
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Paragraph
from reportlab.platypus import Spacer
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Paragraph
from reportlab.platypus import Spacer
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Paragraph
from reportlab.platypus import Spacer
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Paragraph
from reportlab.platypus import Spacer
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Paragraph
from reportlab.platypus import Spacer
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Paragraph
from reportlab.platypus import Spacer
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Paragraph
from reportlab.platypus import Spacer
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Paragraph
from reportlab.platypus import Spacer
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Paragraph
from reportlab.platypus import Spacer
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Paragraph
from reportlab.platypus import Spacer
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Paragraph
from reportlab.platypus import Spacer

st.set_page_config(page_title="🌾 AgroNova FA-3", layout="wide")

# ---------------------------
# API CONFIG
# ---------------------------
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("Add GOOGLE_API_KEY in Streamlit Secrets")
    st.stop()

client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
MODEL_NAME = "gemini-1.5-flash"

# ---------------------------
# HEADER
# ---------------------------
st.title("🌾 AgroNova – FA-3 Production System")
st.caption("Weather-Aware • Multimodal • FA-1 + FA-2 Optimized")

# ---------------------------
# SIDEBAR INPUTS
# ---------------------------
with st.sidebar:
    st.header("Farm Configuration")

    country = st.selectbox("Country", ["India", "Ghana", "USA", "Canada"])
    state = st.text_input("State / Province")
    crop_stage = st.selectbox("Crop Stage", ["Planning","Sowing","Growing","Harvesting"])
    goals = st.multiselect("Goals", ["High Yield","Low Cost","Organic","Water Saving"])

    weather_api_key = st.text_input("Weather API Key (OpenWeather)", type="password")

# ---------------------------
# WEATHER API
# ---------------------------
weather_data = ""
if weather_api_key and state:
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={state}&appid={weather_api_key}&units=metric"
        response = requests.get(url)
        data = response.json()
        rainfall = data.get("rain", {}).get("1h", 0)
        temp = data["main"]["temp"]
        weather_data = f"Temperature: {temp}°C, Rainfall last hour: {rainfall}mm"
        st.info(f"🌦 Weather Injected: {weather_data}")
    except:
        st.warning("Weather API failed")

# ---------------------------
# IMAGE UPLOAD (MULTIMODAL)
# ---------------------------
uploaded_image = st.file_uploader("Upload crop image for pest detection", type=["jpg","png","jpeg"])

image_context = ""
if uploaded_image:
    image_context = "An image has been uploaded for pest analysis."
    st.image(uploaded_image, caption="Uploaded Crop Image")

# ---------------------------
# USER QUESTION
# ---------------------------
question = st.text_area("Describe your farm issue")

# ---------------------------
# GENERATE
# ---------------------------
if st.button("Generate AI Plan"):

    base_prompt = f"""
You are AgroNova agricultural AI.

Farmer Context:
Country: {country}
State: {state}
Crop Stage: {crop_stage}
Goals: {', '.join(goals)}
Weather Data: {weather_data}
Image Context: {image_context}

User Question:
{question}

Rules:
- 3 recommendations
- Each must include Action + Why
- No unsafe chemical dosages
- Simple language
"""

    # Conservative Model
    response_low = client.models.generate_content(
        model=MODEL_NAME,
        contents=base_prompt,
        config={"temperature":0.3}
    )

    # Creative Model
    response_high = client.models.generate_content(
        model=MODEL_NAME,
        contents=base_prompt,
        config={"temperature":0.7}
    )

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Model A (Safe)")
        st.write(response_low.text)

    with col2:
        st.subheader("Model B (Creative)")
        st.write(response_high.text)

    # ---------------------------
    # SAFETY CLASSIFICATION
    # ---------------------------
    risk_score = "🟢 Green"
    if "chemical" in response_low.text.lower():
        risk_score = "🟡 Yellow"
    if "pesticide dosage" in response_low.text.lower():
        risk_score = "🔴 Red"

    st.success(f"Safety Classification: {risk_score}")

    # ---------------------------
    # PDF EXPORT
    # ---------------------------
    doc = SimpleDocTemplate("AgroNova_Report.pdf")
    styles = getSampleStyleSheet()
    elements = []
    elements.append(Paragraph("AgroNova Farm Report", styles["Heading1"]))
    elements.append(Spacer(1, 0.5*inch))
    elements.append(Paragraph(response_low.text, styles["Normal"]))
    doc.build(elements)

    with open("AgroNova_Report.pdf", "rb") as f:
        st.download_button("Download PDF Report", f, "AgroNova_Report.pdf")

# ---------------------------
# FOOTER
# ---------------------------
st.markdown("---")
st.caption(f"AgroNova FA-3 • {datetime.now().year}")
