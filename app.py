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

# ---------- FONT AWESOME + ENHANCED CSS ----------
st.markdown("""
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
<style>
    /* ----- GLOBAL: BLACK TEXT, NO FUNNY STYLES ----- */
    * {
        font-family: 'Inter', 'Segoe UI', sans-serif;
        box-sizing: border-box;
    }
    
    /* Smooth scroll for better UX */
    html {
        scroll-behavior: smooth;
    }
    
    .stApp {
        background: linear-gradient(135deg, #F0F9F0 0%, #E8F5E9 50%, #F9FFF9 100%);
        background-attachment: fixed;
    }
    p, li, div:not(.header-container):not(.sidebar-header):not(.title-text):not(.subtitle-text):not(.badge):not(.stButton > button):not(.stTabs [data-baseweb="tab"]):not(.footer) {
        color: #000000 !important;
    }

    /* ----- VIBRANT SOLID COLOR PALETTE WITH GRADIENTS ----- */
    :root {
        --green: #2E7D32;
        --green-gradient: linear-gradient(135deg, #2E7D32 0%, #388E3C 50%, #43A047 100%);
        --orange: #FF8C42;
        --orange-gradient: linear-gradient(135deg, #FF8C42 0%, #FF9F66 50%, #FFB388 100%);
        --blue: #3A86FF;
        --yellow: #FFBE0B;
        --yellow-gradient: linear-gradient(135deg, #FFBE0B 0%, #FFD147 50%, #FFE380 100%);
        --red: #FF595E;
        --purple: #9B5DE5;
        --light-bg: #F8FFF8;
        --white: #FFFFFF;
        --black: #000000;
        --glass-bg: rgba(255, 255, 255, 0.7);
        --glass-border: rgba(255, 255, 255, 0.3);
    }
    
    /* CSS Variables for animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes slideInLeft {
        from { opacity: 0; transform: translateX(-30px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    @keyframes slideInRight {
        from { opacity: 0; transform: translateX(30px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    @keyframes shimmer {
        0% { background-position: -1000px 0; }
        100% { background-position: 1000px 0; }
    }
    
    @keyframes spin {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    
    @keyframes typing {
        from { width: 0; }
        to { width: 100%; }
    }
    
    @keyframes ripple {
        0% { transform: scale(0); opacity: 1; }
        100% { transform: scale(4); opacity: 0; }
    }
    
    /* Reduced motion for accessibility */
    @media (prefers-reduced-motion: reduce) {
        *, *::before, *::after {
            animation-duration: 0.01ms !important;
            animation-iteration-count: 1 !important;
            transition-duration: 0.01ms !important;
        }
    }

    /* ----- HEADER – GRADIENT, ANIMATED, GLASSMORPHIC ----- */
    .header-container {
        background: var(--green-gradient);
        padding: 2rem 2.5rem;
        border-radius: 30px 30px 30px 0;
        margin-bottom: 2rem;
        border: 6px solid var(--yellow);
        box-shadow: 0 20px 60px rgba(46, 125, 50, 0.3), 
                    0 0 0 1px rgba(255, 255, 255, 0.2) inset;
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-wrap: wrap;
        position: relative;
        overflow: hidden;
        animation: fadeIn 0.8s ease-out;
    }
    
    /* Sticky header on scroll */
    .header-container.sticky {
        position: sticky;
        top: 0;
        z-index: 1000;
        animation: slideInRight 0.5s ease-out;
    }
    
    /* Animated gradient overlay */
    .header-container::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, 
            transparent 30%, 
            rgba(255, 255, 255, 0.1) 50%, 
            transparent 70%);
        animation: shimmer 3s infinite;
    }
    
    .header-text { 
        flex: 2; 
        position: relative;
        z-index: 1;
        animation: slideInLeft 0.8s ease-out;
    }
    
    .header-icon {
        flex: 1;
        text-align: center;
        font-size: 5rem;
        color: var(--yellow);
        text-shadow: 0 4px 20px rgba(255, 190, 11, 0.5);
        display: flex;
        justify-content: center;
        align-items: center;
        animation: float 3s ease-in-out infinite;
        position: relative;
        z-index: 1;
    }
    
    .header-icon:hover {
        animation: pulse 0.6s ease-in-out, float 3s ease-in-out infinite;
    }
    
    .title-text {
        font-size: 3.8rem !important;
        font-weight: 900 !important;
        color: white !important;
        margin-bottom: 0.2rem !important;
        text-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        line-height: 1.2;
    }
    
    .subtitle-text {
        font-size: 1.6rem !important;
        font-weight: 700 !important;
        color: var(--yellow) !important;
        text-shadow: 0 2px 10px rgba(255, 190, 11, 0.5);
    }
    
    /* Responsive header */
    @media (max-width: 768px) {
        .header-container {
            padding: 1.5rem;
            flex-direction: column;
            text-align: center;
        }
        .title-text { font-size: 2.5rem !important; }
        .subtitle-text { font-size: 1.2rem !important; }
        .header-icon { font-size: 3rem; margin-top: 1rem; }
    }

    /* ----- SIDEBAR – SMOOTH SLIDE-IN, GLASSMORPHIC ----- */
    .sidebar .sidebar-content {
        background: var(--green-gradient);
        border-right: 8px solid var(--yellow);
        padding-top: 1.5rem;
        animation: slideInLeft 0.6s ease-out;
        box-shadow: 4px 0 20px rgba(46, 125, 50, 0.2);
    }
    
    .sidebar-header {
        background: var(--yellow-gradient);
        padding: 1.2rem;
        border-radius: 20px;
        margin-bottom: 1.5rem;
        border: 4px solid white;
        text-align: center;
        box-shadow: 0 4px 15px rgba(255, 190, 11, 0.3);
        animation: fadeIn 0.8s ease-out;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .sidebar-header:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(255, 190, 11, 0.4);
    }
    
    .sidebar-header * { color: black !important; }

    /* ----- INPUT LABELS – ICON + TEXT, FLOATING STYLE ----- */
    .input-label {
        display: flex;
        align-items: center;
        gap: 8px;
        font-weight: 700;
        font-size: 1.1rem;
        color: white !important;
        margin-bottom: 6px;
        padding-left: 4px;
        animation: slideInLeft 0.5s ease-out;
        transition: all 0.3s ease;
    }
    
    .input-label:hover {
        transform: translateX(5px);
        color: var(--yellow) !important;
    }
    
    .input-label i {
        font-size: 1.2rem;
        width: 24px;
        text-align: center;
        color: white !important;
        transition: transform 0.3s ease;
    }
    
    .input-label:hover i {
        transform: scale(1.2) rotate(10deg);
    }

    /* ----- BIG, VISIBLE WIDGETS WITH SMOOTH TRANSITIONS ----- */
    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] > div,
    div[data-baseweb="multiselect"] > div {
        background-color: white !important;
        border: 4px solid var(--orange) !important;
        border-radius: 20px !important;
        color: black !important;
        font-weight: 500 !important;
        padding: 8px 16px !important;
        margin-bottom: 16px !important;
        box-shadow: 0 2px 10px rgba(255, 140, 66, 0.2) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        animation: fadeIn 0.5s ease-out;
    }
    
    div[data-baseweb="select"] > div:hover,
    div[data-baseweb="input"] > div:hover,
    div[data-baseweb="multiselect"] > div:hover {
        border-color: var(--red) !important;
        transform: translateY(-2px);
        box-shadow: 0 4px 20px rgba(255, 140, 66, 0.4) !important;
    }
    
    div[data-baseweb="select"] > div:focus-within,
    div[data-baseweb="input"] > div:focus-within,
    div[data-baseweb="multiselect"] > div:focus-within {
        border-color: var(--blue) !important;
        box-shadow: 0 4px 20px rgba(58, 134, 255, 0.4) !important;
        outline: 2px solid rgba(58, 134, 255, 0.3);
        outline-offset: 2px;
    }
    
    /* Dropdown menu itself – glassmorphism */
    div[data-baseweb="select"] div[data-baseweb="popover"] {
        background: var(--glass-bg) !important;
        backdrop-filter: blur(10px) !important;
        -webkit-backdrop-filter: blur(10px) !important;
        border: 3px solid var(--orange) !important;
        border-radius: 15px !important;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1) !important;
        animation: fadeIn 0.3s ease-out;
    }

    /* ----- TABS – ANIMATED, GLASSMORPHIC ----- */
    .stTabs [data-baseweb="tab-list"] {
        gap: 15px;
        background: var(--yellow-gradient);
        padding: 12px;
        border-radius: 60px;
        border: 4px solid white;
        box-shadow: 0 8px 32px rgba(255, 190, 11, 0.3);
        margin-bottom: 2rem;
        display: flex;
        flex-wrap: wrap;
        animation: fadeIn 0.8s ease-out;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 70px;
        background-color: white !important;
        border-radius: 50px !important;
        color: black !important;
        font-weight: 800 !important;
        font-size: 1.2rem !important;
        border: 4px solid var(--green) !important;
        padding: 0 2rem !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        gap: 10px;
        white-space: nowrap;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        position: relative;
        overflow: hidden;
    }
    
    /* Tab hover effect with ripple */
    .stTabs [data-baseweb="tab"]:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 6px 20px rgba(46, 125, 50, 0.3);
    }
    
    /* Tab icons via pseudo-elements */
    .stTabs [data-baseweb="tab"]:nth-child(1)::before {
        font-family: "Font Awesome 6 Free";
        content: "\\f0ae";
        font-weight: 900;
        font-size: 1.4rem;
        margin-right: 6px;
        color: var(--green);
        transition: transform 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:nth-child(2)::before {
        font-family: "Font Awesome 6 Free";
        content: "\\f544";
        font-weight: 900;
        font-size: 1.4rem;
        margin-right: 6px;
        color: var(--green);
        transition: transform 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover::before {
        transform: scale(1.2) rotate(10deg);
    }
    
    .stTabs [aria-selected="true"] {
        background: var(--green-gradient) !important;
        color: white !important;
        border-color: var(--yellow) !important;
        box-shadow: 0 4px 20px rgba(46, 125, 50, 0.4) !important;
        transform: scale(1.05);
    }
    
    .stTabs [aria-selected="true"]::before {
        color: white !important;
    }
    
    /* Responsive tabs */
    @media (max-width: 768px) {
        .stTabs [data-baseweb="tab"] {
            height: 60px;
            font-size: 1rem !important;
            padding: 0 1.5rem !important;
        }
    }

    /* ----- CARDS – GLASSMORPHIC, ANIMATED ----- */
    .recommendation-card {
        background: var(--glass-bg);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border-radius: 30px 30px 30px 0;
        padding: 1.8rem 2rem;
        margin: 1.5rem 0;
        border-left: 12px solid var(--green);
        border: 1px solid var(--glass-border);
        border-left: 12px solid var(--green);
        box-shadow: 0 8px 32px rgba(46, 125, 50, 0.15),
                    0 0 0 1px rgba(255, 255, 255, 0.3) inset;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
        animation: fadeIn 0.6s ease-out;
        animation-fill-mode: both;
    }
    
    /* Staggered animation for multiple cards */
    .recommendation-card:nth-child(1) { animation-delay: 0.1s; }
    .recommendation-card:nth-child(2) { animation-delay: 0.2s; }
    .recommendation-card:nth-child(3) { animation-delay: 0.3s; }
    
    /* Shimmer effect on hover */
    .recommendation-card::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, 
            transparent 30%, 
            rgba(255, 255, 255, 0.3) 50%, 
            transparent 70%);
        transform: translateX(-100%);
        transition: transform 0.6s ease;
    }
    
    .recommendation-card:hover::before {
        transform: translateX(100%);
    }
    
    .recommendation-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 12px 48px rgba(46, 125, 50, 0.25),
                    0 0 0 1px rgba(255, 255, 255, 0.5) inset;
        border-left-width: 16px;
    }
    
    .recommendation-card h4 {
        color: var(--green) !important;
        font-size: 1.7rem !important;
        font-weight: 800 !important;
        border-bottom: 4px dashed var(--yellow);
        padding-bottom: 0.8rem;
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 1rem;
        position: relative;
        z-index: 1;
    }
    
    .recommendation-card .card-content {
        position: relative;
        z-index: 1;
    }
    
    /* Copy button inside card */
    .copy-btn {
        position: absolute;
        top: 1rem;
        right: 1rem;
        background: var(--yellow);
        border: 2px solid white;
        border-radius: 50%;
        width: 40px;
        height: 40px;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        transition: all 0.3s ease;
        z-index: 2;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    }
    
    .copy-btn:hover {
        transform: scale(1.1) rotate(10deg);
        background: var(--orange);
    }
    
    /* Responsive cards */
    @media (max-width: 768px) {
        .recommendation-card {
            padding: 1.2rem 1.5rem;
            margin: 1rem 0;
        }
        .recommendation-card h4 {
            font-size: 1.3rem !important;
        }
    }

    /* ----- CHAT BUBBLES – ANIMATED, SMOOTH APPEARANCE ----- */
    .user-message, .ai-message {
        padding: 1.2rem 1.8rem;
        border-radius: 40px 40px 40px 0;
        margin: 1rem 0;
        border: 4px solid white;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        max-width: 85%;
        font-size: 1.05rem;
        display: flex;
        align-items: flex-start;
        gap: 14px;
        transition: all 0.3s ease;
        animation: slideInRight 0.4s ease-out;
        position: relative;
        overflow: hidden;
    }
    
    /* Message animation variants */
    .user-message {
        animation: slideInRight 0.4s ease-out;
    }
    
    .ai-message {
        animation: slideInLeft 0.4s ease-out;
    }
    
    .user-message:hover, .ai-message:hover {
        transform: translateX(5px);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
    }
    
    .user-message i, .ai-message i {
        font-size: 1.8rem;
        flex-shrink: 0;
        margin-top: 2px;
        transition: transform 0.3s ease;
    }
    
    .user-message:hover i, .ai-message:hover i {
        transform: scale(1.1) rotate(5deg);
    }
    
    .user-message p, .ai-message p {
        color: black !important;
        font-weight: 500;
        margin: 0;
        flex: 1;
        line-height: 1.5;
    }
    
    .user-message {
        background: linear-gradient(135deg, #D4EDF7 0%, #A8DAED 100%);
        border-left: 12px solid var(--blue);
        margin-left: auto;
    }
    
    .ai-message {
        background: linear-gradient(135deg, #E2F3E2 0%, #C8E6C9 100%);
        border-left: 12px solid var(--green);
    }
    
    /* Typing indicator animation */
    .typing-indicator {
        display: flex;
        gap: 5px;
        padding: 1rem;
        animation: fadeIn 0.3s ease-out;
    }
    
    .typing-indicator span {
        width: 10px;
        height: 10px;
        border-radius: 50%;
        background: var(--green);
        animation: typing-dot 1.4s infinite;
    }
    
    .typing-indicator span:nth-child(2) { animation-delay: 0.2s; }
    .typing-indicator span:nth-child(3) { animation-delay: 0.4s; }
    
    @keyframes typing-dot {
        0%, 60%, 100% { transform: translateY(0); opacity: 0.7; }
        30% { transform: translateY(-10px); opacity: 1; }
    }
    
    /* Responsive chat bubbles */
    @media (max-width: 768px) {
        .user-message, .ai-message {
            max-width: 95%;
            padding: 1rem 1.2rem;
            font-size: 0.95rem;
        }
    }

    /* ----- BADGES – ANIMATED, GLASSMORPHIC ----- */
    .badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 0.5rem 1.2rem;
        border-radius: 50px;
        font-size: 0.95rem;
        font-weight: 700;
        margin: 0.25rem;
        border: 3px solid white;
        box-shadow: 0 4px 15px rgba(255, 140, 66, 0.3);
        background: var(--orange-gradient);
        color: white !important;
        transition: all 0.3s ease;
        animation: fadeIn 0.5s ease-out;
        cursor: default;
    }
    
    .badge:hover {
        transform: translateY(-3px) scale(1.05);
        box-shadow: 0 6px 20px rgba(255, 140, 66, 0.4);
    }
    
    .badge i { 
        font-size: 1.1rem; 
        transition: transform 0.3s ease;
    }
    
    .badge:hover i {
        transform: scale(1.2) rotate(10deg);
    }

    /* ----- FARM TILES – ANIMATED, CARD FLIP EFFECT ----- */
    .farm-tile {
        background: var(--glass-bg);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 1.4rem 0.5rem;
        border-bottom: 10px solid var(--yellow);
        border: 1px solid var(--glass-border);
        border-bottom: 10px solid var(--yellow);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        text-align: center;
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 6px;
        height: 100%;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
        animation: fadeIn 0.6s ease-out;
        animation-fill-mode: both;
    }
    
    /* Staggered animation for tiles */
    .farm-tile:nth-child(1) { animation-delay: 0.1s; }
    .farm-tile:nth-child(2) { animation-delay: 0.2s; }
    .farm-tile:nth-child(3) { animation-delay: 0.3s; }
    .farm-tile:nth-child(4) { animation-delay: 0.4s; }
    
    .farm-tile::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: var(--green-gradient);
        opacity: 0;
        transition: opacity 0.4s ease;
    }
    
    .farm-tile:hover {
        transform: translateY(-10px) scale(1.05);
        box-shadow: 0 12px 48px rgba(46, 125, 50, 0.3);
        border-bottom-width: 14px;
    }
    
    .farm-tile:hover::before {
        opacity: 0.1;
    }
    
    .farm-tile i { 
        font-size: 2.8rem; 
        color: var(--green); 
        transition: all 0.4s ease;
        position: relative;
        z-index: 1;
    }
    
    .farm-tile:hover i {
        transform: scale(1.2) rotate(10deg);
        color: var(--orange);
    }
    
    .farm-tile h3 { 
        color: var(--green); 
        font-weight: 800; 
        margin: 0; 
        font-size: 1.4rem;
        position: relative;
        z-index: 1;
        transition: all 0.3s ease;
    }
    
    .farm-tile:hover h3 {
        transform: scale(1.1);
    }
    
    .farm-tile p { 
        margin: 0; 
        font-size: 0.9rem;
        position: relative;
        z-index: 1;
    }
    
    /* Animated counter effect */
    .counter {
        animation: countUp 1s ease-out;
    }
    
    @keyframes countUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Responsive tiles */
    @media (max-width: 768px) {
        .farm-tile {
            padding: 1rem 0.5rem;
        }
        .farm-tile i { font-size: 2rem; }
        .farm-tile h3 { font-size: 1.2rem; }
    }

    /* ----- BUTTONS – RIPPLE EFFECT, LOADING STATE ----- */
    .stButton > button {
        background: var(--orange-gradient) !important;
        color: white !important;
        border: 4px solid white !important;
        border-radius: 50px !important;
        padding: 0.9rem 1.8rem !important;
        font-weight: 800 !important;
        font-size: 1.3rem !important;
        box-shadow: 0 8px 30px rgba(255, 140, 66, 0.4) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        width: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 12px;
        position: relative;
        overflow: hidden;
        cursor: pointer;
    }
    
    /* Ripple effect */
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.5);
        transform: translate(-50%, -50%);
        transition: width 0.6s, height 0.6s;
    }
    
    .stButton > button:active::before {
        width: 300px;
        height: 300px;
    }
    
    .stButton > button i { 
        font-size: 1.4rem;
        transition: transform 0.3s ease;
        position: relative;
        z-index: 1;
    }
    
    .stButton > button:hover {
        transform: translateY(-4px) scale(1.02);
        box-shadow: 0 12px 40px rgba(255, 140, 66, 0.5) !important;
        background: linear-gradient(135deg, #FF595E 0%, #FF6B6E 50%, #FF7F7F 100%) !important;
    }
    
    .stButton > button:hover i {
        transform: scale(1.2) rotate(10deg);
    }
    
    .stButton > button:active {
        transform: translateY(-2px) scale(0.98);
        box-shadow: 0 6px 20px rgba(255, 140, 66, 0.4) !important;
    }
    
    /* Disabled state */
    .stButton > button:disabled {
        opacity: 0.5;
        cursor: not-allowed;
        transform: none !important;
    }
    
    /* Loading spinner inside button */
    .button-loading::after {
        content: '';
        position: absolute;
        width: 20px;
        height: 20px;
        margin-left: 10px;
        border: 3px solid white;
        border-top-color: transparent;
        border-radius: 50%;
        animation: spin 0.8s linear infinite;
    }
    
    /* Responsive buttons */
    @media (max-width: 768px) {
        .stButton > button {
            font-size: 1.1rem !important;
            padding: 0.8rem 1.5rem !important;
        }
    }

    /* ----- FOOTER – GRADIENT, ANIMATED ----- */
    .footer {
        background: var(--green-gradient);
        padding: 2rem;
        border-radius: 40px 40px 0 0;
        border-top: 8px solid var(--yellow);
        color: white;
        text-align: center;
        margin-top: 3rem;
        box-shadow: 0 -8px 32px rgba(46, 125, 50, 0.3);
        animation: fadeIn 0.8s ease-out;
        position: relative;
        overflow: hidden;
    }
    
    .footer::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, 
            transparent 30%, 
            rgba(255, 255, 255, 0.1) 50%, 
            transparent 70%);
        animation: shimmer 4s infinite;
    }
    
    .footer * { 
        color: white !important;
        position: relative;
        z-index: 1;
    }
    
    .footer i { 
        margin: 0 10px; 
        font-size: 1.5rem;
        transition: transform 0.3s ease;
    }
    
    .footer i:hover {
        transform: scale(1.3) rotate(15deg);
    }

    /* ----- CUSTOM PROMPT EDITOR – GLASSMORPHIC ----- */
    .prompt-editor {
        background: var(--glass-bg);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border-left: 8px solid var(--yellow);
        border-radius: 20px;
        padding: 1.5rem;
        margin-top: 1rem;
        border: 2px solid var(--glass-border);
        border-left: 8px solid var(--yellow);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        animation: fadeIn 0.5s ease-out;
    }
    
    textarea {
        border: 3px solid var(--green) !important;
        border-radius: 15px !important;
        font-size: 0.95rem !important;
        transition: all 0.3s ease !important;
        background: white !important;
    }
    
    textarea:focus {
        border-color: var(--blue) !important;
        box-shadow: 0 4px 20px rgba(58, 134, 255, 0.3) !important;
        outline: 2px solid rgba(58, 134, 255, 0.2) !important;
        outline-offset: 2px;
    }
    
    textarea:hover {
        border-color: var(--orange) !important;
    }

    /* ----- FEEDBACK EMOJIS – ANIMATED, BOUNCY ----- */
    .stButton button[key*="fb"] {
        font-size: 2.2rem !important;
        padding: 0.3rem !important;
        background: var(--yellow-gradient) !important;
        color: black !important;
        border: 3px solid white !important;
        box-shadow: 0 4px 15px rgba(255, 190, 11, 0.3) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        position: relative;
        overflow: hidden;
    }
    
    .stButton button[key*="fb"]::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.5);
        transform: translate(-50%, -50%);
        transition: width 0.4s, height 0.4s;
    }
    
    .stButton button[key*="fb"]:hover {
        transform: scale(1.2) rotate(10deg);
        background: linear-gradient(135deg, #FFD147 0%, #FFE380 100%) !important;
        box-shadow: 0 6px 25px rgba(255, 190, 11, 0.5) !important;
    }
    
    .stButton button[key*="fb"]:active::before {
        width: 100px;
        height: 100px;
    }
    
    .stButton button[key*="fb"]:active {
        transform: scale(1.1);
        animation: pulse 0.4s ease-in-out;
    }

    /* ----- STREAMLIT HIDDEN LABELS ----- */
    .stSelectbox label, .stTextInput label, .stMultiSelect label, .stSlider label {
        display: none !important;
    }
    
    /* ----- LOADING SPINNER / PROGRESS ----- */
    .stSpinner > div {
        border-color: var(--green) !important;
        border-top-color: transparent !important;
        animation: spin 1s linear infinite !important;
    }
    
    /* Custom loading overlay */
    .loading-overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(46, 125, 50, 0.1);
        backdrop-filter: blur(5px);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 9999;
        animation: fadeIn 0.3s ease-out;
    }
    
    .loading-spinner {
        width: 60px;
        height: 60px;
        border: 6px solid var(--yellow);
        border-top-color: transparent;
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }
    
    /* Success checkmark animation */
    @keyframes checkmark {
        0% { stroke-dashoffset: 100; }
        100% { stroke-dashoffset: 0; }
    }
    
    .success-checkmark {
        animation: checkmark 0.6s ease-out forwards;
    }
    
    /* Progress bar */
    .progress-bar {
        width: 100%;
        height: 8px;
        background: rgba(46, 125, 50, 0.2);
        border-radius: 10px;
        overflow: hidden;
        margin: 1rem 0;
    }
    
    .progress-fill {
        height: 100%;
        background: var(--green-gradient);
        border-radius: 10px;
        animation: progressFill 2s ease-out forwards;
    }
    
    @keyframes progressFill {
        from { width: 0%; }
        to { width: 100%; }
    }
    
    /* Tooltip styles */
    .tooltip {
        position: relative;
        display: inline-block;
    }
    
    .tooltip .tooltiptext {
        visibility: hidden;
        width: 200px;
        background: var(--glass-bg);
        backdrop-filter: blur(10px);
        color: black;
        text-align: center;
        border-radius: 10px;
        padding: 0.5rem 1rem;
        position: absolute;
        z-index: 1;
        bottom: 125%;
        left: 50%;
        margin-left: -100px;
        opacity: 0;
        transition: opacity 0.3s, visibility 0.3s;
        border: 2px solid var(--green);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
    
    .tooltip:hover .tooltiptext {
        visibility: visible;
        opacity: 1;
    }
    
    /* Empty state styling */
    .empty-state {
        text-align: center;
        padding: 3rem 2rem;
        animation: fadeIn 0.6s ease-out;
    }
    
    .empty-state i {
        font-size: 4rem;
        color: var(--green);
        margin-bottom: 1rem;
        opacity: 0.5;
        animation: float 3s ease-in-out infinite;
    }
    
    .empty-state h3 {
        color: var(--green);
        font-size: 1.5rem;
        margin-bottom: 0.5rem;
    }
    
    .empty-state p {
        color: #666;
        font-size: 1.1rem;
    }
    
    /* Error state styling */
    .error-state {
        background: linear-gradient(135deg, #FFE5E5 0%, #FFD5D5 100%);
        border-left: 8px solid var(--red);
        border-radius: 20px;
        padding: 1.5rem;
        margin: 1rem 0;
        animation: fadeIn 0.5s ease-out;
        box-shadow: 0 4px 15px rgba(255, 89, 94, 0.2);
    }
    
    .error-state i {
        color: var(--red);
        font-size: 1.5rem;
        margin-right: 0.5rem;
    }
    
    /* Success state styling */
    .success-state {
        background: linear-gradient(135deg, #E2F3E2 0%, #C8E6C9 100%);
        border-left: 8px solid var(--green);
        border-radius: 20px;
        padding: 1.5rem;
        margin: 1rem 0;
        animation: fadeIn 0.5s ease-out;
        box-shadow: 0 4px 15px rgba(46, 125, 50, 0.2);
    }
    
    .success-state i {
        color: var(--green);
        font-size: 1.5rem;
        margin-right: 0.5rem;
    }
    
    /* Dataframe styling */
    .stDataFrame {
        animation: fadeIn 0.6s ease-out;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: var(--glass-bg) !important;
        backdrop-filter: blur(10px) !important;
        border-radius: 15px !important;
        border: 2px solid var(--green) !important;
        transition: all 0.3s ease !important;
    }
    
    .streamlit-expanderHeader:hover {
        background: rgba(255, 255, 255, 0.9) !important;
        transform: translateX(5px);
        box-shadow: 0 4px 15px rgba(46, 125, 50, 0.2) !important;
    }
    
    /* Slider styling */
    .stSlider {
        animation: fadeIn 0.5s ease-out;
    }
    
    /* Focus states for accessibility */
    *:focus {
        outline: 3px solid var(--blue) !important;
        outline-offset: 2px;
    }
    
    button:focus,
    input:focus,
    textarea:focus,
    select:focus {
        box-shadow: 0 0 0 3px rgba(58, 134, 255, 0.3) !important;
    }
    
    /* High contrast mode support */
    @media (prefers-contrast: high) {
        * {
            border-width: 2px !important;
        }
        
        .header-container,
        .recommendation-card,
        .farm-tile {
            border: 3px solid black !important;
        }
    }
    
    /* Print styles */
    @media print {
        .sidebar,
        .stButton,
        .footer {
            display: none !important;
        }
        
        .header-container,
        .recommendation-card,
        .farm-tile {
            box-shadow: none !important;
            border: 2px solid black !important;
        }
    }

</style>
""", unsafe_allow_html=True)

# ---------------- API KEY ----------------
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("🔐 API Key Missing - Please add GOOGLE_API_KEY to Streamlit Secrets")
    st.stop()
api_key = st.secrets["GOOGLE_API_KEY"]
client = genai.Client(api_key=api_key)

# ---------------- HEADER ----------------
st.markdown("""
<div class="header-container">
    <div class="header-text">
        <h1 class="title-text"><i class="fas fa-leaf" style="margin-right:12px;"></i>FarmaBuddy</h1>
        <h4 class="subtitle-text"><i class="fas fa-robot"></i> AI Farmer Friend</h4>
        <p style="color: white; font-size: 1.3rem; margin-top: 0.5rem;">
            <i class="fas fa-seedling"></i> Smart advice, big harvests  <i class="fas fa-tractor"></i>
        </p>
    </div>
    <div class="header-icon">
        <i class="fas fa-sprout"></i>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR (CRYSTAL CLEAR DROPDOWNS) ----------------
with st.sidebar:
    st.markdown('<div class="sidebar-header"><h3 style="margin:0;">🧑‍🌾 Your Farm Setup</h3></div>', unsafe_allow_html=True)

    # ---- REGION – FULLY VISIBLE, ICON INSIDE LABEL ----
    st.markdown('<label class="input-label"><i class="fas fa-globe-americas"></i> Where is your farm?</label>', unsafe_allow_html=True)
    region = st.selectbox(
        "region",
        ["India", "Ghana", "Canada", "USA", "Australia", "Brazil", "Kenya", "France"],
        label_visibility="collapsed",
        key="region_select"
    )

    # ---- LOCATION ----
    st.markdown('<label class="input-label"><i class="fas fa-map-marker-alt"></i> State / Province</label>', unsafe_allow_html=True)
    location = st.text_input(
        "location",
        placeholder="e.g. Punjab, Ontario...",
        label_visibility="collapsed",
        key="location_input"
    )

    # ---- CROP STAGE ----
    st.markdown('<label class="input-label"><i class="fas fa-seedling"></i> Crop stage?</label>', unsafe_allow_html=True)
    crop_stage_options = {
        "Planning": "📋 Planning",
        "Sowing": "🌱 Sowing",
        "Growing": "🌿 Growing",
        "Harvesting": "🌾 Harvesting",
        "Post-Harvest": "🏭 Storage"
    }
    crop_stage = st.selectbox(
        "crop",
        list(crop_stage_options.keys()),
        format_func=lambda x: crop_stage_options[x],
        label_visibility="collapsed",
        key="crop_select"
    )

    # ---- PRIORITIES ----
    st.markdown('<label class="input-label"><i class="fas fa-bullseye"></i> Your goals</label>', unsafe_allow_html=True)
    priority = st.multiselect(
        "priority",
        ["💧 Save Water", "📈 High Yield", "🌿 Organic", "💰 Low Cost", 
         "🛡️ Pest Control", "🌱 Soil Health", "🚜 Automation", "♻️ Sustainability"],
        default=["📈 High Yield"],
        label_visibility="collapsed",
        key="priority_multiselect"
    )

    # ---- AI CREATIVITY ----
    st.markdown('<label class="input-label"><i class="fas fa-brain"></i> AI Creativity</label>', unsafe_allow_html=True)
    temperature = st.slider(
        "creativity",
        0.2, 0.9, 0.5,
        label_visibility="collapsed",
        key="temp_slider",
        help="More creative = surprising ideas, Consistent = safe advice"
    )
    creativity_percent = int((temperature - 0.2) / 0.7 * 100)
    creativity_label = "🎨 Very Creative" if temperature > 0.7 else "⚖️ Balanced" if temperature > 0.4 else "🎯 Focused"
    st.markdown(f"""
    <div style="background: var(--yellow-gradient); padding: 0.8rem; border-radius: 30px; text-align: center; border:4px solid white; margin-top: 0.5rem; box-shadow: 0 4px 15px rgba(255, 190, 11, 0.3); transition: all 0.3s ease; animation: fadeIn 0.5s ease-out;">
        <span style="font-weight:800; font-size:1.4rem; color:black;">✨ {creativity_percent}% creative</span>
        <p style="font-size:0.9rem; margin:0.3rem 0 0 0; color:black;">{creativity_label}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 📋 Your summary")
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
if 'custom_rec_prompt' not in st.session_state:
    st.session_state.custom_rec_prompt = ""
if 'custom_chat_prompt' not in st.session_state:
    st.session_state.custom_chat_prompt = ""
if 'is_generating' not in st.session_state:
    st.session_state.is_generating = False

# ---------------- JAVASCRIPT FOR ENHANCED INTERACTIONS ----------------
st.markdown("""
<script>
// Auto-scroll to latest message in chat
function scrollToBottom() {
    const chatContainer = document.querySelector('.stContainer');
    if (chatContainer) {
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }
}

// Smooth scroll behavior
document.addEventListener('DOMContentLoaded', function() {
    // Add smooth scroll to all internal links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        });
    });
    
    // Add ripple effect to buttons
    document.querySelectorAll('.stButton > button').forEach(button => {
        button.addEventListener('click', function(e) {
            const ripple = document.createElement('span');
            ripple.classList.add('ripple-effect');
            ripple.style.left = e.offsetX + 'px';
            ripple.style.top = e.offsetY + 'px';
            this.appendChild(ripple);
            
            setTimeout(() => {
                ripple.remove();
            }, 600);
        });
    });
    
    // Observe chat messages and auto-scroll
    const observer = new MutationObserver(scrollToBottom);
    const chatContainer = document.querySelector('.stContainer');
    if (chatContainer) {
        observer.observe(chatContainer, { childList: true, subtree: true });
    }
    
    // Add keyboard shortcuts
    document.addEventListener('keydown', function(e) {
        // Ctrl/Cmd + Enter to submit
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            const sendButton = document.querySelector('[key="send_btn"]');
            if (sendButton) {
                sendButton.click();
            }
        }
    });
    
    // Add copy functionality to recommendation cards
    document.querySelectorAll('.recommendation-card').forEach(card => {
        const copyBtn = document.createElement('div');
        copyBtn.className = 'copy-btn';
        copyBtn.innerHTML = '<i class="fas fa-copy"></i>';
        copyBtn.title = 'Copy to clipboard';
        
        copyBtn.addEventListener('click', function() {
            const text = card.innerText;
            navigator.clipboard.writeText(text).then(() => {
                copyBtn.innerHTML = '<i class="fas fa-check"></i>';
                setTimeout(() => {
                    copyBtn.innerHTML = '<i class="fas fa-copy"></i>';
                }, 2000);
            });
        });
        
        card.appendChild(copyBtn);
    });
});

// Performance optimization: Use GPU acceleration
const style = document.createElement('style');
style.textContent = `
    .recommendation-card,
    .farm-tile,
    .user-message,
    .ai-message,
    .stButton > button {
        will-change: transform;
        transform: translateZ(0);
        backface-visibility: hidden;
    }
`;
document.head.appendChild(style);
</script>
""", unsafe_allow_html=True)

# ---------------- TABS (NO RAW HTML, ICONS VIA CSS) ----------------
tab1, tab2 = st.tabs(["GET ADVICE", "ASK FARM BOT"])

# ========== TAB 1: RECOMMENDATIONS ==========
with tab1:
    st.markdown("## 🚜 Your Farm Dashboard")
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

    # ---- Custom Prompt Expander ----
    with st.expander("🛠️ Advanced: Customize recommendation prompt"):
        st.markdown('<div class="prompt-editor">', unsafe_allow_html=True)
        st.info("Edit the prompt below. {placeholders} will be filled automatically.")
        default_rec_prompt = f"""You are an expert agricultural advisor. 
Farmer location: {{region}}, {{location}}.
Current crop stage: {{crop_stage}}.
Farmer priorities: {{priority}}.

Give EXACTLY 3 farming recommendations in this format:

Recommendation 1:
• Action: (clear, one sentence)
• Why: (one sentence)

Recommendation 2:
• Action:
• Why:

Recommendation 3:
• Action:
• Why:

Use simple words, region-specific advice, and avoid unsafe chemicals."""
        st.session_state.custom_rec_prompt = st.text_area(
            "Edit prompt",
            value=st.session_state.custom_rec_prompt or default_rec_prompt,
            height=280,
            label_visibility="collapsed"
        )
        st.markdown('</div>', unsafe_allow_html=True)

    # ---- Generate Button ----
    col1, col2 = st.columns([2, 1])
    with col1:
        if st.button("🚜 GENERATE FARM PLAN", use_container_width=True, key="gen_btn"):
            if not location:
                st.markdown("""
                <div class="error-state">
                    <i class="fas fa-exclamation-triangle"></i>
                    <strong>Location Required:</strong> Please enter your location in the sidebar to get personalized advice.
                </div>
                """, unsafe_allow_html=True)
            else:
                try:
                    st.session_state.is_generating = True
                    
                    # Show progress indicator
                    progress_placeholder = st.empty()
                    progress_placeholder.markdown("""
                    <div style="text-align: center; padding: 2rem;">
                        <div class="loading-spinner" style="margin: 0 auto;"></div>
                        <p style="margin-top: 1rem; font-size: 1.2rem; color: var(--green); font-weight: 700;">
                            🌱 AI is analyzing your farm setup...
                        </p>
                        <div class="progress-bar">
                            <div class="progress-fill"></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    prompt = st.session_state.custom_rec_prompt or default_rec_prompt
                    prompt = prompt.format(
                        region=region,
                        location=location,
                        crop_stage=crop_stage,
                        priority=', '.join(priority) if priority else 'General'
                    )
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
                    st.session_state.is_generating = False
                    progress_placeholder.empty()
                    
                    # Show success message
                    st.markdown("""
                    <div class="success-state">
                        <i class="fas fa-check-circle"></i>
                        <strong>Success!</strong> Your personalized farm plan is ready below.
                    </div>
                    """, unsafe_allow_html=True)
                    st.balloons()
                    
                except Exception as e:
                    st.session_state.is_generating = False
                    progress_placeholder.empty()
                    st.markdown("""
                    <div class="error-state">
                        <i class="fas fa-exclamation-circle"></i>
                        <strong>Oops!</strong> AI service is temporarily busy. Please try again in a moment.
                    </div>
                    """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="tooltip" style="background: var(--yellow-gradient); border-radius: 30px; padding: 1rem; text-align: center; border:4px solid white; box-shadow: 0 4px 15px rgba(255, 190, 11, 0.3); transition: all 0.3s ease; cursor: help; animation: fadeIn 0.6s ease-out;" 
             title="Click the button on the left to generate personalized farming recommendations based on your inputs">
            <i class="fas fa-lightbulb" style="font-size:2rem; color:black;"></i>
            <p style="color:black; font-weight:700; margin:0;">Tap to get advice</p>
            <span class="tooltiptext">Fill in your details and click "Generate Farm Plan" to receive AI-powered recommendations!</span>
        </div>
        """, unsafe_allow_html=True)

    # ---- Display Recommendations ----
    if st.session_state.show_recommendations and st.session_state.full_output:
        st.markdown("## 📋 3 STEPS TO A BETTER HARVEST")
        recs = st.session_state.full_output.split('\n\n')
        icons = ["1️⃣", "2️⃣", "3️⃣"]
        for i, rec in enumerate(recs[:3], 1):
            if rec.strip():
                cleaned = rec.replace('•', '➤').replace('Recommendation', '').strip()
                st.markdown(f"""
                <div class="recommendation-card" style="animation-delay: {i * 0.1}s;">
                    <h4>{icons[i-1]} Recommendation {i}</h4>
                    <div class="card-content" style="font-size:1.2rem; line-height:1.8;">
                        {cleaned}
                    </div>
                </div>
                """, unsafe_allow_html=True)
    elif not st.session_state.show_recommendations and not st.session_state.is_generating:
        # Empty state
        st.markdown("""
        <div class="empty-state">
            <i class="fas fa-seedling"></i>
            <h3>Ready to get started?</h3>
            <p>Fill in your farm details in the sidebar and click "Generate Farm Plan" to receive personalized recommendations.</p>
        </div>
        """, unsafe_allow_html=True)

# ========== TAB 2: CHAT ==========
with tab2:
    st.markdown("## 💬 Chat with FarmaBuddy")
    st.markdown('<p style="font-size:1.2rem; color:black;"><i class="fas fa-comment-dots"></i> Ask anything – pests, fertilizers, weather...</p>', unsafe_allow_html=True)

    # ---- Custom Chat Prompt ----
    with st.expander("🛠️ Advanced: Customize chat AI prompt"):
        st.markdown('<div class="prompt-editor">', unsafe_allow_html=True)
        st.info("This system prompt guides how the AI responds. {placeholders} are replaced with your farm data.")
        default_chat_prompt = f"""You are FarmaBuddy, a helpful farming assistant.
Current farmer context:
- Region: {{region}}
- Location: {{location}}
- Crop stage: {{crop_stage}}
- Priorities: {{priority}}

Answer the user's question with:
- Very simple, practical language
- Short sentences
- No unsafe chemicals
- Focus on actionable advice
If the question is not about farming, politely redirect."""
        st.session_state.custom_chat_prompt = st.text_area(
            "Edit system prompt",
            value=st.session_state.custom_chat_prompt or default_chat_prompt,
            height=220,
            label_visibility="collapsed",
            key="chat_prompt_edit"
        )
        st.markdown('</div>', unsafe_allow_html=True)

    # ---- Chat Container ----
    chat_container = st.container()
    with chat_container:
        st.markdown('<div style="background: linear-gradient(135deg, #F0F7F0 0%, #E8F5E9 100%); border-radius: 40px; padding: 1.5rem; min-height: 400px;">', unsafe_allow_html=True)
        
        if not st.session_state.chat_history:
            # Empty state for chat
            st.markdown("""
            <div class="empty-state">
                <i class="fas fa-comments"></i>
                <h3>Start a conversation!</h3>
                <p>Ask me anything about farming - pests, fertilizers, irrigation, weather, or any farm-related questions.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            for msg in st.session_state.chat_history:
                if msg["role"] == "user":
                    st.markdown(f'''
                    <div class="user-message">
                        <i class="fas fa-user"></i>
                        <p><strong>You:</strong> {msg["content"]}</p>
                    </div>
                    ''', unsafe_allow_html=True)
                else:
                    st.markdown(f'''
                    <div class="ai-message">
                        <i class="fas fa-robot"></i>
                        <p><strong>FarmaBuddy:</strong> {msg["content"]}</p>
                    </div>
                    ''', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

    # ---- Input & Send ----
    col_in1, col_in2 = st.columns([5, 1])
    with col_in1:
        user_q = st.text_input("", placeholder="💭 Type your farming question...", label_visibility="collapsed", key="chat_input")
    with col_in2:
        send_click = st.button("📤 SEND", use_container_width=True, key="send_btn")

    if send_click and user_q:
        st.session_state.chat_history.append({"role": "user", "content": user_q})
        
        # Show typing indicator
        typing_placeholder = st.empty()
        typing_placeholder.markdown("""
        <div class="ai-message" style="max-width: 200px;">
            <i class="fas fa-robot"></i>
            <div class="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        try:
            system_prompt = st.session_state.custom_chat_prompt or default_chat_prompt
            system_prompt = system_prompt.format(
                region=region,
                location=location if location else 'unknown',
                crop_stage=crop_stage,
                priority=', '.join(priority) if priority else 'General'
            )
            full_prompt = f"{system_prompt}\n\nUser question: {user_q}"
            response = client.models.generate_content(
                model="gemini-3-flash-preview",
                contents=full_prompt,
                config={"temperature": temperature, "max_output_tokens": 1024}
            )
            if hasattr(response, "text") and response.text:
                ai_reply = response.text
            else:
                ai_reply = "😕 I didn't get that. Please rephrase."
            
            typing_placeholder.empty()
            st.session_state.chat_history.append({"role": "assistant", "content": ai_reply})
            st.rerun()
        except Exception as e:
            typing_placeholder.empty()
            st.markdown("""
            <div class="error-state">
                <i class="fas fa-exclamation-circle"></i>
                <strong>Connection Issue:</strong> AI service is busy. Please try again.
            </div>
            """, unsafe_allow_html=True)
            st.session_state.chat_history.append({"role": "assistant", "content": "⚠️ AI service is busy. Try again."})
            st.rerun()

    if st.session_state.chat_history:
        if st.button("🗑️ Clear chat", use_container_width=True, key="clear_chat"):
            st.session_state.chat_history = []
            st.rerun()

# ---------------- FEEDBACK (EMOJI ONLY) ----------------
st.markdown("---")
st.markdown("## 👍 How was your experience?")
cols = st.columns(5)
emojis = ["😞", "🙁", "😐", "🙂", "😍"]
for i, emoji in enumerate(emojis, 1):
    with cols[i-1]:
        if st.button(emoji, key=f"fb{i}"):
            st.balloons() if i >= 3 else st.toast("Thank you!")

# ---------------- SESSION LOG ----------------
st.markdown("---")
st.markdown("## 📊 Today's activity")
log_data = {
    "Time": datetime.now().strftime("%H:%M"),
    "Region": region,
    "Location": location or "—",
    "Stage": crop_stage,
    "Goals": len(priority),
    "Chats": len(st.session_state.chat_history)
}
st.dataframe(pd.DataFrame([log_data]), use_container_width=True, hide_index=True)

# ---------------- FOOTER ----------------
st.markdown(f"""
<div class="footer">
    <div style="display: flex; justify-content: center; gap: 30px; align-items: center;">
        <i class="fas fa-leaf"></i>
        <span style="font-size:1.8rem; font-weight:800;">FarmaBuddy</span>
        <i class="fas fa-tractor"></i>
    </div>
    <p style="font-size:1.2rem; margin-top:1rem;">❤️ Made for farmers – simple, colorful, smart</p>
    <p style="font-size:0.9rem;">{datetime.now().strftime("%B %Y")}</p>
</div>
""", unsafe_allow_html=True)
