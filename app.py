import streamlit as st
import pandas as pd
import requests
from datetime import datetime
from google import genai
from google.genai import types
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate
from io import BytesIO

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="🌾 AgroNova",
    page_icon="🌱",
    layout="wide"
)

# =====================================================
# PREMIUM CLEAN GREEN UI
# =====================================================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg,#071e14,#0c2f20);
    color:#e8f5ec;
}
.block-container {max-width:1100px;padding-top:2rem;}
.header {
    background:linear-gradient(90deg,#0f3d28,#145c3a);
    padding:2rem;border-radius:16px;margin-bottom:2rem;
}
.card {
    background:#0f3d28;
    padding:1.5rem;border-radius:14px;margin-bottom:1rem;
}
.recommendation {
    background:#0c3323;
    padding:1.2rem;border-left:4px solid #22c55e;
    border-radius:12px;margin-bottom:1rem;
}
.safe {color:#22c55e;font-weight:600;}
.caution {color:#facc15;font-weight:600;}
.danger {color:#ef4444;font-weight:600;}
.footer {text-align:center;margin-top:3rem;opacity:0.7;}
</style>
""", unsafe_allow_html=True)

# =====================================================
# API KEY
# =====================================================
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("Add GOOGLE_API_KEY in Streamlit Secrets")
    st.stop()

client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])

# =====================================================
# MODEL CONFIG (FOR YOUR ACCOUNT)
# =====================================================

MODEL_NAME = "gemini-3-flash-preview"

try:
    client.models.generate_content(
        model=MODEL_NAME,
        contents="test",
        config={"max_output_tokens": 5}
    )
except Exception as e:
    st.error("Gemini model not accessible. Check API key permissions.")
    st.stop()


# =====================================================
# HEADER
# =====================================================
st.markdown("""
<div class="header">
<h1>🌾 AgroNova – Elite Production System</h1>
<p>Weather-Aware • Multimodal • Safety Validated • Enterprise Architecture</p>
</div>
""", unsafe_allow_html=True)

# =====================================================
# SIDEBAR
# =====================================================
with st.sidebar:
    st.header("Farm Configuration")

    country = st.selectbox("Country",
        ["India","Ghana","Canada","USA","Brazil","Australia"])

    state = st.text_input("State / Province")

    crop_stage = st.selectbox("Crop Stage",
        ["Planning","Sowing","Growing","Harvesting","Storage"])

    goals = st.multiselect("Goals",
        ["High Yield","Low Cost","Organic","Water Saving","Pest Control","Soil Health"])

    weather_api = st.text_input("Weather API Key (OpenWeather)")

    temperature = st.slider("AI Creativity",0.2,0.8,0.4)

# =====================================================
# WEATHER INTEGRATION
# =====================================================
def get_weather(city, key):
    if not city or not key:
        return "Weather data unavailable."
    try:
        url=f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={key}&units=metric"
        r=requests.get(url).json()
        if "weather" in r:
            return f"{r['weather'][0]['main']}, {r['main']['temp']}°C"
        return "Weather unavailable."
    except:
        return "Weather unavailable."

weather_summary = get_weather(state, weather_api)

# =====================================================
# MULTIMODAL CONTENT BUILDER
# =====================================================
def build_contents(prompt_text, image_file):
    if image_file:
        img_bytes=image_file.read()
        return [
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(prompt_text),
                    types.Part.from_bytes(
                        data=img_bytes,
                        mime_type=image_file.type
                    )
                ]
            )
        ]
    return prompt_text

# =====================================================
# PDF GENERATOR
# =====================================================
def generate_pdf(text):
    buffer=BytesIO()
    doc=SimpleDocTemplate(buffer)
    styles=getSampleStyleSheet()
    story=[]
    story.append(Paragraph(text, styles["Normal"]))
    doc.build(story)
    buffer.seek(0)
    return buffer

# =====================================================
# MAIN AREA
# =====================================================
uploaded_image = st.file_uploader("Upload crop image for pest detection", type=["jpg","png","jpeg"])

question = st.text_area("Describe your farm issue")

if st.button("Generate Elite Farm Plan"):

    if not state:
        st.warning("Please enter state/province.")
    else:
        base_prompt=f"""
You are AgroNova, an expert agricultural AI advisor.

Farmer Context:
Country: {country}
State: {state}
Crop Stage: {crop_stage}
Goals: {', '.join(goals) if goals else 'General'}
Current Weather: {weather_summary}

Provide EXACTLY 3 recommendations:

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
Avoid unsafe chemicals.
"""

        contents=build_contents(base_prompt, uploaded_image)

        try:
            with st.spinner("Running dual model validation..."):

                # Low temperature
                response_low=client.models.generate_content(
                    model=MODEL_NAME,
                    contents=contents,
                    config={"temperature":0.3,"max_output_tokens":900}
                )

                # High temperature
                response_high=client.models.generate_content(
                    model=MODEL_NAME,
                    contents=contents,
                    config={"temperature":0.7,"max_output_tokens":900}
                )

                text_low=response_low.text if hasattr(response_low,"text") else ""
                text_high=response_high.text if hasattr(response_high,"text") else ""

                st.success("Comparison Generated")

                col1,col2=st.columns(2)

                with col1:
                    st.subheader("Stable Output (0.3)")
                    st.markdown(f'<div class="recommendation">{text_low}</div>',unsafe_allow_html=True)

                with col2:
                    st.subheader("Creative Output (0.7)")
                    st.markdown(f'<div class="recommendation">{text_high}</div>',unsafe_allow_html=True)

                # SAFETY CLASSIFICATION
                safety_prompt=f"""
Classify this advice as SAFE, CAUTION, or UNSAFE:

{text_low}

Return only one word.
"""
                safety=client.models.generate_content(
                    model=MODEL_NAME,
                    contents=safety_prompt
                )

                label=safety.text.strip().upper()

                if "SAFE" in label:
                    st.markdown('<p class="safe">🟢 Safety Status: SAFE</p>',unsafe_allow_html=True)
                elif "CAUTION" in label:
                    st.markdown('<p class="caution">🟡 Safety Status: CAUTION</p>',unsafe_allow_html=True)
                else:
                    st.markdown('<p class="danger">🔴 Safety Status: UNSAFE</p>',unsafe_allow_html=True)

                # PDF EXPORT
                pdf_buffer=generate_pdf(text_low)
                st.download_button(
                    label="Download Farm Report (PDF)",
                    data=pdf_buffer,
                    file_name="AgroNova_Report.pdf",
                    mime="application/pdf"
                )

        except Exception as e:
            st.error("AI service temporarily unavailable.")
            st.code(str(e))

# =====================================================
# FOOTER
# =====================================================
st.markdown(f"""
<div class="footer">
AgroNova • Elite AI Agricultural Intelligence • {datetime.now().year}
</div>
""", unsafe_allow_html=True)
