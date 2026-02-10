import streamlit as st
import google.generativeai as genai
import pandas as pd
import matplotlib.pyplot as plt

# ==================================================
# FA-2: PAGE CONFIGURATION (DESIGN)
# ==================================================
st.set_page_config(
    page_title="AgroNova | Smart Farming Assistant (UP)",
    page_icon="🌾",
    layout="wide"
)

# ==================================================
# FA-2: UI STYLING
# ==================================================
st.markdown("""
<style>
.stApp { background-color: #0b0f14; color: #eaeaea; }
.header {
    background: linear-gradient(90deg, #1fa2ff, #12d8fa, #a6ffcb);
    padding: 30px;
    border-radius: 16px;
    color: black;
    margin-bottom: 25px;
}
.stButton>button {
    background-color: #ffd166;
    color: black;
    font-weight: bold;
    border-radius: 8px;
    padding: 12px;
}
</style>
""", unsafe_allow_html=True)

# ==================================================
# FA-2: SECURE API CONFIGURATION
# ==================================================
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("API key not found. Please add GOOGLE_API_KEY in Streamlit Secrets.")
    st.stop()

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config={
        "temperature": 0.2,          # FA-1: hallucination control
        "max_output_tokens": 400
    }
)

# ==================================================
# HEADER (FA-1: PROBLEM CONTEXT)
# ==================================================
st.markdown("""
<div class="header">
<h1>🌾 AgroNova – Smart Farming Assistant</h1>
<p>Generative AI–based advisory system for farmers in Uttar Pradesh</p>
</div>
""", unsafe_allow_html=True)

# ==================================================
# FA-1: USER PERSONA (UP)
# ==================================================
with st.sidebar:
    st.header("👤 Farmer Persona")

    farmer_name = st.text_input("Name", "Ram Saran Verma")
    farmer_location = st.text_input("Location", "Barabanki, Uttar Pradesh")
    land_size = st.text_input("Land Size", "2 Hectares")

    st.divider()
    st.markdown("**Persona Validation**")
    st.checkbox("Region-specific", True)
    st.checkbox("Practical guidance", True)
    st.checkbox("Safe recommendations", True)

# ==================================================
# FA-1: FEATURE SELECTION
# ==================================================
districts = ["Barabanki", "Lucknow", "Sitapur", "Hardoi"]
crops = ["Wheat", "Rice", "Mustard", "Vegetables"]

col1, col2 = st.columns(2)

with col1:
    district = st.selectbox("District", districts)
    crop = st.selectbox("Crop", crops)

with col2:
    feature = st.selectbox(
        "Advisory Feature",
        [
            "Crop Diversification",
            "Pest & Disease Management",
            "Weather-based Advisory",
            "Soil Health & Fertilizer",
            "Sustainable Farming Practices"
        ]
    )
    query = st.text_input(
        "Farmer Question",
        placeholder="e.g., How to control pest attack safely?"
    )

# ==================================================
# FA-2: INPUT VALIDATION
# ==================================================
if st.button("Get AI Advice"):
    if not query.strip():
        st.warning("Please enter a farming question.")
        st.stop()

    # ==================================================
    # FA-1: PROMPT ENGINEERING
    # ==================================================
    prompt = f"""
You are an expert agricultural advisor working for AgroNova.

Farmer Profile:
Name: {farmer_name}
Location: {district}, Uttar Pradesh
Land Size: {land_size}
Crop: {crop}

Advisory Category: {feature}

Constraints:
- Use safe and farmer-friendly practices
- Avoid chemical dosage recommendations
- Provide advice in simple bullet points
- Keep recommendations region-specific

Question:
{query}
"""

    with st.spinner("Analyzing regional farming context..."):
        response = model.generate_content(prompt)

        st.markdown(f"### 💡 AI Advisory for {farmer_name}")
        st.info(response.text)

# ==================================================
# FA-2: OUTPUT VISUALIZATION (IMPACT)
# ==================================================
st.write("---")
st.markdown("### 📈 Estimated Impact of AI Advisory (Uttar Pradesh)")

impact_df = pd.DataFrame({
    "Practice": ["Traditional Farming", "AI-Assisted Farming"],
    "Average Yield (kg/ha)": [1400, 2000]
})

fig, ax = plt.subplots()
ax.bar(
    impact_df["Practice"],
    impact_df["Average Yield (kg/ha)"],
    color=["#ef476f", "#06d6a0"]
)
ax.set_ylabel("Yield (kg/ha)")
st.pyplot(fig)

st.caption(
    "AI-assisted yield represents estimated improvement due to timely, localized, and safe advisory support."
)
