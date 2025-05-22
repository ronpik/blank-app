import streamlit as st
import os
from pathlib import Path
import asyncio
from openai import AsyncOpenAI
from typing import Dict, List, Optional, Any, Tuple, Union
from globalog import LOG
import uuid
import time

# Configuration and settings
st.set_page_config(
    page_title="ד״ר רוני - AI Relationship Coach",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Environment variables
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", st.secrets.get("OPENAI_API_KEY", ""))
ASSISTANT_ID = os.environ.get("ASSISTANT_ID", st.secrets.get("ASSISTANT_ID", ""))
VECTOR_STORE_ID = os.environ.get("VECTOR_STORE_ID", st.secrets.get("VECTOR_STORE_ID", ""))
MAX_RETRIES = int(os.environ.get("MAX_RETRIES", st.secrets.get("MAX_RETRIES", 3)))
POLL_INTERVAL = float(os.environ.get("POLL_INTERVAL", st.secrets.get("POLL_INTERVAL", 1)))
MAX_POLL_ATTEMPTS = int(os.environ.get("MAX_POLL_ATTEMPTS", st.secrets.get("MAX_POLL_ATTEMPTS", 30)))

# Paths
CONTENT_DIR = Path(__file__).parent 
ASSETS_FOLDER = CONTENT_DIR / "streamlit_app" / "static" / "widget" / "assets"
THERAPIST_AVATAR_PATH = ASSETS_FOLDER / "icon_ksharim.jpg"
THERAPIST_AVATAR_URL = "https://cdn.jsdelivr.net/gh/rony-ai/rony-assets@main/assets/therapist.svg"
USER_AVATAR_PATH = ASSETS_FOLDER / "user.svg"

# Custom CSS for RTL and styling
st.markdown("""
<style>
    /* Global RTL direction for the entire app */
    body {
        direction: rtl !important;
    }
    .main .block-container {
        max-width: 1000px;
        padding: 2rem;
        direction: rtl !important;
    }
    
    /* Styling for the title */
    .title {
        text-align: center;
        color: #9C3EE8;
        font-size: 2em;
        margin-bottom: 20px;
        font-weight: bold;
    }
    
    /* Chat styling */
    .stChatFloatingInputContainer {
        bottom: 20px !important;
        background-color: rgba(255, 255, 255, 0.9) !important;
        padding: 10px !important;
        border-radius: 10px !important;
        border: 1px solid #eaeaea !important;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1) !important;
    }
    
    /* Override chat message avatars and styling */
    .stChatMessage .avatar {
        width: 40px !important;
        height: 40px !important;
        border-radius: 50% !important;
        margin: 0 10px !important;
        padding: 2px !important;
        background-color: white !important;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1) !important;
    }
    
    /* User chat bubble */
    .stChatMessage[data-testid="stChatMessage-user"] .content p {
        background-color: #E8E8E8 !important;
        border: 1px solid #D3D3D3 !important;
        color: #333 !important;
        border-radius: 18px !important;
        border-top-left-radius: 5px !important;
        padding: 12px 18px !important;
        text-align: right !important;
    }
    
    /* Assistant chat bubble */
    .stChatMessage[data-testid="stChatMessage-assistant"] .content p {
        background-color: #FFFFFF !important;
        border: 1px solid rgba(156, 62, 232, 0.3) !important;
        color: #333 !important;
        border-radius: 18px !important;
        border-top-right-radius: 5px !important;
        padding: 12px 18px !important;
        text-align: right !important;
    }
    
    /* Chat input styling */
    .stChatInputContainer {
        direction: rtl !important;
        padding: 10px !important;
        border-radius: 12px !important;
        border: 1px solid #eaeaea !important;
    }
    
    /* RTL for inputs */
    input[type="text"] {
        direction: rtl !important;
        text-align: right !important;
    }
    
    /* Make chat container taller */
    .stChatContainer {
        height: 70vh !important;
        overflow-y: auto !important;
        margin-bottom: 20px !important;
    }
    
    /* Style sidebar */
    .css-1d391kg {
        direction: rtl !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "thread_id" not in st.session_state:
    st.session_state.thread_id = None

if "client" not in st.session_state:
    st.session_state.client = None
    st.session_state.client_initialized = False

if "processing_message" not in st.session_state:
    st.session_state.processing_message = False

# OpenAI Assistants API Service
class OpenAIService:
    """Service for interacting with OpenAI's Assistants API."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the OpenAI service."""
        self.api_key = api_key or OPENAI_API_KEY
        if not self.api_key or self.api_key == "your_openai_api_key_here":
            LOG.error("OpenAI API key is not configured or is a placeholder.")
            raise ValueError("OpenAI API key is not configured.")

        self.client = AsyncOpenAI(api_key=self.api_key)
        self.assistant_id = ASSISTANT_ID
        self.vector_store_id = VECTOR_STORE_ID
        self.max_retries = MAX_RETRIES
        self.poll_interval = POLL_INTERVAL
        self.max_poll_attempts = MAX_POLL_ATTEMPTS
        
        LOG.info(f"OpenAIService initialized. Assistant ID: {self.assistant_id if self.assistant_id else 'Not Set'}, Vector Store ID: {self.vector_store_id if self.vector_store_id else 'Not Set'}")

    async def check_api_key(self) -> Tuple[bool, str]:
        """Check if the OpenAI API key is valid by making a lightweight call."""
        try:
            await self.client.models.list()
            LOG.info("OpenAI API key validation successful (models.list).")
            return True, "OpenAI API connection successful"
        except Exception as e:
            LOG.error(f"OpenAI API key validation failed: {type(e).__name__} - {e}")
            return False, f"OpenAI API connection failed: {type(e).__name__}"

    async def create_thread(self) -> Any:
        """Create a new thread on OpenAI."""
        LOG.info("Creating new OpenAI thread.")
        try:
            tool_resources = {}
            if self.vector_store_id:
                tool_resources = {"file_search": {"vector_store_ids": [self.vector_store_id]}}
                LOG.info(f"Creating thread with tool_resources for vector store: {self.vector_store_id}")
            
            thread_params = {}
            if tool_resources:
                thread_params["tool_resources"] = tool_resources

            thread = await self.client.beta.threads.create(**thread_params)
            LOG.info(f"Successfully created OpenAI thread ID: {thread.id}")
            return thread
        except Exception as e:
            LOG.error(f"Unexpected error creating OpenAI thread: {e}")
            raise

    async def add_message_to_thread(self, thread_id: str, content: str, role: str = "user") -> Any:
        """Add a message to an existing OpenAI thread."""
        LOG.info(f"Adding message to OpenAI thread {thread_id} with role '{role}'. Content: {content[:50]}...")
        try:
            message = await self.client.beta.threads.messages.create(
                thread_id=thread_id,
                role=role,
                content=content
            )
            LOG.info(f"Successfully added message ID {message.id} to thread {thread_id}.")
            return message
        except Exception as e:
            LOG.error(f"Unexpected error adding message to thread {thread_id}: {e}")
            raise

    async def create_run(self, thread_id: str, assistant_id: Optional[str] = None) -> Any:
        """Create a run for a thread with the specified assistant."""
        target_assistant_id = assistant_id or self.assistant_id
        if not target_assistant_id:
            LOG.error("Cannot create run: No assistant ID provided or configured.")
            raise ValueError("Assistant ID is required to create a run.")
        
        LOG.info(f"Creating run for thread {thread_id} with assistant {target_assistant_id}.")
        try:
            run_params = {"assistant_id": target_assistant_id}
            run = await self.client.beta.threads.runs.create(thread_id=thread_id, **run_params)
            LOG.info(f"Successfully created run ID {run.id} for thread {thread_id} with status {run.status}.")
            return run
        except Exception as e:
            LOG.error(f"Unexpected error creating run for thread {thread_id}: {e}")
            raise

    async def get_run_status(self, thread_id: str, run_id: str) -> Any:
        """Get the status and details of a specific run."""
        LOG.debug(f"Retrieving status for run {run_id} in thread {thread_id}.")
        try:
            run = await self.client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
            LOG.debug(f"Status for run {run.id}: {run.status}")
            return run
        except Exception as e:
            LOG.error(f"Unexpected error retrieving status for run {run_id}: {e}")
            raise

    async def poll_run_until_completion(self, thread_id: str, run_id: str) -> Any:
        """Poll a run until it reaches a terminal state (completed, failed, etc.)."""
        LOG.info(f"Polling run {run_id} in thread {thread_id} for completion...")
        attempts = 0
        
        with st.status("ד״ר רוני חושב...", expanded=True) as status:
            while attempts < self.max_poll_attempts:
                run = await self.get_run_status(thread_id, run_id)
                
                if run.status == "completed":
                    LOG.info(f"Run {run.id} completed successfully.")
                    status.update(label="ד״ר רוני סיים לחשוב!", state="complete", expanded=False)
                    return run
                elif run.status in ["failed", "cancelled", "expired", "requires_action"]:
                    LOG.error(f"Run {run.id} ended with terminal status: {run.status}. Error: {run.last_error}")
                    status.update(label=f"שגיאה: {run.status}", state="error")
                    raise Exception(f"Run failed with status: {run.status}")
                
                status.update(label=f"ד״ר רוני חושב... ({attempts + 1}/{self.max_poll_attempts})")
                LOG.debug(f"Run {run.id} status: {run.status}. Waiting {self.poll_interval}s before next poll.")
                await asyncio.sleep(self.poll_interval)
                attempts += 1
            
            status.update(label="פעולה ארכה יותר מדי זמן", state="error")
            raise TimeoutError(f"Run {run_id} timed out after {self.max_poll_attempts * self.poll_interval} seconds.")

    async def get_assistant_messages(self, thread_id: str, limit: int = 20) -> List[Any]:
        """Get messages from a thread, typically used to find the assistant's response."""
        LOG.info(f"Retrieving messages from thread {thread_id}, limit {limit}")
        try:
            list_params = {"thread_id": thread_id, "order": "desc", "limit": limit}
            messages_page = await self.client.beta.threads.messages.list(**list_params)
            LOG.info(f"Retrieved {len(messages_page.data)} messages from thread {thread_id}.")
            return messages_page.data
        except Exception as e:
            LOG.error(f"Unexpected error retrieving messages from thread {thread_id}: {e}")
            raise

    async def get_latest_assistant_response(self, thread_id: str, run_id: str) -> Optional[str]:
        """Get the text of the latest assistant message after a run."""
        LOG.info(f"Getting latest assistant response for thread {thread_id} after run {run_id}")
        messages = await self.get_assistant_messages(thread_id, limit=20)
        
        for message in messages:
            if message.role == "assistant":
                if message.content and isinstance(message.content, list):
                    text_content = []
                    for content_block in message.content:
                        if content_block.type == "text":
                            text_content.append(content_block.text.value)
                    full_response = "\n".join(text_content)
                    LOG.info(f"Found assistant response in thread {thread_id}: {full_response[:100]}...")
                    return full_response
        
        LOG.warning(f"No assistant message found for thread {thread_id} after run {run_id}.")
        return None

    async def process_user_message(self, thread_id: str, user_message_content: str) -> Tuple[str, str, Optional[Dict[str, Any]]]:
        """Process a user message and get the assistant's response."""
        if not self.assistant_id:
            LOG.error("Assistant ID not set. Cannot process message.")
            raise ValueError("Assistant ID is required.")

        # 1. Add user message to the thread
        await self.add_message_to_thread(thread_id, user_message_content, role="user")

        # 2. Create a run
        run = await self.create_run(thread_id, self.assistant_id)
        
        # 3. Poll for run completion
        completed_run = await self.poll_run_until_completion(thread_id, run.id)
        
        # 4. Retrieve the latest assistant message
        assistant_response = await self.get_latest_assistant_response(thread_id, completed_run.id)
        
        run_usage_details = completed_run.usage.model_dump() if hasattr(completed_run, 'usage') and completed_run.usage else None

        if assistant_response is None:
            LOG.warning(f"Assistant did not provide a response for thread {thread_id}, run {completed_run.id}")
            return thread_id, "אני לא יכול לספק תשובה כרגע.", run_usage_details
            
        return thread_id, assistant_response, run_usage_details

# Create sidebar
st.sidebar.markdown("<h1 style='text-align: center; color: #9C3EE8;'>ד״ר רוני</h1>", unsafe_allow_html=True)
st.sidebar.markdown("<h3 style='text-align: center; direction: rtl;'>יועץ זוגיות AI</h3>", unsafe_allow_html=True)
st.sidebar.markdown("---")

# Add a new thread button
if st.sidebar.button("שיחה חדשה", use_container_width=True):
    st.session_state.thread_id = None
    st.session_state.messages = []
    st.rerun()

# Display current thread ID
if st.session_state.thread_id:
    st.sidebar.markdown(f"<p style='direction: rtl; font-size: 0.8em;'>מזהה שיחה נוכחית: {st.session_state.thread_id[:14]}...</p>", unsafe_allow_html=True)
else:
    st.sidebar.markdown("<p style='direction: rtl; font-size: 0.8em;'>שיחה חדשה תיפתח אוטומטית</p>", unsafe_allow_html=True)

# Instructions/Introduction in sidebar
with st.sidebar.expander("כיצד להשתמש ביועץ זוגיות AI", expanded=False):
    st.markdown("""
    <div style="direction: rtl; text-align: right;">
    <h3>איך להשתמש בד״ר רוני</h3>

    <p>ד״ר רוני הוא יועץ זוגיות מבוסס AI שיכול לעזור בשאלות על תקשורת, פתרון קונפליקטים, בניית קשר בריא ועוד.
    פשוט הקלידו את השאלה שלכם בתיבת הטקסט למטה וד״ר רוני יענה.</p>

    <p><strong>דוגמאות לשאלות:</strong></p>
    <ul style="padding-right: 20px;">
        <li>איך לתקשר טוב יותר עם בן/בת הזוג שלי?</li>
        <li>איך להתמודד עם ויכוחים חוזרים על אותם נושאים?</li>
        <li>טיפים לשיפור האינטימיות בקשר</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.markdown("<p style='text-align: center; font-size: 0.8em;'>*הערה: ד״ר רוני הוא יועץ AI ואינו תחליף לטיפול מקצועי.*</p>", unsafe_allow_html=True)

# Main app area
st.markdown("<h1 class='title'>ד״ר רוני | יועץ זוגיות AI</h1>", unsafe_allow_html=True)

# Initialize OpenAI client
async def initialize_client():
    """Initialize the OpenAI client and check API key validity."""
    if st.session_state.client_initialized:
        LOG.info("Client already initialized")
        return True
    
    LOG.info(st.secrets.keys())
    if not OPENAI_API_KEY:
        st.error("OpenAI API Key is missing. Please set it in your environment variables or Streamlit secrets.")
        return False
    
    try:
        st.session_state.openai_service = OpenAIService(api_key=OPENAI_API_KEY)
        valid, message = await st.session_state.openai_service.check_api_key()
        if valid:
            LOG.info("OpenAI API key validation successful.")
            st.session_state.client_initialized = True
            return True
        else:
            LOG.error(f"OpenAI API key validation failed: {message}")
            st.error(f"Failed to initialize OpenAI client: {message}")
            st.session_state.client_initialized = False
            return False
    except Exception as e:
        LOG.error(f"Unexpected error during client initialization: {e}")
        st.error(f"An unexpected error occurred during initialization: {e}")
        st.session_state.client_initialized = False
        return False

# Initialize OpenAI Service
if not st.session_state.client_initialized:
    asyncio.run(initialize_client())

# Create a new thread if needed
async def ensure_thread():
    if not st.session_state.thread_id and st.session_state.client_initialized:
        try:
            thread = await st.session_state.openai_service.create_thread()
            st.session_state.thread_id = thread.id
            LOG.info(f"Created new thread with ID: {thread.id}")
            return True
        except Exception as e:
            LOG.error(f"Failed to create thread: {e}")
            st.error("Failed to start a new conversation. Please try again later.")
            return False
    return True

# Display existing chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar=THERAPIST_AVATAR_PATH if message["role"] == "assistant" else None):
        st.markdown(message["content"])

# Process new messages
async def process_message(user_input):
    if not st.session_state.client_initialized:
        await initialize_client()
        if not st.session_state.client_initialized:
            return
    
    # Create thread if needed
    if not st.session_state.thread_id:
        thread_created = await ensure_thread()
        if not thread_created:
            return
    
    try:
        # Process the message
        thread_id, response, usage = await st.session_state.openai_service.process_user_message(
            st.session_state.thread_id, 
            user_input
        )
        
        # Add assistant response to messages and display it
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        # Display the assistant's response in UI
        with st.chat_message("assistant", avatar=THERAPIST_AVATAR_PATH):
            st.markdown(response)
        
        if usage:
            LOG.info(f"Message processing complete. Usage: {usage}")
            
    except Exception as e:
        LOG.error(f"Error processing message: {e}")
        st.error(f"Error communicating with OpenAI: {str(e)}")

# Chat input
if prompt := st.chat_input("שאל את ד״ר רוני..."):
    # Display user message
    st.chat_message("user").markdown(prompt)
    
    # Add to message history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Process the message
    asyncio.run(process_message(prompt))