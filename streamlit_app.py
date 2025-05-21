import streamlit as st
import streamlit.components.v1 as components
import os
import base64
from globalog import LOG # Import globalog
import shutil

# --- Configuration for Streamlit App & Widget ---
LOG.info("Streamlit App: Initializing configuration...")

# Directory structure for assets - fixed paths
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

# Full API URL for the widget config
API_FULL_URL = f"{FASTAPI_BACKEND_PUBLIC_URL}{API_BASE_PATH_ON_FASTAPI}"

# Asset paths for the frontend - need to be relative
THERAPIST_AVATAR_RELATIVE = "streamlit_app/static/widget/assets/therapist.svg"
USER_AVATAR_RELATIVE = "streamlit_app/static/widget/assets/user.svg"

# Function to read and encode files as base64
def get_file_content_as_base64(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            data = f.read()
            return base64.b64encode(data).decode()
    return None

# Function to get file content as string
def get_file_content_as_string(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return f.read()
    return None

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

# If files don't exist, show instructions with updated paths
if not widget_script_exists:
    st.warning("**Widget script not found!**\n\n"
               f"Looking for file at: {WIDGET_SCRIPT_PATH}\n\n"
               "Please make sure the widget JavaScript file is in the correct location.")

if not (therapist_avatar_exists and user_avatar_exists):
    st.warning("""
    **Missing avatar files!** Please verify:
    
    1. Therapist avatar at: streamlit_app/static/widget/assets/therapist.svg
    2. User avatar at: streamlit_app/static/widget/assets/user.svg
    """)

# --- Embed the Chat Widget ---
if widget_script_exists:
    # Read and encode the SVG files to data URLs if they exist
    therapist_avatar_data = None
    user_avatar_data = None
    
    if therapist_avatar_exists:
        therapist_avatar_data = get_file_content_as_base64(THERAPIST_AVATAR_PATH)
    
    if user_avatar_exists:
        user_avatar_data = get_file_content_as_base64(USER_AVATAR_PATH)
    
    # Construct avatar URLs - either as data URLs or placeholder
    therapist_avatar_url = f"data:image/svg+xml;base64,{therapist_avatar_data}" if therapist_avatar_data else "https://via.placeholder.com/40"
    user_avatar_url = f"data:image/svg+xml;base64,{user_avatar_data}" if user_avatar_data else "https://via.placeholder.com/40"
    
    # Get the widget script content
    widget_script = get_file_content_as_string(WIDGET_SCRIPT_PATH)
    
    # Debug script length
    script_length = len(widget_script) if widget_script else 0
    st.sidebar.info(f"Widget script loaded: {script_length} characters")
    
    # Create the HTML content - following the structure from example.html
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Therapist Chat Widget Example</title>
  <style>
    body {{
      font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial, sans-serif;
      line-height: 1.6;
      margin: 0;
      padding: 20px;
      color: #333;
      max-width: 800px;
      margin: 0 auto;
    }}
    h1 {{
      margin-top: 40px;
      border-bottom: 1px solid #eee;
      padding-bottom: 10px;
    }}
    p {{
      margin-bottom: 20px;
    }}
    .example-section {{
      margin: 40px 0;
      padding: 20px;
      background-color: #f9f9f9;
      border-radius: 8px;
      border: 1px solid #eee;
    }}
    .example-button {{
      display: inline-block;
      padding: 10px 15px;
      background-color: #6B4BB5;
      color: white;
      border: none;
      border-radius: 4px;
      cursor: pointer;
      margin-right: 10px;
      margin-bottom: 10px;
      font-size: 14px;
    }}
    .example-button:hover {{
      background-color: #5a3fa0;
    }}
    .code-block {{
      background-color: #f5f5f5;
      padding: 15px;
      border-radius: 4px;
      overflow-x: auto;
      font-family: monospace;
      margin: 20px 0;
    }}
    #debugPanel {{
      background-color: #f8f8f8;
      border: 1px solid #ddd;
      padding: 10px;
      margin-top: 20px;
      font-family: monospace;
      max-height: 200px;
      overflow-y: auto;
    }}
    .api-config {{
      margin-top: 20px;
      padding: 10px;
      border: 1px solid #ddd;
      border-radius: 4px;
    }}
    .api-config input {{
      padding: 8px;
      width: 300px;
      margin-right: 10px;
    }}
    .api-config button {{
      padding: 8px 12px;
      background-color: #6B4BB5;
      color: white;
      border: none;
      border-radius: 4px;
      cursor: pointer;
    }}
    .language-config example-section {{
      margin-top: 20px;
      padding: 20px;
      background-color: #f9f9f9;
      border-radius: 8px;
      border: 1px solid #eee;
    }}
    .language-config label {{
      display: block;
      margin-bottom: 10px;
    }}
    .language-config select {{
      padding: 8px;
      width: 300px;
      margin-right: 10px;
    }}
    .language-config input[type="checkbox"] {{
      margin-right: 10px;
    }}
    .language-config button {{
      padding: 8px 12px;
      background-color: #6B4BB5;
      color: white;
      border: none;
      border-radius: 4px;
      cursor: pointer;
    }}
  </style>
  <script>
    // Debug script to monitor resource loading
    document.addEventListener('DOMContentLoaded', function() {{
      console.log('DOM Content Loaded');
      
      // Create debug panel
      const debugPanel = document.createElement('div');
      debugPanel.id = 'debugPanel';
      debugPanel.innerHTML = '<h3>Debug Log:</h3>';
      document.body.appendChild(debugPanel);
      
      function logMessage(msg) {{
        console.log(msg);
        const entry = document.createElement('div');
        entry.textContent = msg;
        debugPanel.appendChild(entry);
        debugPanel.scrollTop = debugPanel.scrollHeight;
      }}
      
      // Monitor all script loads
      const originalCreateElement = document.createElement;
      document.createElement = function(tagName) {{
        const element = originalCreateElement.call(document, tagName);
        if (tagName.toLowerCase() === 'script') {{
          logMessage('Script element created');
          const originalSetAttribute = element.setAttribute;
          element.setAttribute = function(name, value) {{
            if (name === 'src') {{
              logMessage(`Script src attribute set to: ${{value}}`);
            }}
            return originalSetAttribute.call(this, name, value);
          }}
          // Monitor script errors
          element.addEventListener('error', function(e) {{
            logMessage(`ERROR loading script: ${{e.target.src}}`);
          }});
          element.addEventListener('load', function(e) {{
            logMessage(`SUCCESS loading script: ${{e.target.src}}`);
          }});
        }}
        return element;
      }};
      
      // Monitor fetch requests
      const originalFetch = window.fetch;
      window.fetch = function(input, init) {{
        logMessage(`Fetch request to: ${{input}}`);
        return originalFetch.apply(this, arguments)
          .then(response => {{
            logMessage(`Fetch response ${{response.status}} from: ${{input}}`);
            return response;
          }})
          .catch(error => {{
            logMessage(`Fetch ERROR from: ${{input}} - ${{error.message}}`);
            throw error;
          }});
      }};
      
      // Monitor XMLHttpRequest
      const originalXhrOpen = XMLHttpRequest.prototype.open;
      XMLHttpRequest.prototype.open = function(method, url) {{
        this.addEventListener('load', function() {{
          logMessage(`XHR ${{method}} response ${{this.status}} from: ${{url}}`);
        }});
        this.addEventListener('error', function() {{
          logMessage(`XHR ${{method}} ERROR from: ${{url}}`);
        }});
        logMessage(`XHR ${{method}} request to: ${{url}}`);
        return originalXhrOpen.apply(this, arguments);
      }};

      // Check for broken scripts on window errors
      window.addEventListener('error', function(e) {{
        if (e.filename) {{
          logMessage(`ERROR in script: ${{e.filename}} - ${{e.message}}`);
        }}
      }});
    }});
  </script>

  <!-- Initialize the widget configuration before loading the script -->
  <script>
    window.TherapistChatConfig = {{
      apiBase: '{API_FULL_URL}',  // Ensure this includes /api
      primaryColor: '#6B4BB5',
      secondaryColor: '#FFFFFF',
      position: 'bottom-right',
      initialState: 'collapsed',
      placeholder: 'שאל שאלה את ד״ר רוני...',
      therapistAvatar: '{THERAPIST_AVATAR_RELATIVE}',
      userAvatar: '{USER_AVATAR_RELATIVE}',
      title: 'Therapist Chat',
      fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif',
      enableMarkdown: true,
      language: 'he', // Default to English
      forceRTL: false // Default to LTR unless language is 'he'
    }};
  </script>
</head>
<body>
  <h1>Therapist Chat Widget Demo</h1>
  <p>This page demonstrates the therapist chat widget with markdown formatting support.</p>

  <div class="api-config">
    <h3>API Backend Configuration</h3>
    <p>Enter the URL of your FastAPI backend server (including the /api base path):</p>
    <input type="text" id="apiBaseInput" value="{API_FULL_URL}" placeholder="e.g., http://localhost:8000/api">
    <button onclick="updateApiBase()">Update API URL</button>
    <button onclick="testApiConnection()">Test Connection</button>
    <div id="apiStatus" style="margin-top: 10px; padding: 5px;"></div>
  </div>

  <div class="language-config example-section">
    <h3>Language & RTL Configuration</h3>
    <label for="languageSelect">Select Language:</label>
    <select id="languageSelect">
      <option value="en">English (LTR)</option>
      <option value="he" selected>Hebrew (RTL)</option>
    </select>
    <label for="forceRTLCheckbox" style="margin-left: 15px;">Force RTL:</label>
    <input type="checkbox" id="forceRTLCheckbox">
    <button onclick="updateLanguageSettings()" style="margin-left: 10px;">Apply Language</button>
  </div>

  <div class="example-section">
    <h2>Try Markdown Examples</h2>
    <p>Click on these buttons to see how different markdown formatting renders in the chat:</p>
    
    <button class="example-button" onclick="simulateResponse('text-formatting')">Text Formatting</button>
    <button class="example-button" onclick="simulateResponse('lists')">Lists</button>
    <button class="example-button" onclick="simulateResponse('headings')">Headings</button>
    <button class="example-button" onclick="simulateResponse('blockquotes')">Blockquotes</button>
    <button class="example-button" onclick="simulateResponse('code')">Code Examples</button>
    <button class="example-button" onclick="simulateResponse('links')">Links</button>
    <button class="example-button" onclick="simulateResponse('combined')">Combined Example</button>
  </div>

  <div class="example-section">
    <h2>Widget Configuration</h2>
    <p>The widget is configured with the following options:</p>
    <div class="code-block">
      <pre id="configDisplay">
{{
  apiBase: '{API_FULL_URL}',
  primaryColor: '#6B4BB5',
  secondaryColor: '#FFFFFF',
  position: 'bottom-right',
  initialState: 'collapsed',
  placeholder: 'שאל שאלה את ד״ר רוני...',
  therapistAvatar: '{THERAPIST_AVATAR_RELATIVE}',
  userAvatar: '{USER_AVATAR_RELATIVE}',
  title: 'Therapist Chat',
  fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif',
  enableMarkdown: true,
  language: 'he',
  forceRTL: false
}}</pre>
    </div>
  </div>

  <script>{widget_script}</script>
  <script>
    // Function to update the API base URL
    function updateApiBase() {{
      const newApiBase = document.getElementById('apiBaseInput').value.trim();
      if (newApiBase) {{
        // Update the config
        window.TherapistChatConfig.apiBase = newApiBase;
        
        updateConfigDisplay(); // Update displayed config
        reinitializeWidget(); // Reinitialize the widget
      }}
    }}

    // Function to update language settings
    function updateLanguageSettings() {{
      const selectedLanguage = document.getElementById('languageSelect').value;
      const forceRTL = document.getElementById('forceRTLCheckbox').checked;

      window.TherapistChatConfig.language = selectedLanguage;
      window.TherapistChatConfig.forceRTL = forceRTL;

      updateConfigDisplay(); // Update displayed config
      reinitializeWidget(); // Reinitialize the widget
    }}

    // Function to update the displayed config in the pre block
    function updateConfigDisplay() {{
      const configDisplay = document.getElementById('configDisplay');
      if (configDisplay) {{
        configDisplay.textContent = JSON.stringify(window.TherapistChatConfig, null, 2);
      }}
    }}

    // Function to reinitialize the widget
    function reinitializeWidget() {{
      if (window.TherapistChat && window.TherapistChat.init) {{
        const existingWidget = document.getElementById('therapist-chat-widget-container');
        if (existingWidget) {{
          existingWidget.remove();
        }}
        window.TherapistChat.init(window.TherapistChatConfig);
      }} else {{
        console.error('TherapistChat object not found or init method not available for reinitialization');
      }}
    }}

    // Mock responses for different markdown examples
    const mockResponses = {{
      'text-formatting': 
`Here are some text formatting examples:

**Bold text** for emphasis
*Italic text* for subtle emphasis
***Bold and italic*** for strong emphasis
~~Strikethrough~~ for indicating removed content

You can also use __underscores__ for *_mixed_* formatting.`,

      'lists': 
`Here are some list examples:

Unordered List:
* Item 1
* Item 2
  * Nested item 2.1
  * Nested item 2.2
* Item 3

Ordered List:
1. First step
2. Second step
   1. Substep 2.1
   2. Substep 2.2
3. Third step

Task List:
- [x] Completed task
- [ ] Pending task
- [ ] Another pending task`,

      'headings': 
`# Heading Level 1
## Heading Level 2
### Heading Level 3
#### Heading Level 4
##### Heading Level 5
###### Heading Level 6

Headings help to organize content hierarchically.`,

      'blockquotes': 
`Here's how blockquotes look:

> This is a single blockquote
> It can continue across multiple lines

> Blockquotes can also be nested:
> > This is a nested blockquote
> > > And another level of nesting

Blockquotes are useful for highlighting important information or quoting someone.`,

      'code': 
`Here are code formatting examples:

Inline code: \`const name = "Therapist";\`

Code blocks:

\`\`\`javascript
function greet(name) {{
  return "Hello, " + name + "!";
}}

const message = greet("Client");
console.log(message);
\`\`\`

\`\`\`python
def calculate_sentiment(text):
    # Analyze sentiment
    return "positive"
\`\`\``,

      'links': 
`Here are examples of links:

[Visit our website](https://example.com)

[Learn more about therapy](https://example.com/therapy)

Reference-style links make text more readable:
[This guide][1] has more information.

[1]: https://example.com/guide`,

      'combined': 
`# Relationship Communication Guide

## Common Communication Patterns

Good communication is **vital** for healthy relationships. Here are some patterns to recognize:

1. **Active Listening**
   * Maintain eye contact
   * Avoid interrupting
   * Ask clarifying questions

2. **"I" Statements**
   Instead of: "You always ignore me!"
   Try: "I feel unheard when our conversations are cut short."

> "The single biggest problem in communication is the illusion that it has taken place." - George Bernard Shaw

### Communication Exercise

Try this simple exercise with your partner:

\`\`\`
1. Set a timer for 5 minutes
2. Person A speaks without interruption
3. Person B summarizes what they heard
4. Switch roles
\`\`\`

[Learn more about effective communication](https://example.com)

Remember that *practice* makes progress!`
    }};

    // Function to simulate response from the therapist
    function simulateResponse(exampleType) {{
      // First open the widget if it's collapsed
      if (window.TherapistChat) {{
        window.TherapistChat.open();
        
        // Simulate sending a message after a brief delay
        setTimeout(() => {{
          if (document.querySelector('.therapist-chat-input')) {{
            // Set a fake user message
            const input = document.querySelector('.therapist-chat-input');
            input.value = `Show me an example of ${{exampleType}} formatting`;
            
            // Find and click the send button
            const sendButton = document.querySelector('.therapist-chat-send-button');
            if (sendButton) {{
              sendButton.click();
              
              // Simulate a response from the chatbot after a short delay
              setTimeout(() => {{
                // Mock server response
                const mockServerResponse = {{
                  thread_id: "demo-thread-123",
                  response: mockResponses[exampleType] || "I don't have an example for that format."
                }};
                
                // Manually call the display logic
                const messagesArea = document.querySelector('.therapist-chat-messages-area');
                if (messagesArea) {{
                  // Remove loading indicator if any
                  const loadingIndicator = document.querySelector('.therapist-chat-loading-indicator');
                  if (loadingIndicator) loadingIndicator.remove();
                  
                  // Create and append the therapist message
                  const messageEl = document.createElement('div');
                  messageEl.className = 'therapist-chat-message assistant-message';
                  
                  const avatarEl = document.createElement('div');
                  avatarEl.className = 'therapist-chat-avatar';
                  avatarEl.style.backgroundImage = 'url({THERAPIST_AVATAR_RELATIVE})';
                  
                  const bubbleEl = document.createElement('div');
                  bubbleEl.className = 'therapist-chat-message-bubble';
                  
                  // Use marked.js if loaded
                  if (window.marked) {{
                    bubbleEl.innerHTML = window.marked.parse(mockServerResponse.response);
                  }} else {{
                    bubbleEl.innerHTML = mockServerResponse.response.replace(/\\n/g, '<br>');
                  }}
                  
                  messageEl.appendChild(avatarEl);
                  messageEl.appendChild(bubbleEl);
                  messagesArea.appendChild(messageEl);
                  
                  // Scroll to bottom
                  messagesArea.scrollTop = messagesArea.scrollHeight;
                  
                  // Enable send button
                  const sendButton = document.querySelector('.therapist-chat-send-button');
                  if (sendButton) sendButton.disabled = false;
                }}
              }}, 1500);
            }}
          }}
        }}, 500);
      }}
    }}

    // Test API connectivity
    function testApiConnection() {{
      const apiBase = document.getElementById('apiBaseInput').value.trim();
      const statusEl = document.getElementById('apiStatus');
      statusEl.innerHTML = 'Testing connection...';
      statusEl.style.backgroundColor = '#f8f9fa';

      // Format the URL properly
      const apiUrl = apiBase.includes('://') ? `${{apiBase}}/healthz` : `http://${{apiBase}}/healthz`;
      
      // Show URL being tested in debug panel
      if (typeof logMessage === 'function') {{
        logMessage(`Testing API connection to: ${{apiUrl}}`);
      }}

      fetch(apiUrl, {{
        method: 'GET',
        headers: {{
          'Content-Type': 'application/json'
        }},
        mode: 'cors'
      }})
      .then(response => {{
        if (response.ok) {{
          return response.json().then(data => {{
            statusEl.innerHTML = 'Connection successful! ✅<br>API Status: ' + (data.status || 'OK');
            statusEl.style.backgroundColor = '#d4edda';
            return;
          }});
        }}
        throw new Error(`Status: ${{response.status}} ${{response.statusText}}`);
      }})
      .catch(error => {{
        console.error('API connection test failed:', error);
        statusEl.innerHTML = `Connection failed ❌<br>${{error.message}}`;
        statusEl.style.backgroundColor = '#f8d7da';
      }});
    }}

    // Document ready function to test connection on load
    document.addEventListener('DOMContentLoaded', function() {{
      setTimeout(testApiConnection, 1000); // Delay slightly to ensure page is fully loaded
      
      // Set the language selector to match the initial config
      document.getElementById('languageSelect').value = 'he';
    }});
  </script>
</body>
</html> 
    """
    
    # Embed the HTML with the script directly in the page
    components.html(html_content, height=600, scrolling=True)
else:
    st.error(f"Widget script not found at: {WIDGET_SCRIPT_PATH}")

st.markdown("--- ")
st.markdown("### Disclaimer")
st.markdown("This is a demo application. Information provided should not be considered professional advice.") 