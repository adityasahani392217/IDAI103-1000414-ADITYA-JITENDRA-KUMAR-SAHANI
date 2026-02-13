import streamlit as st
import requests
from datetime import datetime
from google import genai
from google.genai import types
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from io import BytesIO

# =====================================================
# CONFIG
# =====================================================
st.set_page_config(page_title="🌾 AgroNova", layout="wide")

MODEL_NAME = "gemini-1.5-flash"

# =====================================================
# API SETUP
# =====================================================
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("Add GOOGLE_API_KEY in Streamlit Secrets.")
    st.stop()

client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])

# =====================================================
# HEADER
# =====================================================
st.title("🌾 AgroNova – Smart Farming Intelligence")
st.caption("Weather-Aware • Image Analysis • Model Comparison")

st.warning("This is an educational project. Permission required for real agricultural deployment.")

# =====================================================
# SIDEBAR
# =====================================================
with st.sidebar:
    st.header("Farm Configuration")

    language = st.selectbox("Language", ["English", "Hindi"])

    country = st.selectbox("Country",
                           ["India", "Ghana", "Canada", "USA", "Brazil", "Australia"])

    state = st.text_input("State / Province")

    crop_stage = st.selectbox("Crop Stage",
                              ["Planning", "Sowing", "Growing", "Harvesting", "Storage"])

    goals = st.multiselect("Goals",
                           ["High Yield", "Low Cost", "Organic",
                            "Water Saving", "Pest Control", "Soil Health"])

    weather_key = st.text_input("OpenWeather API Key", type="password")

    creativity = st.slider("AI Creativity", 0.2, 0.8, 0.4)

# =====================================================
# WEATHER
# =====================================================
def get_weather(city, key):
    if not key or not city:
        return "Weather data unavailable."

    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={key}&units=metric"
        r = requests.get(url)
        data = r.json()

        if "main" not in data:
            return "Weather data unavailable."

        return f"""
Temperature: {data['main']['temp']}°C  
Humidity: {data['main']['humidity']}%  
Condition: {data['weather'][0]['description']}
"""
    except:
        return "Weather service error."

weather_info = get_weather(state, weather_key)

# =====================================================
# IMAGE UPLOAD
# =====================================================
uploaded_image = st.file_uploader(
    "Upload Crop Image (optional)",
    type=["jpg", "jpeg", "png"]
)

# =====================================================
# USER QUESTION
# =====================================================
question = st.text_area("Describe your farming issue")

# =====================================================
# GENERATE
# =====================================================
if st.button("Generate Analysis"):

    if not state:
        st.warning("Enter location first.")
        st.stop()

    base_prompt = f"""
You are an agricultural advisory assistant.

Farmer Context:
Country: {country}
State: {state}
Crop Stage: {crop_stage}
Goals: {', '.join(goals) if goals else 'General productivity'}

Weather:
{weather_info}

User Question:
{question}

Instructions:
- Provide exactly 3 recommendations.
- Each must contain Action and Why.
- Use simple language.
- Respond in {language}.
- Avoid unsafe chemical instructions.
"""

    try:

        # Build content correctly
        if uploaded_image:
            image_bytes = uploaded_image.read()

            contents = [
                types.Content(
                    role="user",
                    parts=[
                        types.Part.from_text(base_prompt),
                        types.Part.from_bytes(
                            data=image_bytes,
                            mime_type=uploaded_image.type
                        )
                    ]
                )
            ]
        else:
            contents = base_prompt

        with st.spinner("Generating comparison..."):

            response_low = client.models.generate_content(
                model=MODEL_NAME,
                contents=contents,
                config=types.GenerateContentConfig(
                    temperature=0.3,
                    max_output_tokens=900
                )
            )

            response_high = client.models.generate_content(
                model=MODEL_NAME,
                contents=contents,
                config=types.GenerateContentConfig(
                    temperature=0.7,
                    max_output_tokens=900
                )
            )

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Conservative Model (0.3)")
            st.markdown(response_low.text)

        with col2:
            st.subheader("Creative Model (0.7)")
            st.markdown(response_high.text)

        # =====================================================
        # SAFETY CHECK
        # =====================================================
        safety_prompt = f"""
Classify this advice as:
Green (Safe)
Yellow (Caution)
Red (Unsafe)

Return only one word.

Advice:
{response_low.text}
"""

        safety = client.models.generate_content(
            model=MODEL_NAME,
            contents=safety_prompt,
            config=types.GenerateContentConfig(temperature=0.1)
        )

        st.subheader("Safety Indicator")
        st.info(safety.text)

        # =====================================================
        # PDF EXPORT
        # =====================================================
        def create_pdf(text):
            buffer = BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=A4)
            styles = getSampleStyleSheet()
            elements = []
            elements.append(Paragraph("AgroNova Farm Report", styles["Heading1"]))
            elements.append(Spacer(1, 12))
            elements.append(Paragraph(text.replace("\n", "<br/>"), styles["Normal"]))
            doc.build(elements)
            buffer.seek(0)
            return buffer

        pdf = create_pdf(response_low.text)

        st.download_button(
            "Download PDF Report",
            data=pdf,
            file_name="AgroNova_Report.pdf",
            mime="application/pdf"
        )

        # =====================================================
        # VOICE OUTPUT
        # =====================================================
        st.markdown(f"""
        <script>
        var msg = new SpeechSynthesisUtterance(`{response_low.text}`);
        msg.lang = "{'hi-IN' if language=='Hindi' else 'en-IN'}";
        window.speechSynthesis.speak(msg);
        </script>
        """, unsafe_allow_html=True)

    except Exception as e:
        st.error("AI service temporarily unavailable.")
        st.code(str(e))

# =====================================================
# FOOTER
# =====================================================
st.markdown("---")
st.caption(f"AgroNova • Educational Smart Farming System • {datetime.now().year}")
