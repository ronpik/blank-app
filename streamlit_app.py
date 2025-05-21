import streamlit as st
import streamlit.components.v1 as components
import os
from globalog import LOG # Import globalog

# --- Configuration for Streamlit App & Widget ---
LOG.info("Streamlit App: Initializing configuration for standalone frontend...")

# URL of the EXTERNALLY RUNNING FastAPI backend.
# This MUST be accessible from the user's browser.
# Example: "http://your-deployed-fastapi-domain.com" or "http://localhost:8000" if FastAPI is running locally.
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

# Construct URLs for widget resources, assuming FastAPI serves them
# The FastAPI server (running elsewhere) must be configured to serve these paths.
WIDGET_SCRIPT_URL = f"{FASTAPI_BACKEND_PUBLIC_URL}/widget/therapist-chat-widget.min.js"
WIDGET_API_BASE_FOR_JS = f"{FASTAPI_BACKEND_PUBLIC_URL}{API_BASE_PATH_ON_FASTAPI}"
THERAPIST_AVATAR_URL = f"{FASTAPI_BACKEND_PUBLIC_URL}/widget/assets/therapist.svg"
USER_AVATAR_URL = f"{FASTAPI_BACKEND_PUBLIC_URL}/widget/assets/user.svg"

# --- Streamlit App Layout ---
st.set_page_config(page_title="Therapist Chat Demo", layout="wide")

st.title("AI Relationship Coach Chat")
st.markdown("""
This is a demonstration of an AI-powered relationship coach. 
Click the chat icon in the bottom right to start a conversation.

The chat widget will connect to an external backend service.
""")

st.sidebar.header("About")
st.sidebar.info(
    "This Streamlit app provides a frontend for the AI Relationship Coach. "
    "The chat widget connects to a separate FastAPI backend service for AI interactions."
)
st.sidebar.markdown("--- ")
st.sidebar.subheader("Widget Connection Configuration:")
st.sidebar.json({
    "FASTAPI_BACKEND_PUBLIC_URL": FASTAPI_BACKEND_PUBLIC_URL,
    "widget_script_src": WIDGET_SCRIPT_URL,
    "widget_api_base (for JS)": WIDGET_API_BASE_FOR_JS,
    "therapist_avatar_src": THERAPIST_AVATAR_URL,
    "user_avatar_src": USER_AVATAR_URL
})

# --- Embed the Chat Widget ---
# The widget script and its assets (JS, CSS, images) are served by the external FastAPI backend.
html_to_embed = f"""
    <script>
      // This configuration is passed to the widget when it initializes.
      // It tells the widget where to find its backend API and assets.
      window.TherapistChatConfig = {{
        apiBase: '{WIDGET_API_BASE_FOR_JS}',          // Tells widget where to send POST /chat requests
        therapistAvatar: '{THERAPIST_AVATAR_URL}', // URL for therapist avatar image
        userAvatar: '{USER_AVATAR_URL}',          // URL for user avatar image
        title: 'AI Relationship Coach',
        placeholder: 'Ask about relationships...',
        initialState: 'collapsed',
        language: 'en', // Default language; can be 'he' for Hebrew/RTL
        // forceRTL: true, // Uncomment to force RTL regardless of language
        // primaryColor: '#yourColor', // Optional: Override default theme colors
        // secondaryColor: '#yourOtherColor'
      }};
    </script>
    <script 
        id="therapist-chat-script"
        src="{WIDGET_SCRIPT_URL}" // This script itself is served by the external FastAPI
    ></script>
"""

components.html(html_to_embed, height=0, scrolling=False) # Height 0 as widget is fixed position

st.markdown("--- ")
st.markdown("### Disclaimer")
st.markdown("This is a demo application. Information provided should not be considered professional advice.") 