import streamlit as st
import streamlit.components.v1 as components

st.subheader("Ksharim Chatbot")

html_code = """
<!DOCTYPE html>
# <html dir="rtl" lang="he">
<html lang="he">
<head>
  <meta charset="UTF-8">
  <title>מכון קשרים – ד״ר רוני</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  
  <link rel="stylesheet" href="https://www.gstatic.com/dialogflow-console/fast/df-messenger/prod/v1/themes/df-messenger-default.css">
<script src="https://www.gstatic.com/dialogflow-console/fast/df-messenger/prod/v1/df-messenger.js"></script>
<df-messenger
  location="us-central1"
  project-id="ksharim"
  agent-id="85623c36-efc7-4b3b-a13e-7ee68aa74739"
  language-code="he-il"
  max-query-length="-1">
  <df-messenger-chat-bubble
    chat-title="dr-roni-he">
  </df-messenger-chat-bubble>
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
    bottom: 16px;
    right: 16px;
  }
</style>
</head>

<body>
  <!-- Header with logo + titles -->
  <header>
    <img src="https://kshareem.co.il/wp-content/uploads/2022/04/icon_ksharim.jpg"
         alt="לוגו מכון קשרים">
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

  <!-- Rich content handler for playbook tool -->
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