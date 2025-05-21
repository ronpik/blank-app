import streamlit as st
import streamlit.components.v1 as components
import os
from globalog import LOG # Import globalog
import shutil
from pathlib import Path

# --- Configuration for Streamlit App & Widget ---
LOG.info("Streamlit App: Initializing configuration...")

# Directory structure for assets
STREAMLIT_APP_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(STREAMLIT_APP_DIR, "streamlit_app", "static")
WIDGET_DIR = os.path.join(STATIC_DIR, "widget")
ASSETS_DIR = os.path.join(WIDGET_DIR, "assets")

# URL of the EXTERNALLY RUNNING FastAPI backend for API calls only.
# This MUST be accessible from the user's browser.
FASTAPI_BACKEND_PUBLIC_URL = st.secrets.get(
    "FASTAPI_BACKEND_PUBLIC_URL", 
    os.environ.get("FASTAPI_BACKEND_PUBLIC_URL", "http://localhost:8000") # Default for local testing
)
LOG.info(f"Streamlit App: FastAPI backend public URL: {FASTAPI_BACKEND_PUBLIC_URL}")

# API base path on the FastAPI server (e.g., "/api")
API_BASE_PATH_ON_FASTAPI = st.secrets.get(
    "API_BASE_PATH", 
    os.environ.get("API_BASE_PATH", "/api") # Default API base path
)
LOG.info(f"Streamlit App: API base path on FastAPI server: {API_BASE_PATH_ON_FASTAPI}")

# Local static file paths - these will be served by Streamlit
WIDGET_SCRIPT_PATH = os.path.join(ASSETS_DIR, "therapist-chat-widget.min.js")
THERAPIST_AVATAR_PATH = os.path.join(ASSETS_DIR, "therapist.svg")
USER_AVATAR_PATH = os.path.join(ASSETS_DIR, "user.svg")

# --- Streamlit App Layout ---
st.set_page_config(page_title="Therapist Chat Demo", layout="wide")

st.title("AI Relationship Coach Chat")
st.markdown("""
This is a demonstration of an AI-powered relationship coach. 
Click the chat icon in the bottom right to start a conversation.

The chat widget will connect to the FastAPI backend for AI processing.
""")

# Display info about static files in sidebar for debugging
st.sidebar.header("About")
st.sidebar.info(
    "This Streamlit app provides a frontend for the AI Relationship Coach. "
    "The chat widget connects to the FastAPI backend service for AI interactions."
)
st.sidebar.markdown("--- ")
st.sidebar.subheader("App Configuration:")

# Check if all required files exist
widget_script_exists = os.path.isfile(WIDGET_SCRIPT_PATH)
therapist_avatar_exists = os.path.isfile(THERAPIST_AVATAR_PATH)
user_avatar_exists = os.path.isfile(USER_AVATAR_PATH)

status = {
    "FASTAPI_BACKEND_PUBLIC_URL": FASTAPI_BACKEND_PUBLIC_URL,
    "API_BASE_PATH": API_BASE_PATH_ON_FASTAPI,
    "widget_script_file": f"{WIDGET_SCRIPT_PATH} (Exists: {widget_script_exists})",
    "therapist_avatar_file": f"{THERAPIST_AVATAR_PATH} (Exists: {therapist_avatar_exists})",
    "user_avatar_file": f"{USER_AVATAR_PATH} (Exists: {user_avatar_exists})"
}
st.sidebar.json(status)

# If files don't exist, show instructions
if not (widget_script_exists and therapist_avatar_exists and user_avatar_exists):
    st.warning("""
    **Missing asset files!** Please copy the following files:
    
    1. Copy the widget script to: `streamlit_app/static/widget/therapist-chat-widget.min.js`
    2. Copy therapist avatar to: `streamlit_app/static/widget/assets/therapist.svg`
    3. Copy user avatar to: `streamlit_app/static/widget/assets/user.svg`
    """)

# --- Embed the Chat Widget ---
# Use Streamlit's way of serving static files
html_to_embed = f"""
    <script>
      // This configuration is passed to the widget when it initializes
      window.TherapistChatConfig = {{
        apiBase: '{FASTAPI_BACKEND_PUBLIC_URL}{API_BASE_PATH_ON_FASTAPI}',  // API endpoint for chat processing
        therapistAvatar: 'streamlit_app/static/widget/assets/therapist.svg', // Local path to therapist avatar
        userAvatar: 'streamlit_app/static/widget/assets/user.svg',          // Local path to user avatar
        title: 'AI Relationship Coach',
        placeholder: 'Ask about relationships...',
        initialState: 'collapsed',
        language: 'en', // Default language; can be 'he' for Hebrew/RTL
        // forceRTL: true, // Uncomment to force RTL regardless of language
        // primaryColor: '#yourColor', // Optional: Override default theme colors
        // secondaryColor: '#yourOtherColor'
      }};
    </script>
"""

if widget_script_exists:
    # Use components.html to include both the script and our inline config
    components.html(
        f"{html_to_embed}<script src='streamlit_app/static/widget/therapist-chat-widget.min.js'></script>",
        height=0, 
        scrolling=False
    )
else:
    st.error("Widget script not found. Please copy the required files first.")

st.markdown("--- ")
st.markdown("### Disclaimer")
st.markdown("This is a demo application. Information provided should not be considered professional advice.") 