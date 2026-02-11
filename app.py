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

# Custom CSS for enhanced UI with black text
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
    
    /* Chat message styling */
    .user-message {
        background: linear-gradient(90deg, #e8f5e9 0%, #f1f8e9 100%);
        padding: 1rem;
        border-radius: 15px;
        margin: 0.5rem 0;
        border-left: 5px solid #4caf50;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }
    
    .ai-message {
        background: white;
        padding: 1rem;
        border-radius: 15px;
        margin: 0.5rem 0;
        border-left: 5px solid #81c784;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
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
    
    /* Chat container */
    .chat-container {
        max-height: 400px;
        overflow-y: auto;
        padding: 1rem;
        border-radius: 10px;
        background: #f9fdf9;
        border: 2px solid #e8f5e9;
    }
    
    /* BLACK TEXT STYLES FOR FARM DATA AND INSIGHTS */
    .black-text {
        color: #000000 !important;
    }
    
    .farm-data-text {
        color: #000000 !important;
        font-weight: 500;
        margin-bottom: 0.5rem;
    }
    
    .insight-text {
        color: #000000 !important;
        line-height: 1.6;
    }
    
    .ai-content {
        color: #000000 !important;
        line-height: 1.7;
        font-size: 1rem;
    }
    
    /* Recommendation card content in black */
    .recommendation-card p,
    .recommendation-card div:not(.badge),
    .recommendation-card span:not(.badge) {
        color: #000000 !important;
    }
    
    /* Keep headers green */
    .recommendation-card h4 {
        color: #2e7d32 !important;
        margin-top: 0;
        margin-bottom: 1rem;
    }
    
    /* Chat text colors */
    .user-message p {
        color: #000000 !important;
        font-weight: 500;
    }
    
    .ai-message p {
        color: #000000 !important;
        line-height: 1.6;
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
    
    # AI Creativity - Fixed label issue
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

# ---------------- INITIALIZE SESSION STATE ----------------
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'full_output' not in st.session_state:
    st.session_state.full_output = None
if 'show_recommendations' not in st.session_state:
    st.session_state.show_recommendations = False

# ---------------- MAIN CONTENT AREA ----------------
tab1, tab2 = st.tabs(["🌾 Get Recommendations", "💬 Ask Questions"])

with tab1:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 💡 Get AI-Powered Farming Advice")
        
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
        
        # Display recommendations from session state (only if they exist)
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
                        st.markdown(f"""
                        <div class="recommendation-card">
                            <h4>📌 Recommendation {i}</h4>
                            <div class="ai-content">
                                {cleaned_rec}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 📈 Farm Insights")
        
        # Current farm status card
        creativity_label = "Creative" if temperature > 0.6 else "Balanced" if temperature > 0.4 else "Conservative"
        
        st.markdown(f"""
        <div class="recommendation-card">
            <h4>🏡 Current Farm Status</h4>
            <p class="farm-data-text"><strong>Region:</strong> {region}</p>
            <p class="farm-data-text"><strong>Stage:</strong> {crop_stage}</p>
            <p class="farm-data-text"><strong>Priorities:</strong> {len(priority)}</p>
            <p class="farm-data-text"><strong>AI Mode:</strong> {creativity_label}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Best practices tip
        st.markdown("""
        <div class="recommendation-card">
            <h4>💡 Pro Tip</h4>
            <p class="insight-text">For best results, ensure your location is specific (state/province level) and priorities reflect your actual farming goals.</p>
            <small class="insight-text">AI recommendations improve with accurate inputs.</small>
        </div>
        """, unsafe_allow_html=True)

with tab2:
    st.markdown("### 💬 Ask Farming Questions")
    st.markdown("Chat with FarmaBuddy AI to get answers to your specific farming questions.")
    
    # Chat container
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    # Display chat history
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
    
    # Chat input
    col_chat1, col_chat2 = st.columns([4, 1])
    
    with col_chat1:
        user_question = st.text_input(
            "Type your farming question here:",
            placeholder="e.g., What are the best crops for Punjab in summer?",
            label_visibility="collapsed",
            key="chat_input"
        )
    
    with col_chat2:
        send_button = st.button("Send", use_container_width=True, key="send_btn")
    
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
        if st.button("Clear Chat History", use_container_width=True, key="clear_chat"):
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
        st.success(f"Thank you! Feedback recorded: {score}/5 stars ⭐")

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
    "Chat Messages": len(st.session_state.chat_history)
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
