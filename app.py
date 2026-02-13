import streamlit as st
import requests
import pandas as pd
from datetime import datetime
from google import genai
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

# ======================================================
# PAGE CONFIG
# ======================================================
st.set_page_config(page_title="🌾 AgroNova Enterprise", layout="wide")

# ======================================================
# UI
# ======================================================
st.markdown("""
<style>
.stApp { background: linear-gradient(135deg,#0c2f20,#071e14); color:#e8f5ec; }
.header { background:#145c3a; padding:1.5rem; border-radius:15px; margin-bottom:1rem; }
.card { background:#0f3d28; padding:1rem; border-radius:10px; margin-bottom:1rem; }
.stButton>button { background:#22c55e; color:white; border:none; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="header">
<h1>🌾 AgroNova Enterprise Elite</h1>
<p>Weather-Aware • Multimodal • Risk Classified • Enterprise AI System</p>
</div>
""", unsafe_allow_html=True)

# ======================================================
# API INITIALIZATION
# ======================================================
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("Missing GOOGLE_API_KEY in Streamlit Secrets.")
    st.stop()

client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])

# ======================================================
# MODEL ROUTER
# ======================================================
AVAILABLE_MODELS = [
    "models/gemini-1.5-flash",
    "models/gemini-1.5-pro",
    "models/gemini-3-flash-preview"
]

def get_working_model():
    for model in AVAILABLE_MODELS:
        try:
            client.models.generate_content(
                model=model,
                contents="Test",
                config={"max_output_tokens": 5}
            )
            return model
        except:
            continue
    return None

MODEL_NAME = get_working_model()

if not MODEL_NAME:
    st.error("No accessible Gemini model found. Check API permissions.")
    st.stop()

# ======================================================
# SIDEBAR
# ======================================================
with st.sidebar:
    st.header("Farm Configuration")
    country = st.selectbox("Country", ["India","USA","Canada","Brazil"])
    state = st.text_input("State / Province")
    crop_stage = st.selectbox("Crop Stage",["Planning","Sowing","Growing","Harvesting"])
    goals = st.multiselect("Goals",["High Yield","Low Cost","Organic","Water Saving"])
    temperature = st.slider("AI Creativity",0.2,0.8,0.4)
    language = st.selectbox("Language",["English","Hindi"])
    weather_key = st.text_input("Weather API Key (Optional)")

# ======================================================
# WEATHER SERVICE
# ======================================================
def get_weather(location,key):
    if not key or not location:
        return None
    try:
        url=f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={key}&units=metric"
        data=requests.get(url).json()
        return {
            "Temp":data["main"]["temp"],
            "Humidity":data["main"]["humidity"]
        }
    except:
        return None

weather_data=get_weather(state,weather_key)

if weather_data:
    st.info(f"🌦 Temp: {weather_data['Temp']}°C | Humidity: {weather_data['Humidity']}%")

# ======================================================
# INPUT
# ======================================================
uploaded_image = st.file_uploader("Upload crop image (optional)",type=["jpg","png","jpeg"])
question = st.text_area("Describe farm issue")

# ======================================================
# SAFETY CLASSIFIER
# ======================================================
def classify_risk(text):
    risk_keywords=["toxic","high chemical","dangerous","poison"]
    for word in risk_keywords:
        if word in text.lower():
            return "🔴 High Risk"
    if "chemical" in text.lower():
        return "🟡 Moderate Risk"
    return "🟢 Safe"

# ======================================================
# GENERATE
# ======================================================
if st.button("Generate Enterprise Farm Plan"):

    if not state or not question:
        st.warning("Complete required fields.")
    else:
        try:
            base_prompt=f"""
You are AgroNova Enterprise AI.

Country:{country}
State:{state}
Crop Stage:{crop_stage}
Goals:{', '.join(goals)}
Weather:{weather_data}

Question:{question}

Provide 3 practical recommendations.
Avoid unsafe chemical instructions.
Language:{language}
"""

            contents=base_prompt

            if uploaded_image:
                contents=[
                    {"text":base_prompt},
                    {"inline_data":{
                        "mime_type":uploaded_image.type,
                        "data":uploaded_image.getvalue()
                    }}
                ]

            # Model comparison mode
            response_low=client.models.generate_content(
                model=MODEL_NAME,
                contents=contents,
                config={"temperature":0.3,"max_output_tokens":800}
            )

            response_high=client.models.generate_content(
                model=MODEL_NAME,
                contents=contents,
                config={"temperature":0.7,"max_output_tokens":800}
            )

            low_text=response_low.text if hasattr(response_low,"text") else ""
            high_text=response_high.text if hasattr(response_high,"text") else ""

            st.subheader("Stable Mode (0.3)")
            st.markdown(f'<div class="card">{low_text}</div>',unsafe_allow_html=True)

            st.subheader("Creative Mode (0.7)")
            st.markdown(f'<div class="card">{high_text}</div>',unsafe_allow_html=True)

            risk=classify_risk(low_text)
            st.success(f"Safety Classification: {risk}")

            # ======================================================
            # PDF REPORT
            # ======================================================
            buffer=BytesIO()
            doc=SimpleDocTemplate(buffer)
            styles=getSampleStyleSheet()
            elements=[]

            elements.append(Paragraph("AgroNova Enterprise Report",styles["Heading1"]))
            elements.append(Spacer(1,0.3*inch))
            elements.append(Paragraph(low_text.replace("\n","<br/>"),styles["Normal"]))
            elements.append(Spacer(1,0.3*inch))
            elements.append(Paragraph("Safety: "+risk,styles["Normal"]))

            doc.build(elements)
            buffer.seek(0)

            st.download_button(
                "Download Enterprise PDF",
                buffer,
                file_name="AgroNova_Enterprise_Report.pdf",
                mime="application/pdf"
            )

        except Exception as e:
            st.error("AI service temporarily unavailable.")
