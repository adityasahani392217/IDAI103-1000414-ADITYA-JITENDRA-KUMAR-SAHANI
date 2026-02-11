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

# VIBRANT FARMING THEME CSS
st.markdown("""
<style>
    /* 🌈 VIBRANT BACKGROUND GRADIENTS */
    .stApp {
        background: linear-gradient(135deg, #e6ffe6 0%, #f0fff0 25%, #f5fff5 50%, #e8f8e8 75%, #d4f8d4 100%) !important;
        background-attachment: fixed !important;
    }
    
    /* 🎨 VIBRANT HEADER WITH FARMING PATTERN */
    .header-container {
        background: linear-gradient(90deg, 
            #ff6b6b 0%, 
            #ffa726 20%, 
            #ffd93d 40%, 
            #6bcf7f 60%, 
            #4d96ff 80%, 
            #9d65c9 100%);
        padding: 2.5rem;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        margin-bottom: 2.5rem;
        color: white;
        text-align: center;
        position: relative;
        overflow: hidden;
        border: 5px solid white;
    }
    
    .header-container::before {
        content: "🌾🌻🌽🌿☀️💧";
        position: absolute;
        top: 10px;
        left: 0;
        right: 0;
        font-size: 2rem;
        opacity: 0.3;
        animation: float 10s infinite linear;
    }
    
    @keyframes float {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
    
    .title-text {
        font-size: 4rem !important;
        font-weight: 900 !important;
        margin-bottom: 0.5rem !important;
        background: linear-gradient(45deg, #ffffff, #ffffe0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 3px 3px 6px rgba(0, 0, 0, 0.3);
        position: relative;
        z-index: 1;
    }
    
    .subtitle-text {
        font-size: 1.5rem !important;
        font-weight: 600 !important;
        background: linear-gradient(45deg, #ffffff, #e0ffe0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
        position: relative;
        z-index: 1;
    }
    
    /* 🌿 SIDEBAR - FARM FIELD DESIGN */
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, 
            #1a5276 0%, 
            #2e7d32 30%, 
            #27ae60 70%, 
            #2ecc71 100%);
        background-image: radial-gradient(circle at 20% 80%, rgba(255, 255, 255, 0.1) 2px, transparent 10px),
                         radial-gradient(circle at 80% 20%, rgba(255, 255, 255, 0.1) 2px, transparent 10px);
        color: white;
        border-right: 5px solid #ffd700;
    }
    
    .sidebar-header {
        background: rgba(255, 255, 255, 0.15);
        padding: 1.2rem;
        border-radius: 15px;
        margin-bottom: 1.5rem;
        border-left: 5px solid #ffd700;
        backdrop-filter: blur(10px);
        border: 2px solid rgba(255, 255, 255, 0.2);
    }
    
    /* 🎪 VIBRANT INPUT STYLING */
    div[data-baseweb="select"] > div {
        border-radius: 12px !important;
        border: 3px solid #ff6b6b !important;
        background: linear-gradient(135deg, #ffffff, #ffe6e6) !important;
        transition: all 0.3s ease !important;
    }
    
    div[data-baseweb="select"] > div:hover {
        border-color: #ff3838 !important;
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(255, 107, 107, 0.4) !important;
    }
    
    div[data-baseweb="input"] > div {
        border-radius: 12px !important;
        border: 3px solid #4d96ff !important;
        background: linear-gradient(135deg, #ffffff, #e6f0ff) !important;
        transition: all 0.3s ease !important;
    }
    
    div[data-baseweb="input"] > div:hover {
        border-color: #2d7dff !important;
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(77, 150, 255, 0.4) !important;
    }
    
    /* 🌈 COLORFUL MULTISELECT */
    div[data-baseweb="multiselect"] > div {
        border-radius: 12px !important;
        border: 3px solid #6bcf7f !important;
        background: linear-gradient(135deg, #ffffff, #e6ffe6) !important;
    }
    
    /* 🎯 VIBRANT SLIDER */
    .stSlider > div > div {
        background: linear-gradient(90deg, #ff6b6b, #ffa726, #ffd93d, #6bcf7f, #4d96ff) !important;
        border-radius: 10px;
        height: 10px !important;
    }
    
    .stSlider > div > div > div {
        background-color: #ffffff !important;
        border: 3px solid #9d65c9 !important;
        box-shadow: 0 0 10px rgba(157, 101, 201, 0.8) !important;
    }
    
    /* 🚀 GLOWING BUTTONS */
    .stButton > button {
        background: linear-gradient(90deg, 
            #ff6b6b 0%, 
            #ffa726 25%, 
            #6bcf7f 50%, 
            #4d96ff 75%, 
            #9d65c9 100%) !important;
        color: white !important;
        border: none !important;
        padding: 1rem 2rem !important;
        border-radius: 15px !important;
        font-weight: 700 !important;
        font-size: 1.2rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 5px 20px rgba(0, 0, 0, 0.3) !important;
        position: relative !important;
        overflow: hidden !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.02) !important;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.4) !important;
        animation: pulse 1.5s infinite !important;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.3) 0%, transparent 70%);
        opacity: 0;
        transition: opacity 0.3s;
    }
    
    .stButton > button:hover::before {
        opacity: 1;
    }
    
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(255, 107, 107, 0.7); }
        70% { box-shadow: 0 0 0 15px rgba(255, 107, 107, 0); }
        100% { box-shadow: 0 0 0 0 rgba(255, 107, 107, 0); }
    }
    
    /* 🎨 VIBRANT TABS */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: linear-gradient(90deg, #ff6b6b, #ffa726, #6bcf7f, #4d96ff);
        padding: 10px;
        border-radius: 15px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 60px;
        white-space: pre-wrap;
        background: rgba(255, 255, 255, 0.9) !important;
        border-radius: 10px !important;
        color: #2e7d32 !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        border: 2px solid transparent !important;
        transition: all 0.3s ease !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: white !important;
        color: #ff6b6b !important;
        border: 2px solid #ff6b6b !important;
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(255, 107, 107, 0.3) !important;
    }
    
    /* 💎 3D CARDS */
    .recommendation-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8f8f8 100%);
        border-radius: 20px;
        padding: 2rem;
        margin: 1.5rem 0;
        border-left: 8px solid;
        box-shadow: 
            0 10px 20px rgba(0, 0, 0, 0.1),
            inset 0 1px 0 rgba(255, 255, 255, 0.8);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        position: relative;
        overflow: hidden;
    }
    
    .recommendation-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 5px;
        background: linear-gradient(90deg, #ff6b6b, #ffa726, #6bcf7f, #4d96ff, #9d65c9);
    }
    
    .recommendation-card:hover {
        transform: translateY(-10px) rotateX(5deg);
        box-shadow: 
            0 20px 40px rgba(0, 0, 0, 0.2),
            0 0 0 1px rgba(255, 255, 255, 0.1),
            inset 0 1px 0 rgba(255, 255, 255, 0.9);
    }
    
    .recommendation-card h4 {
        color: #2e7d32 !important;
        font-size: 1.5rem !important;
        font-weight: 800 !important;
        margin-bottom: 1rem !important;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    /* 🎪 CHAT MESSAGES - BLACK TEXT ENSURED */
    .user-message {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        padding: 1.2rem;
        border-radius: 20px 20px 5px 20px;
        margin: 1rem 0;
        border: 2px solid #2196f3;
        box-shadow: 0 4px 15px rgba(33, 150, 243, 0.2);
        position: relative;
        max-width: 80%;
        margin-left: auto;
    }
    
    .user-message::after {
        content: "👤";
        position: absolute;
        right: -40px;
        top: 50%;
        transform: translateY(-50%);
        font-size: 1.5rem;
    }
    
    .ai-message {
        background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
        padding: 1.2rem;
        border-radius: 20px 20px 20px 5px;
        margin: 1rem 0;
        border: 2px solid #4caf50;
        box-shadow: 0 4px 15px rgba(76, 175, 80, 0.2);
        position: relative;
        max-width: 80%;
    }
    
    .ai-message::before {
        content: "🌱";
        position: absolute;
        left: -40px;
        top: 50%;
        transform: translateY(-50%);
        font-size: 1.5rem;
    }
    
    /* 🎯 FORCE BLACK TEXT IN CHAT */
    .user-message p,
    .ai-message p,
    .user-message strong,
    .ai-message strong,
    .user-message div,
    .ai-message div,
    .user-message span,
    .ai-message span {
        color: #000000 !important;
        font-weight: 500 !important;
        line-height: 1.6 !important;
        margin: 0 !important;
    }
    
    .user-message strong,
    .ai-message strong {
        color: #000000 !important;
        font-weight: 700 !important;
    }
    
    /* 💬 CHAT CONTAINER */
    .chat-container {
        max-height: 500px;
        overflow-y: auto;
        padding: 1.5rem;
        border-radius: 20px;
        background: linear-gradient(135deg, #f9fdf9 0%, #e8f5e9 100%);
        border: 3px solid #4caf50;
        box-shadow: inset 0 2px 10px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
    }
    
    /* ✨ GLOWING BADGES */
    .badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 25px;
        font-size: 0.9rem;
        font-weight: 700;
        margin: 0.3rem;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;
        border: 2px solid white;
    }
    
    .badge-primary {
        background: linear-gradient(135deg, #ff6b6b, #ff8e53);
        color: white;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
    }
    
    .badge-secondary {
        background: linear-gradient(135deg, #4d96ff, #6bcf7f);
        color: white;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
    }
    
    .badge:hover {
        transform: translateY(-3px) scale(1.05);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
    }
    
    /* 📊 DATA TABLE STYLING */
    .dataframe {
        border-radius: 15px !important;
        overflow: hidden !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15) !important;
        border: 3px solid #4caf50 !important;
        background: white !important;
    }
    
    .dataframe th {
        background: linear-gradient(135deg, #4caf50, #2e7d32) !important;
        color: white !important;
        font-weight: 700 !important;
        text-align: center !important;
    }
    
    .dataframe td {
        color: #333333 !important;
        font-weight: 500 !important;
    }
    
    /* 🎭 FEEDBACK CHECKBOXES */
    .stCheckbox > label {
        font-weight: 600 !important;
        padding: 0.8rem !important;
        border-radius: 10px !important;
        transition: all 0.3s ease !important;
        background: linear-gradient(135deg, #f5f5f5, #ffffff) !important;
        border: 2px solid #e0e0e0 !important;
        margin: 0.5rem 0 !important;
    }
    
    .stCheckbox > label:hover {
        background: linear-gradient(135deg, #e3f2fd, #f3e5f5) !important;
        border-color: #9d65c9 !important;
        transform: translateX(5px);
    }
    
    /* 🌟 SUCCESS/ERROR MESSAGES */
    .stSuccess {
        background: linear-gradient(135deg, #e8f5e9, #c8e6c9) !important;
        border-radius: 15px !important;
        border-left: 8px solid #4caf50 !important;
        padding: 1rem !important;
        border: 2px solid #4caf50 !important;
        color: #1b5e20 !important;
        font-weight: 600 !important;
    }
    
    .stError {
        background: linear-gradient(135deg, #ffebee, #ffcdd2) !important;
        border-radius: 15px !important;
        border-left: 8px solid #f44336 !important;
        padding: 1rem !important;
        border: 2px solid #f44336 !important;
        color: #b71c1c !important;
        font-weight: 600 !important;
    }
    
    .stWarning {
        background: linear-gradient(135deg, #fff3e0, #ffe0b2) !important;
        border-radius: 15px !important;
        border-left: 8px solid #ff9800 !important;
        padding: 1rem !important;
        border: 2px solid #ff9800 !important;
        color: #e65100 !important;
        font-weight: 600 !important;
    }
    
    /* 🎪 FOOTER DESIGN */
    .footer {
        text-align: center;
        margin-top: 3rem;
        padding: 2rem;
        background: linear-gradient(90deg, 
            #ff6b6b 0%, 
            #ffa726 25%, 
            #6bcf7f 50%, 
            #4d96ff 75%, 
            #9d65c9 100%);
        border-radius: 20px;
        border-top: 5px solid white;
        color: white;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .footer::before {
        content: "🌱🌾🌻🌽🍅🥕";
        position: absolute;
        top: 10px;
        left: 0;
        right: 0;
        font-size: 1.5rem;
        opacity: 0.3;
        animation: float 15s infinite linear reverse;
    }
    
    /* 📱 RESPONSIVE DESIGN */
    @media (max-width: 768px) {
        .title-text {
            font-size: 2.5rem !important;
        }
        
        .recommendation-card {
            padding: 1.5rem;
        }
        
        .chat-container {
            max-height: 300px;
        }
    }
    
    /* 🔥 SPECIAL EFFECTS */
    .sparkle {
        animation: sparkle 2s infinite;
    }
    
    @keyframes sparkle {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    /* 🎨 COLORFUL TEXT CLASSES */
    .rainbow-text {
        background: linear-gradient(90deg, 
            #ff6b6b, #ffa726, #ffd93d, #6bcf7f, #4d96ff, #9d65c9);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
    }
    
    /* 💫 ALL TEXT IN BLACK (except headers) */
    p, div:not(.header-container):not(.sidebar-header):not(.title-text):not(.subtitle-text):not(.badge):not(.stButton > button):not(.stTabs [data-baseweb="tab"]):not(.footer) {
        color: #000000 !important;
    }
    
    .ai-content {
        color: #000000 !important;
        line-height: 1.8 !important;
        font-size: 1.1rem !important;
        font-weight: 500 !important;
    }
    
    .insight-text {
        color: #000000 !important;
        line-height: 1.8 !important;
        font-weight: 500 !important;
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
    <p style="opacity: 0.9; margin-bottom: 0; font-size: 1.1rem; text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">
        🚀 Transform Your Farming with AI • 🌈 Colorful Experience • 💡 Smart Insights
    </p>
</div>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.markdown('<div class="sidebar-header">', unsafe_allow_html=True)
    st.markdown("### 🌍 Farm Configuration")
    st.markdown('<p style="color: #ffd700; font-size: 0.9rem;">Customize your farming experience</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Farm Region with icon
    region = st.selectbox(
        "**🌎 Select Region**",
        ["India", "Ghana", "Canada", "USA", "Australia", "Brazil", "Kenya", "France"],
        help="Choose your country for region-specific advice"
    )
    
    # Location
    location = st.text_input(
        "**📍 Enter Location**",
        placeholder="e.g., Punjab, Maharashtra, Ontario...",
        help="State or province for localized recommendations"
    )
    
    # Crop Stage with vibrant icons
    crop_stage_options = {
        "Planning": "📋 Planning Phase",
        "Sowing": "🌱 Sowing Season",
        "Growing": "🌿 Growth Period",
        "Harvesting": "🌾 Harvest Time",
        "Post-Harvest": "🏭 Post-Harvest"
    }
    crop_stage = st.selectbox(
        "**🌱 Crop Stage**",
        list(crop_stage_options.keys()),
        format_func=lambda x: crop_stage_options[x]
    )
    
    # Priorities with icons
    priority = st.multiselect(
        "**🎯 Your Farming Priorities**",
        ["💧 Low Water Use", "📈 High Yield", "🌿 Organic Farming", "💰 Low Cost", 
         "🛡️ Pest Resistance", "🌱 Soil Health", "🚜 Automation", "♻️ Sustainability"],
        default=["📈 High Yield"],
        help="Select your primary farming objectives"
    )
    
    # AI Creativity with vibrant slider
    st.markdown("**🤖 AI Creativity Level**")
    temperature = st.slider(
        "Creativity Level",
        0.2,
        0.9,
        0.5,
        help="Lower = More Consistent, Higher = More Creative",
        label_visibility="collapsed"
    )
    
    # Visual creativity indicator
    creativity_percent = int((temperature - 0.2) / 0.7 * 100)
    st.markdown(f"""
    <div style="display: flex; justify-content: space-between; margin-top: -10px; color: white;">
        <small>🎯 Consistent</small>
        <small>🎨 Creative</small>
    </div>
    <div class="creativity-level" style="width: {creativity_percent}%"></div>
    <div style="text-align: center; margin-top: 10px;">
        <span style="color: #ffd700; font-weight: 700; font-size: 1.1rem;">
            🎭 {creativity_percent}% Creativity Mode
        </span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 📊 Current Session")
    
    # Show current selections as badges
    badge_col1, badge_col2 = st.columns(2)
    with badge_col1:
        if location:
            st.markdown(f'<span class="badge badge-primary">📍 {location[:15]}</span>', unsafe_allow_html=True)
        st.markdown(f'<span class="badge badge-secondary">{crop_stage_options[crop_stage][:3]}</span>', unsafe_allow_html=True)
    
    with badge_col2:
        for p in priority[:2]:
            st.markdown(f'<span class="badge badge-primary">{p[:10]}</span>', unsafe_allow_html=True)

# ---------------- INITIALIZE SESSION STATE ----------------
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'full_output' not in st.session_state:
    st.session_state.full_output = None
if 'show_recommendations' not in st.session_state:
    st.session_state.show_recommendations = False

# ---------------- MAIN CONTENT AREA ----------------
tab1, tab2 = st.tabs(["🌾 **Get Smart Recommendations**", "💬 **Ask Farming Questions**"])

with tab1:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 💡 Generate AI-Powered Farming Advice")
        st.markdown('<p class="insight-text">Click below to get personalized recommendations based on your farm configuration.</p>', unsafe_allow_html=True)
        
        # Action button with enhanced styling
        if st.button("🚀 Generate Smart Recommendations", use_container_width=True, key="generate_btn"):
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
                        
                        # Store in session state to display later
                        st.session_state.full_output = full_output
                        st.session_state.show_recommendations = True
                        
                except Exception as e:
                    st.error("⚠️ Service Temporarily Unavailable")
                    with st.expander("Technical Details"):
                        st.code(str(e))
        
        # Display recommendations from session state
        if 'show_recommendations' in st.session_state and st.session_state.show_recommendations:
            if 'full_output' in st.session_state and st.session_state.full_output:
                full_output = st.session_state.full_output
                st.success("✅ AI Recommendations Generated Successfully!")
                st.markdown("---")
                st.markdown("### 📋 Your Personalized Farming Plan")
                
                # Split recommendations and display in cards
                recommendations = full_output.split('\n\n')
                for i, rec in enumerate(recommendations[:3], 1):
                    if rec.strip():
                        # Clean up the text
                        cleaned_rec = rec.replace('•', '➤').replace('Recommendation', '').strip()
                        icon = "✨" if i == 1 else "🚀" if i == 2 else "💎"
                        st.markdown(f"""
                        <div class="recommendation-card">
                            <h4>{icon} Recommendation {i}</h4>
                            <div class="ai-content">
                                {cleaned_rec}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 📈 Farm Insights Dashboard")
        
        # Current farm status card
        creativity_label = "🎨 Creative" if temperature > 0.6 else "⚖️ Balanced" if temperature > 0.4 else "🎯 Conservative"
        
        st.markdown(f"""
        <div class="recommendation-card">
            <h4>🏡 Current Farm Status</h4>
            <p class="farm-data-text"><strong>🌎 Region:</strong> {region}</p>
            <p class="farm-data-text"><strong>🌱 Stage:</strong> {crop_stage}</p>
            <p class="farm-data-text"><strong>🎯 Priorities:</strong> {len(priority)} selected</p>
            <p class="farm-data-text"><strong>🤖 AI Mode:</strong> {creativity_label}</p>
            <div style="margin-top: 1rem; padding: 0.5rem; background: linear-gradient(135deg, #e3f2fd, #f3e5f5); border-radius: 10px;">
                <small>📍 <strong>Location:</strong> {location if location else "Not specified"}</small>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Best practices tip
        st.markdown("""
        <div class="recommendation-card">
            <h4>💡 Pro Farming Tip</h4>
            <p class="insight-text">For best results, ensure your location is specific (state/province level) and priorities reflect your actual farming goals.</p>
            <small class="insight-text" style="display: block; margin-top: 0.5rem;">
                🌟 <strong>Tip:</strong> AI recommendations improve with accurate inputs and detailed context about your farm conditions.
            </small>
        </div>
        """, unsafe_allow_html=True)
        
        # Quick stats
        st.markdown("""
        <div class="recommendation-card">
            <h4>📊 Quick Stats</h4>
            <p class="insight-text">🎯 <strong>Active Priorities:</strong> {}</p>
            <p class="insight-text">💬 <strong>Chat Messages:</strong> {}</p>
            <p class="insight-text">🤖 <strong>AI Creativity:</strong> {}%</p>
        </div>
        """.format(
            len(priority),
            len(st.session_state.chat_history),
            creativity_percent
        ), unsafe_allow_html=True)

with tab2:
    st.markdown("### 💬 Ask Farming Questions")
    st.markdown('<p class="insight-text">Chat with FarmaBuddy AI to get instant answers to your specific farming questions.</p>', unsafe_allow_html=True)
    
    # Chat container
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    # Display chat history with black text
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            st.markdown(f"""
            <div class="user-message">
                <p><strong>👤 You:</strong> {message["content"]}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="ai-message">
                <p><strong>🌱 FarmaBuddy:</strong> {message["content"]}</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Chat input with vibrant design
    st.markdown("### 💭 Ask a Question")
    col_chat1, col_chat2 = st.columns([5, 1])
    
    with col_chat1:
        user_question = st.text_input(
            "Type your farming question here:",
            placeholder="e.g., What are the best crops for Punjab in summer? How to control pests organically?",
            label_visibility="collapsed",
            key="chat_input"
        )
    
    with col_chat2:
        send_button = st.button("🚀 Send", use_container_width=True, key="send_btn")
    
    # Handle chat submission
    if send_button and user_question:
        # Add user message to chat history
        st.session_state.chat_history.append({"role": "user", "content": user_question})
        
        try:
            with st.spinner("🌱 AI is thinking..."):
                # Build context-aware prompt
                context_prompt = f"""
                You are FarmaBuddy, a helpful farming assistant.
                
                Current Farmer Context:
                - Region: {region}
                - Location: {location}
                - Crop Stage: {crop_stage}
                - Priorities: {', '.join(priority) if priority else 'General farming'}
                
                User Question: {user_question}
                
                Instructions:
                - Provide a clear, practical answer
                - Consider the farmer's context above
                - Keep response concise but informative
                - Use simple language
                - Focus on actionable advice
                - If the question is outside farming, politely redirect
                """
                
                # Get AI response
                response = client.models.generate_content(
                    model="gemini-3-flash-preview",
                    contents=context_prompt,
                    config={
                        "temperature": temperature,
                        "max_output_tokens": 1024
                    }
                )
                
                # Extract AI response
                if hasattr(response, "text") and response.text:
                    ai_response = response.text
                elif hasattr(response, "candidates"):
                    try:
                        ai_response = response.candidates[0].content.parts[0].text
                    except:
                        ai_response = "I apologize, but I'm having trouble generating a response. Please try again."
                else:
                    ai_response = "I apologize, but I'm having trouble generating a response. Please try again."
                
                # Add AI response to chat history
                st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
                
                # Rerun to update the chat display
                st.rerun()
                
        except Exception as e:
            error_msg = "Sorry, I'm having trouble connecting to the AI service. Please try again later."
            st.session_state.chat_history.append({"role": "assistant", "content": error_msg})
            st.rerun()
    
    # Clear chat button
    if st.session_state.chat_history:
        col_clear1, col_clear2, col_clear3 = st.columns([1, 2, 1])
        with col_clear2:
            if st.button("🗑️ Clear Chat History", use_container_width=True, key="clear_chat"):
                st.session_state.chat_history = []
                st.rerun()

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
    if st.button("📤 Submit Feedback", use_container_width=True, key="feedback_btn"):
        score = sum([feedback1, feedback2, feedback3, feedback4, feedback5])
        st.balloons()
        st.success(f"🎉 Thank you! Feedback recorded: {score}/5 stars ⭐")

# ---------------- USAGE LOG ----------------
st.markdown("---")
st.markdown("### 📊 Session Log")

log_data = {
    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "Region": region,
    "Location": location or "Not specified",
    "Crop Stage": crop_stage,
    "Priorities": ", ".join(priority) if priority else "General",
    "AI Creativity": f"{creativity_percent}%",
    "Chat Messages": len(st.session_state.chat_history),
    "Status": "Active"
}

# Display log in a nice dataframe
df_log = pd.DataFrame([log_data])
st.dataframe(df_log, use_container_width=True, hide_index=True)

# ---------------- FOOTER ----------------
st.markdown("""
<div class="footer">
    <div style="display: flex; justify-content: center; align-items: center; gap: 15px; margin-bottom: 15px; flex-wrap: wrap;">
        <span style="font-size: 2rem;">🌱</span>
        <span style="font-weight: 800; font-size: 1.5rem; color: white; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">
            FarmaBuddy AI Assistant
        </span>
        <span style="font-size: 2rem;">🌾</span>
    </div>
    <p style="margin: 0; color: white; font-size: 1rem; font-weight: 600;">
        FA-2 Project • 2026 • Empowering Farmers with AI Technology
    </p>
    <p style="margin: 0; color: rgba(255,255,255,0.9); font-size: 0.9rem; margin-top: 5px;">
        🚀 Built with Gemini AI • 🌈 Colorful UI/UX • 💡 Smart Farming Solutions
    </p>
    <p style="margin: 0; color: rgba(255,255,255,0.8); font-size: 0.8rem; margin-top: 10px;">
        Last Updated: {current_date} | Session ID: {session_id}
    </p>
</div>
""".format(
    current_date=datetime.now().strftime("%B %d, %Y"),
    session_id=datetime.now().strftime("%Y%m%d%H%M%S")
), unsafe_allow_html=True)
