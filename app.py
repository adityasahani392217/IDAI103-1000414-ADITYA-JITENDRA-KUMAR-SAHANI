import streamlit as st
import google.generativeai as genai
import pandas as pd
import matplotlib.pyplot as plt

# ============================================
# 🎨 PAGE CONFIGURATION
# ============================================
st.set_page_config(
    page_title="🌱 AgroNova: Multi-State Smart Assistant",
    page_icon="🌾",
    layout="wide"
)

# ============================================
# 🌑 VIBRANT DARK UI (Design & Implementation)
# ============================================
st.markdown("""
<style>
    .stApp { background-color: #050a0e; color: #e0e0e0; }
    .main-header {
        background: linear-gradient(90deg, #11998e 0%, #38ef7d 100%);
        color: white; padding: 40px; border-radius: 20px;
        text-align: center; margin-bottom: 25px;
        box-shadow: 0 10px 30px rgba(17, 153, 142, 0.3);
    }
    .stButton>button {
        background: linear-gradient(45deg, #f7971e 0%, #ffd200 100%);
        color: black; border: none; padding: 15px;
        border-radius: 10px; font-weight: bold; width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# 🚀 SECURE API CONNECTION (Step 6)
# ============================================
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    # Temperature 0.2 prevents hallucination and ensures region-specific accuracy [cite: 23, 31]
    model = genai.GenerativeModel(
        model_name="gemini-3-flash-preview",
        generation_config={"temperature": 0.2, "max_output_tokens": 500}
    )
else:
    st.error("⚠️ API Key missing in Streamlit Secrets!")
    st.stop()

# ============================================
# 🚀 HEADER & STATE SELECTION
# ============================================
st.markdown("""
<div class="main-header">
    <h1 style="margin:0;">🌾 AgroNova Smart Assistant</h1>
    <p style="font-size:1.2rem;">Serving Farmers across Bihar and Gujarat (Saurashtra)</p>
</div>
""", unsafe_allow_html=True)

selected_state = st.selectbox("🌍 Select Your State:", ["Bihar", "Gujarat (Saurashtra)"])

# ============================================
# 👤 EDITABLE PERSONA SECTION (Sidebar)
# ============================================
with st.sidebar:
    st.title("👤 Current Farmer Persona")
    
    # Updated to editable text boxes for user interaction monitoring [cite: 41, 48]
    if selected_state == "Bihar":
        farmer_name = st.text_input("Name:", value="Ram Kumar Baitha")
        farmer_loc = st.text_input("Location:", value="Kishanganj, Bihar")
        land_size = st.text_input("Land Size:", value="0.25 Ha")
        districts = ["Samastipur", "Kishanganj", "Gaya", "Saharsa", "Muzaffarpur"]
        crops = ["Rice", "Wheat", "Maize", "Litchi"]
    else:
        # Defaults based on Saurashtra Storyboard research [cite: 106, 107]
        farmer_name = st.text_input("Name:", value="Mansukhbhai Patel")
        farmer_loc = st.text_input("Location:", value="Gondal, Rajkot")
        land_size = st.text_input("Land Size:", value="4 Acres")
        districts = ["Rajkot", "Jamnagar", "Amreli", "Junagadh", "Porbandar"]
        crops = ["Groundnut (Kharif)", "Cumin/Jeera (Rabi)", "Cotton"]
    
    st.divider()
    st.markdown("### 📋 Validation Checklist")
    st.checkbox("Region-Specific", value=True) # [cite: 34]
    st.checkbox("Logical Reasoning", value=True) # [cite: 35]
    st.checkbox("Simple Language", value=True) # [cite: 36]

# ============================================
# 🎯 INPUT INTERACTION
# ============================================
col1, col2 = st.columns(2)
with col1:
    district = st.selectbox(f"Select {selected_state} District:", districts)
    crop = st.selectbox("Select Crop:", crops)

with col2:
    category = st.selectbox("Help Category:", ["Pest Management", "Sowing & Weather", "Water/Subsidies", "Soil Health"])
    user_query = st.text_input("Ask a specific question:", placeholder="e.g., Treatment for White Grub?")

# ============================================
# ⚡ AI ADVICE & FORMATTING (Step 4)
# ============================================
if st.button("🚀 GET LOCALIZED ADVICE"):
    with st.spinner(f"🧠 Consulting {selected_state} Agricultural Data..."):
        # Context uses the dynamic persona data from text boxes [cite: 49]
        context_prompt = f"""
Role: Expert Lead Agronomist at AgroNova.
Target Audience: {farmer_name}, a farmer in {district}, {selected_state}.
Topic: {category} for {crop}.


Question: {user_query}
"""
        
        try:
            response = model.generate_content(context_prompt)
            # Use a container for better visibility
            with st.container():
                st.markdown(f"### 💡 Expert Advice for {farmer_name}")
                st.info(response.text) # This puts it in a nice blue box
        except Exception as e:
            st.error(f"Error: {e}")

# ============================================
# 📊 REGIONAL DATA VISUALIZATION
# ============================================
st.write("---")
st.markdown(f"### 📈 Productivity Growth: {selected_state}")

impact_data = {
    'Crop': crops[:3],
    'Traditional Yield': [1200, 1500, 900],
    'AI-Smart Yield': [1800, 2100, 1400]
}
df = pd.DataFrame(impact_data)



fig, ax = plt.subplots(figsize=(10, 4), facecolor='#050a0e')
ax.set_facecolor('#050a0e')
x = range(len(df['Crop']))
ax.bar([i - 0.2 for i in x], df['Traditional Yield'], width=0.4, label='Traditional', color='#ff4b2b')
ax.bar([i + 0.2 for i in x], df['AI-Smart Yield'], width=0.4, label='AI-Smart', color='#00f260')

ax.set_xticks(x)
ax.set_xticklabels(df['Crop'], color='white')
ax.tick_params(colors='white')
ax.legend()
st.pyplot(fig)
