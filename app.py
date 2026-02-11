import streamlit as st
import pandas as pd
from datetime import datetime
from google import genai

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="FarmaBuddy 🌱",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for enhanced UI
st.markdown("""
<style>
    /* Main container styling */
    .main {
        background: linear-gradient(135deg, #f5fff0 0%, #e8f5e8 100%);
    }
    
    /* Header styling */
    .header-container {
        background: linear-gradient(90deg, #2e7d32 0%, #4caf50 100%);
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(76, 175, 80, 0.15);
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }
    
    .title-text {
        font-size: 3.5rem !important;
        font-weight: 800 !important;
        margin-bottom: 0.5rem !important;
        background: linear-gradient(45deg, #ffffff, #e8f5e9);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    .subtitle-text {
        font-size: 1.3rem !important;
        opacity: 0.9;
        margin-bottom: 0.5rem !important;
    }
    
    /* Sidebar styling */
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #1b5e20 0%, #2e7d32 100%);
        color: white;
    }
    
    .sidebar-header {
        background: rgba(255, 255, 255, 0.1);
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1.5rem;
        border-left: 4px solid #81c784;
    }
    
    /* Input styling */
    .stSelectbox, .stTextInput, .stMultiselect, .stSlider {
        margin-bottom: 1.5rem !important;
    }
    
    div[data-baseweb="select"] > div {
        border-radius: 10px !important;
        border: 2px solid #c8e6c9 !important;
    }
    
    div[data-baseweb="input"] > div {
        border-radius: 10px !important;
        border: 2px solid #c8e6c9 !important;
    }
    
    /* Button styling */
    .stButton > button {
        width: 100%;
        background: linear-gradient(90deg, #4caf50 0%, #2e7d32 100%);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 12px;
        font-weight: 600;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(76, 175, 80, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(76, 175, 80, 0.4);
    }
    
    /* Card styling for recommendations */
    .recommendation-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 5px solid #4caf50;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
        transition: transform 0.3s ease;
    }
    
    .recommendation-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.12);
    }
    
    /* Badge styling */
    .badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        margin: 0.25rem;
    }
    
    .badge-primary {
        background: #e8f5e9;
        color: #2e7d32;
        border: 1px solid #a5d6a7;
    }
    
    .badge-secondary {
        background: #f1f8e9;
        color: #558b2f;
        border: 1px solid #c5e1a5;
    }
    
    /* Progress bar for creativity level */
    .creativity-level {
        background: linear-gradient(90deg, #c8e6c9 0%, #4caf50 100%);
        height: 8px;
        border-radius: 4px;
        margin-top: 0.5rem;
    }
    
    /* Footer styling */
    .footer {
        text-align: center;
        margin-top: 3rem;
        padding: 1.5rem;
        background: linear-gradient(90deg, #f1f8e9 0%, #e8f5e9 100%);
        border-radius: 15px;
        border-top: 3px solid #4caf50;
    }
    
    /* Checkbox styling */
    .stCheckbox > label {
        font-weight: 500;
        padding: 0.5rem;
        border-radius: 8px;
        transition: all 0.3s ease;
    }
    
    .stCheckbox > label:hover {
        background: #f1f8e9;
    }
    
    /* Dataframe styling */
    .dataframe {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
    }
    
    /* Success message styling */
    .stSuccess {
        border-radius: 10px;
        border-left: 5px solid #4caf50;
    }
    
    /* Error message styling */
    .stError {
        border-radius: 10px;
        border-left: 5px solid #f44336;
    }
</style>
""", unsafe_allow_html=True)

# ---------------- API KEY & CLIENT ----------------
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("🔐 API Key Missing - Please add GOOGLE_API_KEY to Streamlit Secrets")
    st.stop()

api_key = st.secrets["GOOGLE_API_KEY"]
client = genai.Client(api_key=api_key)

# ---------------- HEADER ----------------
st.markdown("""
<div class="header-container">
    <h1 class="title-text">🌱 FarmaBuddy</h1>
    <h4 class="subtitle-text">AI-Powered Smart Farming Assistant</h4>
    <p style="opacity: 0.8; margin-bottom: 0;">Built with Gemini AI • Deployed on Streamlit Cloud</p>
</div>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.markdown('<div class="sidebar-header">', unsafe_allow_html=True)
    st.markdown("### 🌍 Farm Configuration")
    st.markdown("Configure your farm details for personalized recommendations")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Farm Region
    region = st.selectbox(
        "**Select Region**",
        ["India", "Ghana", "Canada"],
        help="Choose your country for region-specific advice"
    )
    
    # Location
    location = st.text_input(
        "**Enter Location**",
        placeholder="e.g., Punjab, Maharashtra, Ontario...",
        help="State or province for localized recommendations"
    )
    
    # Crop Stage with icons
    crop_stage_options = {
        "Planning": "📋 Planning",
        "Sowing": "🌱 Sowing",
        "Growing": "🌿 Growing",
        "Harvesting": "🌾 Harvesting"
    }
    crop_stage = st.selectbox(
        "**Crop Stage**",
        list(crop_stage_options.keys()),
        format_func=lambda x: crop_stage_options[x]
    )
    
    # Priorities
    priority = st.multiselect(
        "**Your Farming Priorities**",
        ["Low Water Use", "High Yield", "Organic Farming", "Low Cost"],
        default=["High Yield"],
        help="Select your primary farming objectives"
    )
    
    # AI Creativity
    st.markdown("**🤖 AI Creativity Level**")
    temperature = st.slider(
        "",
        0.2,
        0.9,
        0.5,
        help="Lower = More Consistent, Higher = More Creative",
        label_visibility="collapsed"
    )
    
    # Visual creativity indicator
    creativity_percent = int((temperature - 0.2) / 0.7 * 100)
    st.markdown(f"""
    <div style="display: flex; justify-content: space-between; margin-top: -10px;">
        <small>Consistent</small>
        <small>Creative</small>
    </div>
    <div class="creativity-level" style="width: {creativity_percent}%"></div>
    <div style="text-align: center; margin-top: 5px; color: #4caf50; font-weight: 600;">
        {creativity_percent}% Creativity
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 📊 Current Session")
    
    # Show current selections as badges
    if location:
        st.markdown(f'<span class="badge badge-primary">📍 {location}</span>', unsafe_allow_html=True)
    st.markdown(f'<span class="badge badge-secondary">{crop_stage_options[crop_stage]}</span>', unsafe_allow_html=True)
    
    for p in priority:
        st.markdown(f'<span class="badge badge-primary">🎯 {p}</span>', unsafe_allow_html=True)

# ---------------- MAIN CONTENT AREA ----------------
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 💡 Get AI-Powered Farming Advice")
    
    # Action button with enhanced styling
    if st.button("🚀 Generate Smart Recommendations", use_container_width=True):
        if not location:
            st.warning("📍 Please enter your location to get personalized recommendations")
        else:
            try:
                with st.spinner("🤖 AI is analyzing your farm data..."):
                    # Build prompt
                    prompt = f"""
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
                    
                    # Get AI response
                    response = client.models.generate_content(
                        model="gemini-3-flash-preview",
                        contents=prompt,
                        config={
                            "temperature": temperature,
                            "max_output_tokens": 1024
                        }
                    )
                    
                    # Extract response
                    if hasattr(response, "text") and response.text:
                        full_output = response.text
                    elif hasattr(response, "candidates"):
                        try:
                            full_output = response.candidates[0].content.parts[0].text
                        except:
                            full_output = "⚠️ Could not parse full response."
                    else:
                        full_output = "⚠️ No content returned."
                    
                    # Display recommendations in cards
                    st.success("✅ AI Recommendations Generated Successfully!")
                    st.markdown("---")
                    st.markdown("### 📋 Your Personalized Farming Plan")
                    
                    # Split recommendations and display in cards
                    recommendations = full_output.split('\n\n')
                    for i, rec in enumerate(recommendations[:3], 1):
                        if rec.strip():
                            st.markdown(f"""
                            <div class="recommendation-card">
                                <h4>📌 Recommendation {i}</h4>
                                {rec.replace('•', '➤').replace('Recommendation', '').strip()}
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        # Fallback display
                        st.markdown(f"""
                        <div class="recommendation-card">
                            <h4>📋 AI Recommendations</h4>
                            {full_output}
                        </div>
                        """, unsafe_allow_html=True)
                    
            except Exception as e:
                st.error("⚠️ Service Temporarily Unavailable")
                with st.expander("Technical Details"):
                    st.code(str(e))

# In the CSS section, add these specific styles:
# In the CSS section, add these styles:
st.markdown("""
<style>
    /* Make all farm data, insights, and recommendations text black */
    .farm-data-text, .insight-text, .data-text, .recommendation-text {
        color: #000000 !important;
        font-weight: 500;
    }
    
    /* Make all text inside recommendation cards black */
    .recommendation-card p,
    .recommendation-card li,
    .recommendation-card div,
    .recommendation-card span:not(.badge) {
        color: #000000 !important;
    }
    
    /* Specifically target AI recommendation content */
    .ai-recommendations-content {
        color: #000000 !important;
    }
    
    /* Target the farm insights sections */
    .farm-insights-section p,
    .farm-insights-section strong {
        color: #000000 !important;
    }
    
    /* Make pro tip text black */
    .pro-tip-section p,
    .pro-tip-section small {
        color: #000000 !important;
    }
    
    /* Keep headers green but content black */
    .recommendation-card h4 {
        color: #2e7d32 !important;
    }
</style>
""", unsafe_allow_html=True)

# Update the farm insights section with new classes:
with col2:
    st.markdown("### 📈 Farm Insights")
    
    # Current farm status card - UPDATED
    st.markdown(f"""
    <div class="recommendation-card farm-status-card farm-insights-section" style="background: linear-gradient(135deg, #e8f5e9 0%, #f1f8e9 100%);">
        <h4 style="color: #2e7d32;">🏡 Current Farm Status</h4>
        <p class="farm-data-text"><strong>Region:</strong> {region}</p>
        <p class="farm-data-text"><strong>Stage:</strong> {crop_stage}</p>
        <p class="farm-data-text"><strong>Priorities:</strong> {len(priority)}</p>
        <p class="farm-data-text"><strong>AI Mode:</strong> {"Creative" if temperature > 0.6 else "Balanced" if temperature > 0.4 else "Conservative"}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Best practices tip - UPDATED
    st.markdown("""
    <div class="recommendation-card pro-tip-card pro-tip-section" style="background: linear-gradient(135deg, #f1f8e9 0%, #e8f5e9 100%);">
        <h4 style="color: #2e7d32;">💡 Pro Tip</h4>
        <p class="insight-text">For best results, ensure your location is specific (state/province level) and priorities reflect your actual farming goals.</p>
        <small class="insight-text">AI recommendations improve with accurate inputs.</small>
    </div>
    """, unsafe_allow_html=True)

# Update the AI recommendations display section in the button action:
# Replace this section:
st.markdown("### 📋 Your Personalized Farming Plan")

# Split recommendations and display in cards
recommendations = full_output.split('\n\n')
for i, rec in enumerate(recommendations[:3], 1):
    if rec.strip():
        st.markdown(f"""
        <div class="recommendation-card">
            <h4 style="color: #2e7d32;">📌 Recommendation {i}</h4>
            <div class="recommendation-text ai-recommendations-content">
                {rec.replace('•', '➤').replace('Recommendation', '').strip()}
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
    # Fallback display
        st.markdown(f"""
        <div class="recommendation-card">
            <h4 style="color: #2e7d32;">📋 AI Recommendations</h4>
            <div class="recommendation-text ai-recommendations-content">
                {full_output}
            </div>
        </div>
        """, unsafe_allow_html=True)

# Also update the alternative display path:
else:
    st.markdown(f"""
    <div class="recommendation-card">
        <h4 style="color: #2e7d32;">📋 AI Recommendations</h4>
        <div class="recommendation-text ai-recommendations-content">
            {full_output}
        </div>
    </div>
    """, unsafe_allow_html=True)
# Update the usage log section:

# ---------------- FEEDBACK SECTION ----------------
st.markdown("---")
st.markdown("### ✅ Quality Assurance")

# Feedback in columns
col_fb1, col_fb2, col_fb3 = st.columns(3)

with col_fb1:
    feedback1 = st.checkbox("✅ Region-specific advice", help="Advice tailored to your region")
    feedback2 = st.checkbox("✅ Logical reasoning", help="Clear explanations provided")

with col_fb2:
    feedback3 = st.checkbox("✅ Simple language", help="Easy to understand terms")
    feedback4 = st.checkbox("✅ Actionable steps", help="Practical implementation guidance")

with col_fb3:
    feedback5 = st.checkbox("✅ Safe & ethical", help="No unsafe recommendations")
    if st.button("📤 Submit Feedback", use_container_width=True):
        score = sum([feedback1, feedback2, feedback3, feedback4, feedback5])
        st.balloons()
        st.success(f"Thank you! Feedback recorded: {score}/5 stars ⭐")

# ---------------- USAGE LOG ----------------
st.markdown("---")
st.markdown("### 📊 Session Log")
st.markdown('<p class="usage-log-text">Current session activity and configuration:</p>', unsafe_allow_html=True)

log_data = {
    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "Region": region,
    "Location": location or "Not specified",
    "Crop Stage": crop_stage,
    "Priorities": ", ".join(priority) if priority else "General",
    "AI Creativity": f"{creativity_percent}%"
}

# Display log in a nice dataframe
df_log = pd.DataFrame([log_data])
st.dataframe(df_log, use_container_width=True, hide_index=True)

# ---------------- FOOTER ----------------
st.markdown("""
<div class="footer">
    <div style="display: flex; justify-content: center; align-items: center; gap: 10px; margin-bottom: 10px;">
        <span style="color: #4caf50;">🌱</span>
        <span style="font-weight: 600; color: #2e7d32;">FarmaBuddy AI Assistant</span>
        <span style="color: #4caf50;">🌾</span>
    </div>
    <p style="margin: 0; color: #666; font-size: 0.9rem;">
        FA-2 Project • 2026 • Empowering Farmers with AI Technology
    </p>
    <p style="margin: 0; color: #888; font-size: 0.8rem;">
        Last Updated: {current_date}
    </p>
</div>
""".format(current_date=datetime.now().strftime("%B %d, %Y")), unsafe_allow_html=True)
