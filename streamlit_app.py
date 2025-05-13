import streamlit as st
import streamlit.components.v1 as components

st.subheader("Chatbot using Vertex AI Agent Builder.")

html_code="""

<!DOCTYPE html>
<html>
<head>
  <title>Your Custom Chatbot</title>
  <style>
    body {
      background-color: lightblue;
    }
  </style>
</head>
<body>
  <h1>Your Custom Chatbot</h1>
  <p>This is a test only. Please add additional information you wish to include.</p>
</body>
</html>

<link rel="stylesheet" href="https://www.gstatic.com/dialogflow-console/fast/df-messenger/prod/v1/themes/df-messenger-default.css">
<script src="https://www.gstatic.com/dialogflow-console/fast/df-messenger/prod/v1/df-messenger.js"></script>
<df-messenger
  location="us"
  project-id="ksharim"
  agent-id="574c260b-5642-4931-8654-959f62d913b2"
  language-code="en"
  max-query-length="-1">
  <df-messenger-chat
    chat-title="מכון קשרים - ד״ר רוני">
  </df-messenger-chat>
</df-messenger>
<style>
  df-messenger {
    z-index: 999;
    position: fixed;
    --df-messenger-font-color: #000;
    --df-messenger-font-family: Google Sans;
    --df-messenger-chat-background: #f3f6fc;
    --df-messenger-message-user-background: #d3e3fd;
    --df-messenger-message-bot-background: #fff;
    bottom: 0;
    right: 0;
    top: 0;
    width: 350px;
  }
</style>
    
"""

components.html(html_code, height=650,  scrolling=True)