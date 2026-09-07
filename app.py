import streamlit as st
from openai import OpenAI

# Page setup
st.set_page_config(page_title="Christian Companion", page_icon="✝️")
st.title("✝️ Christian Faith & Comfort Companion")
st.caption("A space for biblical encouragement, guidance, and prayer.")

# Secure API Key input
api_key = st.sidebar.text_input("Enter OpenAI API Key", type="password")

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

if not api_key:
    st.info("Please enter your OpenAI API key in the sidebar to begin.", icon="🔑")
    st.stop()

client = OpenAI(api_key=api_key)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "assistant", "content": "Grace and peace to you! I am here to listen, offer biblical encouragement, pray with you, or walk through whatever is on your heart today. How can I support you right now?"}
    ]

# Display chat messages (excluding the system prompt)
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# User input
if prompt := st.chat_input("Share what's on your mind..."):
    # Add user message to history and UI
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate assistant response
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
            stream=True,
        )
        response = st.write_stream(stream)
    
    # Add assistant response to history
    st.session_state.messages.append({"role": "assistant", "content": response})
