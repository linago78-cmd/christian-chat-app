import streamlit as st
import google.generativeai as genai

# Page setup
st.set_page_config(page_title="Christian Companion", page_icon="✝️")
st.title("✝️ Christian Faith & Comfort Companion")
st.caption("A space for biblical encouragement, guidance, and prayer.")

# Retrieve API Key automatically from Streamlit Secrets, or fall back to sidebar input
api_key = st.secrets.get("GEMINI_API_KEY") or st.sidebar.text_input("Enter Gemini API Key", type="password")

if not api_key:
    st.info("Please enter your Gemini API key in the sidebar, or add GEMINI_API_KEY to Streamlit Secrets.", icon="🔑")
    st.stop()

# Configure Gemini API
genai.configure(api_key=api_key)

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

# Initialize chat history (Gemini uses 'model' and 'user' roles)
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "model", 
            "parts": ["Grace and peace to you! I am here to listen, offer biblical encouragement, pray with you, or walk through whatever is on your heart today. How can I support you right now?"]
        }
    ]

# Display past chat messages
for message in st.session_state.messages:
    role = "assistant" if message["role"] == "model" else "user"
    with st.chat_message(role):
        st.markdown(message["parts"][0])

# User input
if prompt := st.chat_input("Share what's on your mind..."):
    # Add user message to UI and history
    st.session_state.messages.append({"role": "user", "parts": [prompt]})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Initialize Gemini model with the system prompt passed via system_instruction
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=SYSTEM_PROMPT
    )

    # Generate response
    with st.chat_message("assistant"):
        chat = model.start_chat(history=st.session_state.messages[:-1])
        response = chat.send_message(prompt)
        st.markdown(response.text)

    # Add assistant response to history
    st.session_state.messages.append({"role": "model", "parts": [response.text]})
