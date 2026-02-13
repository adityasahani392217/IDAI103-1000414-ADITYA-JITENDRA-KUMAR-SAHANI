import streamlit as st
import pandas as pd
from datetime import datetime
from google import genai

# ================= CONFIG =================
st.set_page_config(
    page_title="🌾 FarmaBuddy",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================= CLEAN PROFESSIONAL UI =================
st.markdown("""
<style>

/* ---------- GLOBAL ---------- */
* {
    font-family: 'Inter', 'Segoe UI', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #F3F9F4 0%, #E9F5EC 100%);
}

/* ---------- COLOR SYSTEM ---------- */
:root {
    --primary: #2E7D32;
    --accent: #4CAF50;
    --light: #F5FBF6;
    --card: #FFFFFF;
    --border: #E0E6E2;
    --text: #1E1E1E;
}

/* ---------- HEADER ---------- */
.header-container {
    background: var(--primary);
    padding: 1.8rem 2.2rem;
    border-radius: 18px;
    margin-bottom: 2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.title-text {
    font-size: 2.6rem !important;
    font-weight: 800 !important;
    color: white !important;
    margin: 0 !important;
}

.subtitle-text {
    font-size: 1.1rem !important;
    color: #C8E6C9 !important;
}

/* ---------- SIDEBAR ---------- */
.sidebar .sidebar-content {
    background: var(--primary);
}

.sidebar-header {
    background: white;
    color: var(--primary);
    padding: 1rem;
    border-radius: 12px;
    text-align: center;
    margin-bottom: 1.5rem;
    font-weight: 700;
}

/* ---------- INPUTS ---------- */
div[data-baseweb="select"] > div,
div[data-baseweb="input"] > div,
div[data-baseweb="multiselect"] > div,
textarea {
    background: white !important;
    border: 1.5px solid var(--border) !important;
    border-radius: 10px !important;
    padding: 8px 14px !important;
}

div[data-baseweb="select"] > div:hover,
textarea:hover {
    border-color: var(--accent) !important;
}

/* ---------- TABS ---------- */
.stTabs [data-baseweb="tab-list"] {
    background: var(--light);
    border-radius: 50px;
    padding: 6px;
}

.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: var(--primary) !important;
    font-weight: 600 !important;
    border-radius: 30px !important;
    padding: 10px 22px !important;
}

.stTabs [aria-selected="true"] {
    background: var(--primary) !important;
    color: white !important;
}

/* ---------- CARDS ---------- */
.recommendation-card {
    background: white;
    border-radius: 14px;
    padding: 1.5rem;
    margin: 1.2rem 0;
    border: 1px solid var(--border);
}

.recommendation-card h4 {
    color: var(--primary);
    font-size: 1.3rem;
    font-weight: 700;
}

/* ---------- CHAT ---------- */
.user-message, .ai-message {
    padding: 1rem 1.4rem;
    border-radius: 14px;
    margin: 0.6rem 0;
    font-size: 0.95rem;
    border: 1px solid var(--border);
}

.user-message {
    background: #E3F2FD;
}

.ai-message {
    background: #E8F5E9;
}

/* ---------- BUTTON ---------- */
.stButton > button {
    background: var(--primary) !important;
    color: white !important;
    border-radius: 8px !important;
    padding: 0.6rem 1.2rem !important;
    font-weight: 600 !important;
    border: none !important;
}

.stButton > button:hover {
    background: var(--accent) !important;
}

/* ---------- FOOTER ---------- */
.footer {
    background: var(--primary);
    padding: 1.5rem;
    border-radius: 20px 20px 0 0;
    text-align: center;
    color: white;
    margin-top: 3rem;
}

</style>
""", unsafe_allow_html=True)

# ================= API KEY =================
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("🔐 API Key Missing - Add GOOGLE_API_KEY in Streamlit Secrets")
    st.stop()

client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])

# ================= HEADER =================
st.markdown("""
<div class="header-container">
    <div>
        <h1 class="title-text">🌱 FarmaBuddy</h1>
        <div class="subtitle-text">AI Smart Assistant for Farmers</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ================= SIDEBAR =================
with st.sidebar:
    st.markdown('<div class="sidebar-header">🧑‍🌾 Farm Setup</div>', unsafe_allow_html=True)

    region = st.selectbox("Country", 
        ["India", "Ghana", "Canada", "USA", "Australia", "Brazil", "Kenya", "France"])

    location = st.text_input("State / Province", placeholder="e.g. Punjab")

    crop_stage = st.selectbox("Crop Stage", 
        ["Planning", "Sowing", "Growing", "Harvesting", "Post-Harvest"])

    priority = st.multiselect(
        "Goals",
        ["Save Water", "High Yield", "Organic", "Low Cost", 
         "Pest Control", "Soil Health", "Automation"]
    )

    temperature = st.slider("AI Creativity", 0.2, 0.9, 0.5)

# ================= SESSION =================
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ================= TABS =================
tab1, tab2 = st.tabs(["Get Advice", "Chat with AI"])

# ================= RECOMMENDATION TAB =================
with tab1:
    st.subheader("Farm Recommendations")

    if st.button("Generate Farm Plan", use_container_width=True):
        if not location:
            st.warning("Please enter location.")
        else:
            prompt = f"""
You are an expert agricultural advisor.

Region: {region}
Location: {location}
Crop stage: {crop_stage}
Farmer goals: {', '.join(priority) if priority else 'General'}

Give exactly 3 farming recommendations:
Each must include:
- Action:
- Why:

Use simple words. Avoid unsafe chemicals.
"""
            try:
                with st.spinner("Generating advice..."):
                    response = client.models.generate_content(
                        model="gemini-3-flash-preview",
                        contents=prompt,
                        config={
                            "temperature": temperature,
                            "max_output_tokens": 1024
                        }
                    )
                    output = response.text if hasattr(response, "text") else "No response"
                    recommendations = output.split("\n\n")

                    for i, rec in enumerate(recommendations[:3], 1):
                        st.markdown(f"""
                        <div class="recommendation-card">
                            <h4>Recommendation {i}</h4>
                            <p>{rec}</p>
                        </div>
                        """, unsafe_allow_html=True)

            except:
                st.error("AI service temporarily unavailable.")

# ================= CHAT TAB =================
with tab2:
    st.subheader("Chat with FarmaBuddy")

    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f'<div class="user-message"><strong>You:</strong> {msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="ai-message"><strong>AI:</strong> {msg["content"]}</div>', unsafe_allow_html=True)

    user_q = st.text_input("Ask a farming question")

    if st.button("Send"):
        if user_q:
            st.session_state.chat_history.append({"role": "user", "content": user_q})
            try:
                with st.spinner("AI thinking..."):
                    full_prompt = f"""
You are a helpful farming assistant.

Region: {region}
Location: {location}
Stage: {crop_stage}
Goals: {', '.join(priority)}

User question: {user_q}

Answer simply and clearly.
"""
                    response = client.models.generate_content(
                        model="gemini-3-flash-preview",
                        contents=full_prompt,
                        config={
                            "temperature": temperature,
                            "max_output_tokens": 1024
                        }
                    )
                    reply = response.text if hasattr(response, "text") else "Please rephrase."
                    st.session_state.chat_history.append({"role": "assistant", "content": reply})
                    st.rerun()
            except:
                st.session_state.chat_history.append({"role": "assistant", "content": "AI busy. Try again."})
                st.rerun()

# ================= FOOTER =================
st.markdown(f"""
<div class="footer">
    🌾 FarmaBuddy • Smart Farming AI • {datetime.now().year}
</div>
""", unsafe_allow_html=True)
