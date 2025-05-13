import streamlit as st
import streamlit.components.v1 as components

st.subheader("Chatbot using Vertex AI Agent Builder.")

html_code = """
<!DOCTYPE html>
<html dir="rtl" lang="he">
<head>
  <meta charset="UTF-8">
  <title>מכון קשרים - ד״ר רוני</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    /* Page base */
    body {
      margin: 0;
      padding: 0;
      background-color: #ffffff;
      font-family: Arial, sans-serif;
      color: #4B0082; /* deep purple */
      direction: rtl;
    }
    /* Header */
    header {
      display: flex;
      align-items: center;
      justify-content: center;
      background-color: #4B0082;
      padding: 16px;
    }
    header img {
      height: 48px;
      margin-left: 12px;
    }
    header .titles {
      text-align: right;
      line-height: 1.2;
    }
    header .titles h1,
    header .titles h2 {
      margin: 0;
      color: #ffffff;
    }
    header .titles h1 {
      font-size: 1.5rem;
    }
    header .titles h2 {
      font-size: 1.125rem;
      opacity: 0.9;
    }
    /* Chat widget styling */
    df-messenger {
      position: fixed;
      bottom: 20px;
      left: 20px;
      width: 350px;
      height: calc(100% - 40px);
      max-width: calc(100% - 40px);
      --df-messenger-font-color: #4B0082;
      --df-messenger-font-family: Arial, sans-serif;
      --df-messenger-chat-background: #f8f4ff;
      --df-messenger-message-user-background: #e0d4f7;
      --df-messenger-message-bot-background: #ffffff;
    }
  </style>

  <!-- Dialogflow CSS & JS -->
  <link rel="stylesheet"
        href="https://www.gstatic.com/dialogflow-console/fast/df-messenger/prod/v1/themes/df-messenger-default.css">
  <script src="https://www.gstatic.com/dialogflow-console/fast/df-messenger/prod/v1/df-messenger.js"></script>
</head>
<body>
  <header>
    <img src="https://kshareem.co.il/wp-content/uploads/2022/04/icon_ksharim.jpg"
         alt="לוגו מכון קשרים">
    <div class="titles">
      <h1>מכון קשרים</h1>
      <h2>ד״ר רוני</h2>
    </div>
  </header>

  <!-- Your chatbot -->
  <df-messenger
    location="us"
    project-id="ksharim"
    agent-id="574c260b-5642-4931-8654-959f62d913b2"
    language-code="en"
    max-query-length="-1">
    <df-messenger-chat chat-title="מכון קשרים - ד״ר רוני"></df-messenger-chat>
  </df-messenger>
</body>
<script>
    const dfMessenger = document.querySelector('df-messenger');

    function addRichContent(customPayload) {
        // Render the returned richContent array as a custom card
        dfMessenger.renderCustomCard(customPayload.richContent);
        return Promise.resolve({ status: "OK", reason: null });
    }

    // Replace with your full tool resource name:
    const toolId = 'projects/ksharim/locations/us/agents/574c260b-5642-4931-8654-959f62d913b2/tools/7bbf0864-0e65-43e1-95a3-5b7a5e445e60';
    dfMessenger.registerClientSideFunction(toolId, addRichContent.name, addRichContent);
</script>
</html>
"""

components.html(html_code, height=650, scrolling=True)