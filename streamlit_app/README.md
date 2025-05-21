# Therapist Chat Streamlit App

This folder contains the Streamlit application for the AI Relationship Coach chat interface.

## Structure

- `streamlit_app.py`: Main Streamlit application
- `static/`: Directory for static assets
  - `widget/`: Directory for widget files
    - `therapist-chat-widget.min.js`: The chat widget JavaScript file
    - `assets/`: Images and icons
      - `therapist.svg`: Therapist avatar image
      - `user.svg`: User avatar image

## Setup Instructions

1. Copy the required asset files:
   - Copy the widget JavaScript file to: `static/widget/therapist-chat-widget.min.js`
   - Copy the therapist avatar to: `static/widget/assets/therapist.svg`
   - Copy the user avatar to: `static/widget/assets/user.svg`

2. Set the environment variables or Streamlit secrets:
   - `FASTAPI_BACKEND_PUBLIC_URL`: URL of the FastAPI backend (default: "http://localhost:8000")
   - `API_BASE_PATH`: Base path for API endpoints on the FastAPI server (default: "/api")

3. Run the Streamlit app:
   ```
   streamlit run streamlit_app.py
   ```

## Configuration

The chat widget can be configured by modifying the `TherapistChatConfig` object in the `streamlit_app.py` file:

- `apiBase`: API endpoint for chat processing
- `language`: Set to 'en' for English, 'he' for Hebrew (RTL)
- `forceRTL`: Force RTL layout regardless of language
- `primaryColor` and `secondaryColor`: Override default theme colors

## Notes

- The FastAPI backend must be running and accessible for the chat functionality to work
- Static assets are served locally by the Streamlit app
- This app works well for both local development and deployment on Streamlit Cloud 