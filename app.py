import streamlit as st
from openai import OpenAI

# Page setup
st.set_page_config(page_title="Christian Companion", page_icon="✝️")
st.title("✝️ Christian Faith & Comfort Companion")
st.caption("A space for biblical encouragement, guidance, and prayer.")

# Secure API Key input
# Retrieve API Key automatically from Secrets or fall back to sidebar input
api_key = st.secrets.get("GEMINI_API_KEY") or st.sidebar.text_input("Enter Gemini API Key", type="password")

if not api_key:
    st.info("Please enter your Gemini API key in the sidebar to begin, or add it to Streamlit Secrets.", icon="🔑")
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
