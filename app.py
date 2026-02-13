import streamlit as st
import requests
import pandas as pd
from datetime import datetime
from google import genai
from google.genai import types
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Spacer
from reportlab.lib.pagesizes import A4
from io import BytesIO

# =========================================================
# CONFIG
# =========================================================
st.set_page_config(page_title="🌾 AgroNova FA-3", layout="wide")

MODEL_NAME = "models/gemini-1.5-flash"

# =========================================================
# API SETUP
# =========================================================
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("Add GOOGLE_API_KEY in Streamlit Secrets")
    st.stop()

client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])

# =========================================================
# HEADER
# =========================================================
st.title("🌾 AgroNova – FA-3 Production System")
st.caption("Weather-Aware • Multimodal • Model Validation • PDF Export")

# =========================================================
# SIDEBAR CONFIG
# =========================================================
with st.sidebar:
    st.header("Farm Configuration")

    language = st.selectbox("Language", ["English", "Hindi", "French"])

    country = st.selectbox(
        "Country",
        ["India", "Ghana", "Canada", "USA", "Brazil", "Australia"]
    )

    state = st.text_input("State / Province")

    crop_stage = st.selectbox(
        "Crop Stage",
        ["Planning", "Sowing", "Growing", "Harvesting", "Storage"]
    )

    goals = st.multiselect(
        "Goals",
        ["High Yield", "Low Cost", "Organic", "Water Saving",
         "Pest Control", "Soil Health"]
    )

    weather_key = st.text_input("Weather API Key (OpenWeather)", type="password")

    temperature = st.slider("AI Creativity", 0.2, 0.8, 0.4)

# =========================================================
# WEATHER FUNCTION
# =========================================================
def get_weather(city, api_key):
    if not api_key:
        return "No weather data (API key missing)."

    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(url)
        data = response.json()

        if "main" not in data:
            return "Weather data unavailable."

        return f"""
Temperature: {data['main']['temp']}°C  
Humidity: {data['main']['humidity']}%  
Condition: {data['weather'][0]['description']}
"""
    except:
        return "Weather API error."

weather_info = get_weather(state, weather_key) if state else "No location provided."

# =========================================================
# IMAGE UPLOAD (MULTIMODAL)
# =========================================================
uploaded_image = st.file_uploader(
    "Upload crop image for pest detection",
    type=["jpg", "jpeg", "png"]
)

# =========================================================
# USER INPUT
# =========================================================
user_query = st.text_area("Describe your farm issue")

# =========================================================
# MAIN BUTTON
# =========================================================
if st.button("Generate FA-3 Analysis"):

    if not state:
        st.warning("Please enter your location.")
        st.stop()

    base_prompt = f"""
You are AgroNova, an agricultural AI system.

Farmer Context:
Country: {country}
State: {state}
Crop Stage: {crop_stage}
Goals: {', '.join(goals) if goals else 'General productivity'}

Weather Forecast:
{weather_info}

User Question:
{user_query}

Instructions:
- Provide EXACTLY 3 farming recommendations.
- Each must include Action and Why.
- Use simple language.
- Respond strictly in {language}.
- Avoid unsafe chemical instructions.
"""

    # =====================================================
    # CONTENT BUILD (Multimodal)
    # =====================================================
    contents = [base_prompt]

    if uploaded_image:
        image_part = types.Part.from_bytes(
            uploaded_image.read(),
            mime_type=uploaded_image.type
        )
        contents.append(image_part)

    # =====================================================
    # MODEL COMPARISON
    # =====================================================
    with st.spinner("Generating model comparison..."):

        response_low = client.models.generate_content(
            model=MODEL_NAME,
            contents=contents,
            config={"temperature": 0.3, "max_output_tokens": 900}
        )

        response_high = client.models.generate_content(
            model=MODEL_NAME,
            contents=contents,
            config={"temperature": 0.7, "max_output_tokens": 900}
        )

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Model A (Safe Mode – 0.3)")
        st.markdown(response_low.text)

    with col2:
        st.subheader("Model B (Creative Mode – 0.7)")
        st.markdown(response_high.text)

    # =====================================================
    # SAFETY VALIDATION PASS
    # =====================================================
    safety_prompt = f"""
Classify the safety of this farming advice.

Return one word only:
Green (Safe)
Yellow (Caution)
Red (Unsafe)

Advice:
{response_low.text}
"""

    safety_response = client.models.generate_content(
        model=MODEL_NAME,
        contents=safety_prompt,
        config={"temperature": 0.1}
    )

    st.subheader("Safety Classification")
    st.info(safety_response.text)

    # =====================================================
    # PDF EXPORT
    # =====================================================
    def generate_pdf(text):
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        styles = getSampleStyleSheet()
        elements = []
        elements.append(Paragraph("AgroNova FA-3 Report", styles['Heading1']))
        elements.append(Spacer(1, 12))
        elements.append(Paragraph(text.replace("\n", "<br/>"), styles['Normal']))
        doc.build(elements)
        buffer.seek(0)
        return buffer

    pdf_file = generate_pdf(response_low.text)

    st.download_button(
        label="Download Farm Report (PDF)",
        data=pdf_file,
        file_name="AgroNova_Report.pdf",
        mime="application/pdf"
    )

    # =====================================================
    # VOICE OUTPUT (Browser Speech)
    # =====================================================
    st.markdown(f"""
    <script>
    var msg = new SpeechSynthesisUtterance(`{response_low.text}`);
    msg.lang = "{'hi-IN' if language=='Hindi' else 'fr-FR' if language=='French' else 'en-IN'}";
    window.speechSynthesis.speak(msg);
    </script>
    """, unsafe_allow_html=True)

# =========================================================
# FOOTER
# =========================================================
st.markdown("---")
st.caption(f"AgroNova FA-3 Production System • {datetime.now().year}")
