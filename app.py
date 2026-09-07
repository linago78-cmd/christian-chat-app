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

# System Prompt with locked NIV translation
SYSTEM_PROMPT = """
You are a loving, wise, and deeply grounded Christian mentor and companion. 
Your goal is to offer emotional support, spiritual encouragement, and godly wisdom.

Key Guidelines:
1. Always base your advice on Scripture, pointing back to the character and teachings of Jesus Christ.
2. Quote scripture and reference biblical passages using the **NIV (New International Version)** translation.
3. Offer comfort, empathy, and prayer when the user is struggling, hurting, or anxious.
4. Gently correct the user with truth and love if they express attitudes, beliefs, or actions that contradict Scripture (Ephesians 4:15).
5. Rejoice, encourage, and cheer them on when they do what is right, honoring their spiritual growth.
6. Maintain a warm, compassionate, humble, and respectful tone at all times.
"""

# Function to dynamically select an active model
def get_model():
    try:
        available = [
            m.name for m in genai.list_models() 
            if 'generateContent' in m.supported_generation_methods
        ]
        for preferred in ["models/gemini-3.6-flash", "models/gemini-2.5-flash", "gemini-3.6-flash", "gemini-2.5-flash"]:
            if preferred in available:
                return genai.GenerativeModel(model_name=preferred, system_instruction=SYSTEM_PROMPT)
        if available:
            return genai.GenerativeModel(model_name=available[0], system_instruction=SYSTEM_PROMPT)
    except Exception:
        pass
    
    return genai.GenerativeModel(model_name="gemini-3.6-flash", system_instruction=SYSTEM_PROMPT)

# Sidebar Clear Chat Button
if st.sidebar.button("🗑️ Clear Chat History", use_container_width=True):
    st.session_state.messages = [
        {
            "role": "model",
            "parts": ["Grace and peace to you! I am here to listen, offer biblical encouragement, pray with you, or walk through whatever is on your heart today. How can I support you right now?"]
        }
    ]
    st.rerun()

# Initialize message history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "model",
            "parts": ["Grace and peace to you! I am here to listen, offer biblical encouragement, pray with you, or walk through whatever is on your heart today. How can I support you right now?"]
        }
    ]

# Display past messages
for msg in st.session_state.messages:
    role = "assistant" if msg["role"] == "model" else "user"
    with st.chat_message(role):
        st.markdown(msg["parts"][0])

# Quick Action Buttons
st.markdown("---")
st.write("✨ **Quick Requests:**")
col1, col2, col3 = st.columns(3)

prompt_to_send = None

with col1:
    if st.button("📖 Daily Verse", use_container_width=True):
        prompt_to_send = "Please share an encouraging Bible verse from the NIV translation for today, along with a short reflection on how to apply it."

with col2:
    if st.button("🙏 Pray with Me", use_container_width=True):
        prompt_to_send = "Please write a heartfelt prayer for peace, wisdom, and strength today."

with col3:
    if st.button("🕊️ Seek Comfort", use_container_width=True):
        prompt_to_send = "I am feeling overwhelmed today. Please share some biblical encouragement and comfort from the NIV scriptures."

# Capture typed input if no button was clicked
typed_prompt = st.chat_input("Share what's on your mind...")
if typed_prompt:
    prompt_to_send = typed_prompt

# Process input (from button or text box)
if prompt_to_send:
    st.session_state.messages.append({"role": "user", "parts": [prompt_to_send]})
    with st.chat_message("user"):
        st.markdown(prompt_to_send)

    with st.chat_message("assistant"):
        try:
            model = get_model()
            chat = model.start_chat(history=st.session_state.messages[:-1])
            response = chat.send_message(prompt_to_send)
            
            st.markdown(response.text)
            st.session_state.messages.append({"role": "model", "parts": [response.text]})
            st.rerun()
        except Exception as e:
            st.error(f"Error communicating with Gemini: {e}")
