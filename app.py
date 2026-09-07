import streamlit as st
import google.generativeai as genai

# Page setup
st.set_page_config(page_title="Christian Companion", page_icon="✝️")
st.title("✝️ Christian Faith & Comfort Companion")
st.caption("A space for biblical encouragement, guidance, and prayer.")

# Retrieve API Key automatically from Streamlit Secrets or sidebar input
api_key = st.secrets.get("GEMINI_API_KEY") or st.sidebar.text_input("Enter Gemini API Key", type="password")

if not api_key:
    st.info("Please enter your Gemini API key in the sidebar, or add GEMINI_API_KEY to Streamlit Secrets.", icon="🔑")
    st.stop()

# Configure Gemini API
genai.configure(api_key=api_key)

# Function to dynamically pick a valid available model
@st.cache_resource
def get_working_model_name():
    try:
        available_models = [
            m.name for m in genai.list_models() 
            if 'generateContent' in m.supported_generation_methods
        ]
        # Prefer gemini-1.5-flash or gemini-2.0-flash if listed
        for preferred in ["models/gemini-1.5-flash", "models/gemini-2.0-flash", "models/gemini-1.5-pro"]:
            if preferred in available_models:
                return preferred
        if available_models:
            return available_models[0]
    except Exception:
        pass
    return "gemini-1.5-flash-latest"

# System Prompt defining the bot's persona and behavior
SYSTEM_PROMPT = """
You are a loving, wise, and deeply grounded Christian mentor and companion. 
Your goal is to offer emotional support, spiritual encouragement, and godly wisdom.

Key Guidelines:
1. Always base your advice on Scripture, pointing back to the character and teachings of Jesus Christ.
2. Offer comfort, empathy, and prayer when the user is struggling, hurting, or anxious.
3. Gently correct the user with truth and love if they express attitudes, beliefs, or actions that contradict Scripture (Ephesians 4:15).
4. Rejoice, encourage, and cheer them on when they do what is right, honoring their spiritual growth.
5. Maintain a warm, compassionate, humble, and respectful tone at all times.
6. Frequently incorporate relevant Bible verses to support your points.
"""

# Initialize Gemini Chat Session in session state
if "chat" not in st.session_state:
    model_name = get_working_model_name()
    model = genai.GenerativeModel(
        model_name=model_name,
        system_instruction=SYSTEM_PROMPT
    )
    st.session_state.chat = model.start_chat(history=[])
    
    st.session_state.display_messages = [
        {
            "role": "assistant",
            "content": "Grace and peace to you! I am here to listen, offer biblical encouragement, pray with you, or walk through whatever is on your heart today. How can I support you right now?"
        }
    ]

# Display all past messages in the UI
for msg in st.session_state.display_messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Process user input
if prompt := st.chat_input("Share what's on your mind..."):
    # Display user message
    st.session_state.display_messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate assistant response using the persistent chat session
    with st.chat_message("assistant"):
        try:
            response = st.session_state.chat.send_message(prompt)
            st.markdown(response.text)
            st.session_state.display_messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Error communicating with Gemini: {e}")
