import streamlit as st
import pandas as pd
from datetime import datetime
from google import genai

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="🌾 FarmaBuddy",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- FONT AWESOME & VIBRANT SOLID COLOR CSS ----------
st.markdown("""
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
<style>
    /* 🎯 GLOBAL RESET - BLACK TEXT FOR ALL CONTENT */
    * {
        font-family: 'Segoe UI', 'Arial', sans-serif;
    }
    p, li, div:not(.header-container):not(.sidebar-header):not(.title-text):not(.subtitle-text):not(.badge):not(.stButton > button):not(.stTabs [data-baseweb="tab"]):not(.footer) {
        color: #000000 !important;
    }
    
    /* 🌈 VIBRANT SOLID COLOR PALETTE */
    :root {
        --primary-green: #2E7D32;
        --primary-orange: #FF8C42;
        --primary-blue: #3A86FF;
        --primary-yellow: #FFBE0B;
        --primary-red: #FF595E;
        --primary-purple: #9B5DE5;
        --light-bg: #F8FFF8;
        --white: #FFFFFF;
        --black: #000000;
    }
    
    .stApp {
        background-color: var(--light-bg);
    }
    
    /* 🌟 HEADER – BIG, BRIGHT, FRIENDLY */
    .header-container {
        background-color: var(--primary-green);
        padding: 2rem 1.5rem;
        border-radius: 30px 30px 30px 0;
        margin-bottom: 2rem;
        border: 6px solid var(--primary-yellow);
        box-shadow: 12px 12px 0 rgba(0,0,0,0.1);
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-wrap: wrap;
    }
    .header-text {
        flex: 2;
    }
    .header-icon {
        flex: 1;
        text-align: center;
        font-size: 5rem;
        color: var(--primary-yellow);
        text-shadow: 6px 6px 0 rgba(0,0,0,0.2);
    }
    .title-text {
        font-size: 3.8rem !important;
        font-weight: 900 !important;
        color: white !important;
        margin-bottom: 0.2rem !important;
        text-shadow: 6px 6px 0 rgba(0,0,0,0.2);
        line-height: 1.2;
    }
    .subtitle-text {
        font-size: 1.6rem !important;
        font-weight: 700 !important;
        color: var(--primary-yellow) !important;
        text-shadow: 3px 3px 0 rgba(0,0,0,0.2);
    }
    
    /* 🧑‍🌾 SIDEBAR – FARM TOOLBAR */
    .sidebar .sidebar-content {
        background-color: var(--primary-green);
        border-right: 8px solid var(--primary-yellow);
    }
    .sidebar-header {
        background-color: var(--primary-yellow);
        padding: 1.2rem;
        border-radius: 20px;
        margin-bottom: 1.5rem;
        border: 4px solid white;
        color: black !important;
        text-align: center;
    }
    .sidebar-header * {
        color: black !important;
    }
    
    /* 🎛️ INPUT FIELDS – BIG & FRIENDLY */
    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] > div,
    div[data-baseweb="multiselect"] > div {
        border-radius: 20px !important;
        border-width: 4px !important;
        background-color: white !important;
        font-size: 1.1rem !important;
        font-weight: 500 !important;
    }
    div[data-baseweb="select"] > div { border-color: var(--primary-orange) !important; }
    div[data-baseweb="input"] > div { border-color: var(--primary-blue) !important; }
    div[data-baseweb="multiselect"] > div { border-color: var(--primary-purple) !important; }
    
    /* 🚜 BUTTONS – JUMBO, PLAYFUL */
    .stButton > button {
        background-color: var(--primary-orange) !important;
        color: white !important;
        border: none !important;
        border-radius: 40px !important;
        padding: 1.2rem 2rem !important;
        font-weight: 800 !important;
        font-size: 1.5rem !important;
        border: 4px solid white !important;
        box-shadow: 8px 8px 0 rgba(0,0,0,0.2) !important;
        transition: all 0.1s ease !important;
        width: 100%;
    }
    .stButton > button:hover {
        transform: translateY(-4px) scale(1.02);
        box-shadow: 12px 12px 0 rgba(0,0,0,0.2) !important;
        background-color: var(--primary-red) !important;
    }
    
    /* 🎴 GIANT CARDS – LIKE FARM POSTERS */
    .recommendation-card {
        background-color: white;
        border-radius: 30px 30px 30px 0;
        padding: 2rem;
        margin: 1.5rem 0;
        border-left: 12px solid var(--primary-green);
        box-shadow: 12px 12px 0 rgba(46,125,50,0.2);
        transition: all 0.2s;
    }
    .recommendation-card:hover {
        transform: translateY(-5px);
        box-shadow: 16px 16px 0 rgba(46,125,50,0.25);
    }
    .recommendation-card h4 {
        color: var(--primary-green) !important;
        font-size: 1.8rem !important;
        font-weight: 800 !important;
        border-bottom: 4px dashed var(--primary-yellow);
        padding-bottom: 0.8rem;
    }
    
    /* 💬 CHAT BUBBLES – CLEAR, BLACK TEXT */
    .user-message, .ai-message {
        padding: 1.2rem 1.8rem;
        border-radius: 40px 40px 40px 0;
        margin: 1rem 0;
        border: 4px solid white;
        box-shadow: 8px 8px 0 rgba(0,0,0,0.1);
        max-width: 85%;
        font-size: 1.1rem;
    }
    .user-message {
        background-color: #D4EDF7;
        border-left: 12px solid var(--primary-blue);
        margin-left: auto;
    }
    .ai-message {
        background-color: #E2F3E2;
        border-left: 12px solid var(--primary-green);
    }
    .user-message p, .ai-message p {
        color: black !important;
        font-weight: 500;
        margin: 0;
    }
    
    /* 🏷️ BADGES – COLORFUL TAGS */
    .badge {
        display: inline-block;
        padding: 0.6rem 1.2rem;
        border-radius: 50px;
        font-size: 1rem;
        font-weight: 700;
        margin: 0.3rem;
        border: 3px solid white;
        box-shadow: 4px 4px 0 rgba(0,0,0,0.1);
        background-color: var(--primary-orange);
        color: white !important;
    }
    .badge i { margin-right: 8px; }
    
    /* 📊 FARM DASHBOARD TILES */
    .farm-tile {
        background-color: white;
        border-radius: 20px;
        padding: 1.5rem;
        border-bottom: 10px solid var(--primary-yellow);
        box-shadow: 8px 8px 0 rgba(0,0,0,0.08);
        text-align: center;
    }
    .farm-tile i {
        font-size: 3rem;
        color: var(--primary-green);
    }
    .farm-tile h3 {
        color: var(--primary-green);
        font-weight: 800;
        margin: 0.5rem 0;
    }
    
    /* 📱 TAB BUTTONS – BIG ICONS */
    .stTabs [data-baseweb="tab-list"] {
        gap: 15px;
        background-color: var(--primary-yellow);
        padding: 15px;
        border-radius: 60px;
        border: 4px solid white;
        box-shadow: 8px 8px 0 rgba(0,0,0,0.1);
        margin-bottom: 1.5rem;
    }
    .stTabs [data-baseweb="tab"] {
        height: 80px;
        background-color: white !important;
        border-radius: 50px !important;
        color: black !important;
        font-weight: 800 !important;
        font-size: 1.3rem !important;
        border: 4px solid var(--primary-green) !important;
        padding: 0 2rem !important;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .stTabs [aria-selected="true"] {
        background-color: var(--primary-green) !important;
        color: white !important;
        border-color: var(--primary-yellow) !important;
    }
    
    /* 🦶 FOOTER – FARM SIGN */
    .footer {
        background-color: var(--primary-green);
        padding: 2rem;
        border-radius: 40px 40px 0 0;
        border-top: 8px solid var(--primary-yellow);
        color: white;
        text-align: center;
        margin-top: 3rem;
    }
    .footer * { color: white !important; }
    
    /* ℹ️ TOOLTIPS – SIMPLE */
    .tooltip-icon {
        font-size: 1.2rem;
        color: var(--primary-yellow);
        margin-left: 5px;
        cursor: help;
    }
</style>
""", unsafe_allow_html=True)

# ---------------- API KEY & CLIENT ----------------
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("🔐 API Key Missing - Please add GOOGLE_API_KEY to Streamlit Secrets")
    st.stop()
api_key = st.secrets["GOOGLE_API_KEY"]
client = genai.Client(api_key=api_key)

# ---------------- HEADER (WITH BIG EMOJI & ICON) ----------------
st.markdown("""
<div class="header-container">
    <div class="header-text">
        <h1 class="title-text">🌱 FarmaBuddy</h1>
        <h4 class="subtitle-text">🤖 AI Farmer Friend</h4>
        <p style="color: white; font-size: 1.3rem; margin-top: 0.5rem;">
            <i class="fas fa-seedling"></i> Smart advice, big harvests  <i class="fas fa-tractor"></i>
        </p>
    </div>
    <div class="header-icon">
        <i class="fas fa-leaf"></i>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR (ICON-FIRST) ----------------
with st.sidebar:
    st.markdown('<div class="sidebar-header">', unsafe_allow_html=True)
    st.markdown("### 🧑‍🌾 **Your Farm Setup**")
    st.markdown("</div>", unsafe_allow_html=True)
    
    # 🌍 Region – with flag icons
    region = st.selectbox(
        "🌎 **Where is your farm?**",
        ["India", "Ghana", "Canada", "USA", "Australia", "Brazil", "Kenya", "France"],
        help="Choose your country"
    )
    
    # 📍 Location – big icon
    location = st.text_input(
        "📍 **State / Province**",
        placeholder="e.g. Punjab, Ontario...",
        help="Your local area"
    )
    
    # 🌱 Crop stage – icon dropdown
    crop_stage_options = {
        "Planning": "📋 Planning",
        "Sowing": "🌱 Sowing",
        "Growing": "🌿 Growing",
        "Harvesting": "🌾 Harvesting",
        "Post-Harvest": "🏭 Storage"
    }
    crop_stage = st.selectbox(
        "🌱 **Crop stage?**",
        list(crop_stage_options.keys()),
        format_func=lambda x: crop_stage_options[x],
        help="What's happening now?"
    )
    
    # 🎯 Priorities – with colorful icons
    priority = st.multiselect(
        "🎯 **Your goals**",
        ["💧 Save Water", "📈 High Yield", "🌿 Organic", "💰 Low Cost", 
         "🛡️ Pest Control", "🌱 Soil Health", "🚜 Automation", "♻️ Sustainability"],
        default=["📈 High Yield"],
        help="Pick what matters most"
    )
    
    # 🤖 AI creativity – big slider
    st.markdown("**🤖 AI Creativity**")
    temperature = st.slider(
        "creativity", 0.2, 0.9, 0.5, 
        label_visibility="collapsed",
        help="More creative = surprising ideas, Consistent = safe advice"
    )
    creativity_percent = int((temperature - 0.2) / 0.7 * 100)
    st.markdown(f"""
    <div style="background: #FFBE0B; padding: 0.8rem; border-radius: 30px; text-align: center; border: 4px solid white;">
        <span style="font-weight:800; font-size:1.4rem; color:black;">✨ {creativity_percent}% creative</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 📋 **Your summary**")
    # Show badges with icons
    cols = st.columns(2)
    with cols[0]:
        if location:
            st.markdown(f'<span class="badge"><i class="fas fa-map-marker-alt"></i> {location[:10]}</span>', unsafe_allow_html=True)
        st.markdown(f'<span class="badge"><i class="fas fa-seedling"></i> {crop_stage_options[crop_stage][:2]}</span>', unsafe_allow_html=True)
    with cols[1]:
        for p in priority[:2]:
            st.markdown(f'<span class="badge">{p[:10]}</span>', unsafe_allow_html=True)

# ---------------- SESSION STATE ----------------
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'full_output' not in st.session_state:
    st.session_state.full_output = None
if 'show_recommendations' not in st.session_state:
    st.session_state.show_recommendations = False

# ---------------- MAIN DASHBOARD (TABS AS BIG BUTTONS) ----------------
tab1, tab2 = st.tabs([
    "🌾 **GET ADVICE**  <i class='fas fa-list-check' style='margin-left:8px;'></i>",
    "💬 **ASK FARM BOT**  <i class='fas fa-robot' style='margin-left:8px;'></i>"
])

# ---------- TAB 1: SMART RECOMMENDATIONS ----------
with tab1:
    # QUICK STATS TILES (VISUAL DASHBOARD)
    st.markdown("## 🚜 **Your Farm Dashboard**")
    col_tile1, col_tile2, col_tile3, col_tile4 = st.columns(4)
    with col_tile1:
        st.markdown(f"""
        <div class="farm-tile">
            <i class="fas fa-globe-asia"></i>
            <h3>{region}</h3>
            <p style="color:black;">Region</p>
        </div>
        """, unsafe_allow_html=True)
    with col_tile2:
        st.markdown(f"""
        <div class="farm-tile">
            <i class="fas fa-calendar-alt"></i>
            <h3>{crop_stage}</h3>
            <p style="color:black;">Stage</p>
        </div>
        """, unsafe_allow_html=True)
    with col_tile3:
        st.markdown(f"""
        <div class="farm-tile">
            <i class="fas fa-bullseye"></i>
            <h3>{len(priority)}</h3>
            <p style="color:black;">Goals</p>
        </div>
        """, unsafe_allow_html=True)
    with col_tile4:
        creativity_icon = "🎨" if temperature > 0.6 else "⚖️" if temperature > 0.4 else "🎯"
        st.markdown(f"""
        <div class="farm-tile">
            <i class="fas fa-brain"></i>
            <h3>{creativity_icon}</h3>
            <p style="color:black;">{creativity_percent}%</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # BIG ACTION BUTTON
    col1, col2 = st.columns([2,1])
    with col1:
        if st.button("🚀 **GENERATE FARM PLAN**", use_container_width=True, key="gen_btn"):
            if not location:
                st.warning("📍 Please enter your location first")
            else:
                try:
                    with st.spinner("🌿 AI is thinking about your farm..."):
                        prompt = f"""
                        You are a friendly agricultural advisor. Farmer from {region}, {location}.
                        Crop stage: {crop_stage}. Priorities: {', '.join(priority) if priority else 'General'}.
                        
                        Give EXACTLY 3 recommendations in this format:
                        Recommendation 1:
                        • Action: (simple, clear)
                        • Why: (one sentence)
                        
                        Recommendation 2:
                        • Action:
                        • Why:
                        
                        Recommendation 3:
                        • Action:
                        • Why:
                        
                        Use very simple words. No chemicals.
                        """
                        response = client.models.generate_content(
                            model="gemini-3-flash-preview",
                            contents=prompt,
                            config={"temperature": temperature, "max_output_tokens": 1024}
                        )
                        if hasattr(response, "text") and response.text:
                            full_output = response.text
                        else:
                            full_output = "⚠️ Could not get advice. Try again."
                        st.session_state.full_output = full_output
                        st.session_state.show_recommendations = True
                except Exception as e:
                    st.error("⚠️ AI service busy. Please try later.")
    
    with col2:
        st.markdown("""
        <div style="background-color: #FFBE0B; border-radius: 30px; padding: 1rem; text-align: center; border:4px solid white;">
            <i class="fas fa-lightbulb" style="font-size:2rem; color:black;"></i>
            <p style="color:black; font-weight:700;">Tap to get advice</p>
        </div>
        """, unsafe_allow_html=True)
    
    # DISPLAY RECOMMENDATIONS
    if st.session_state.show_recommendations and st.session_state.full_output:
        st.success("✅ **Your personalized farm plan is ready!**")
        st.markdown("## 📋 **3 STEPS TO A BETTER HARVEST**")
        recs = st.session_state.full_output.split('\n\n')
        icons = ["1️⃣", "2️⃣", "3️⃣"]
        for i, rec in enumerate(recs[:3], 1):
            if rec.strip():
                cleaned = rec.replace('•', '➤').replace('Recommendation', '').strip()
                st.markdown(f"""
                <div class="recommendation-card">
                    <h4>{icons[i-1]} Recommendation {i}</h4>
                    <div style="font-size:1.2rem; line-height:1.8;">
                        {cleaned}
                    </div>
                </div>
                """, unsafe_allow_html=True)

# ---------- TAB 2: CHAT WITH AI (BIG, VISUAL, BLACK TEXT) ----------
with tab2:
    st.markdown("## 💬 **Chat with FarmaBuddy**")
    st.markdown('<p style="font-size:1.3rem; color:black;"><i class="fas fa-comment-dots"></i> Ask anything – pests, fertilizers, weather...</p>', unsafe_allow_html=True)
    
    # CHAT CONTAINER
    chat_container = st.container()
    with chat_container:
        st.markdown('<div class="chat-container" style="background: #F0F7F0; border-radius: 40px; padding: 1.5rem;">', unsafe_allow_html=True)
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                st.markdown(f'''
                <div class="user-message">
                    <p><strong>🧑‍🌾 You:</strong> {msg["content"]}</p>
                </div>
                ''', unsafe_allow_html=True)
            else:
                st.markdown(f'''
                <div class="ai-message">
                    <p><strong>🤖 FarmaBuddy:</strong> {msg["content"]}</p>
                </div>
                ''', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # INPUT AREA – BIG TEXT FIELD + SEND BUTTON
    col_in1, col_in2 = st.columns([5,1])
    with col_in1:
        user_q = st.text_input("", placeholder="e.g. How to stop insects naturally?", label_visibility="collapsed", key="chat_in")
    with col_in2:
        send_click = st.button("📤 **SEND**", use_container_width=True, key="send_chat")
    
    if send_click and user_q:
        st.session_state.chat_history.append({"role": "user", "content": user_q})
        try:
            with st.spinner("🌱 AI is answering..."):
                context = f"""
                Farmer: {region}, {location}, {crop_stage}, priorities: {priority}.
                Question: {user_q}
                Give simple, practical answer. Short sentences. No chemicals.
                """
                response = client.models.generate_content(
                    model="gemini-3-flash-preview",
                    contents=context,
                    config={"temperature": temperature, "max_output_tokens": 1024}
                )
                if hasattr(response, "text") and response.text:
                    ai_reply = response.text
                else:
                    ai_reply = "Sorry, I couldn't understand. Can you ask again?"
                st.session_state.chat_history.append({"role": "assistant", "content": ai_reply})
                st.rerun()
        except:
            st.session_state.chat_history.append({"role": "assistant", "content": "⚠️ AI is busy. Please try later."})
            st.rerun()
    
    if st.session_state.chat_history:
        if st.button("🗑️ **Clear chat**", use_container_width=True, key="clear_chat"):
            st.session_state.chat_history = []
            st.rerun()

# ---------------- FEEDBACK (EMOJI BASED, SIMPLE) ----------------
st.markdown("---")
st.markdown("## 👍 **How was your experience?**")
col_f1, col_f2, col_f3, col_f4, col_f5 = st.columns(5)
with col_f1:
    if st.button("😞", use_container_width=True, key="fb1"):
        st.toast("Thank you for feedback!")
with col_f2:
    if st.button("🙁", use_container_width=True, key="fb2"):
        st.toast("We'll improve!")
with col_f3:
    if st.button("😐", use_container_width=True, key="fb3"):
        st.balloons()
with col_f4:
    if st.button("🙂", use_container_width=True, key="fb4"):
        st.balloons()
with col_f5:
    if st.button("😍", use_container_width=True, key="fb5"):
        st.balloons()
        st.snow()

# ---------------- SESSION LOG (SIMPLIFIED) ----------------
st.markdown("---")
st.markdown("## 📊 **Today's activity**")
log_data = {
    "Time": datetime.now().strftime("%H:%M"),
    "Region": region,
    "Location": location or "—",
    "Stage": crop_stage,
    "Goals": len(priority),
    "Chats": len(st.session_state.chat_history)
}
df_log = pd.DataFrame([log_data])
st.dataframe(df_log, use_container_width=True, hide_index=True)

# ---------------- FOOTER ----------------
st.markdown(f"""
<div class="footer">
    <div style="display: flex; justify-content: center; gap: 40px; flex-wrap: wrap;">
        <span style="font-size:2rem;">🌱</span>
        <span style="font-size:1.8rem; font-weight:800;">FarmaBuddy</span>
        <span style="font-size:2rem;">🌾</span>
    </div>
    <p style="font-size:1.2rem; margin-top:1rem;">❤️ Made for farmers – simple, colorful, smart</p>
    <p style="font-size:0.9rem;">{datetime.now().strftime("%B %Y")}</p>
</div>
""", unsafe_allow_html=True)
