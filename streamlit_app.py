import streamlit as st
import streamlit.components.v1 as components

st.subheader("Ksharim Chatbot")

html_code = """
<!DOCTYPE html>
<html dir="rtl" lang="he">
<head>
  <meta charset="UTF-8" />
  <title>מכון קשרים – ד״ר רוני</title>
  <meta name="viewport" content="width=device-width, initial-scale=1" />

  <!-- Dialogflow Messenger CSS & JS -->
  <link
    rel="stylesheet"
    href="https://www.gstatic.com/dialogflow-console/fast/df-messenger/prod/v1/themes/df-messenger-default.css"
  />
  <script src="https://www.gstatic.com/dialogflow-console/fast/df-messenger/prod/v1/df-messenger.js"></script>

  <style>
    /* ─── Page Background ────────────────────────────────────────── */
    html, body {
      height: 100%;
      margin: 0;
      background: linear-gradient(
        135deg,
        #2c3e50 0%,
        #8e44ad 60%,
        #ecf0f1 100%
      );
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      color: #2c3e50;
      direction: rtl;
    }

    /* ─── Header ─────────────────────────────────────────────────── */
    header {
      display: flex;
      align-items: center;
      justify-content: flex-end;
      background: rgba(255,255,255,0.85);
      padding: 12px 24px;
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    header img {
      height: 50px;
      margin-left: 16px;
    }
    .titles {
      text-align: right;
    }
    .titles h1 {
      margin: 0;
      font-size: 1.6rem;
      color: #8e44ad;
    }
    .titles h2 {
      margin: 0;
      font-size: 1.2rem;
      color: #2c3e50;
    }

    /* ─── Chat Popup ─────────────────────────────────────────────── */
    df-messenger {
      position: fixed;
      bottom: 24px;
      left: 24px;
      width: 360px;
      height: calc(100% - 48px);
      border-radius: 14px;
      overflow: hidden;
      box-shadow: 0 8px 24px rgba(0,0,0,0.15);
      --df-messenger-font-color: #2c3e50;
      --df-messenger-font-family: 'Segoe UI', sans-serif;
      --df-messenger-chat-background: #ffffff;
      --df-messenger-message-user-background: #ecf0f1;
      --df-messenger-message-bot-background: #ffffff;
      --df-messenger-send-icon-color: #8e44ad;
    }
    /* Ensure multi-line cards wrap */
    df-messenger-chat-bubble::part(text) {
      white-space: pre-wrap;
    }
  </style>
</head>
<body>
  <!-- Branded Header -->
  <header>
    <img
      src="https://kshareem.co.il/wp-content/uploads/2022/04/icon_ksharim.jpg"
      alt="לוגו מכון קשרים"
    />
    <div class="titles">
      <h1>מכון קשרים</h1>
      <h2>ד״ר רוני</h2>
    </div>
  </header>

  <!-- The popup chatbot -->
  <df-messenger
    location="us-central1"
    project-id="ksharim"
    agent-id="85623c36-efc7-4b3b-a13e-7ee68aa74739"
    language-code="he-il"
    chat-title="מכון קשרים – ד״ר רוני"
    max-query-length="-1">
  </df-messenger>

  <!-- Rich-content handler for your playbook tool -->
  <script>
    function addRichContent(payload) {
      document
        .querySelector('df-messenger')
        .renderCustomCard(payload.richContent);
      return Promise.resolve({ status: 'OK' });
    }
    window.addEventListener('df-messenger-loaded', () => {
      const dfMessenger = document.querySelector('df-messenger');
      const toolId = 
        'projects/ksharim/locations/us/agents/85623c36-efc7-4b3b-a13e-7ee68aa74739/tools/98561e78-75d3-4925-af61-e792da7fef46';
      dfMessenger.registerClientSideFunction(
        toolId,
        'addRichContent',
        addRichContent
      );
    });
  </script>
</body>
</html>
"""

components.html(html_code, height=650, scrolling=True)