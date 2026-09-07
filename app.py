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

# Function to dynamically select an active model
def get_model():
    # Attempt to list active models from Google API
    try:
        available = [
            m.name for m in genai.list_models() 
            if 'generateContent' in m.supported_generation_methods
        ]
        # Check for latest flash models in preference order
        for preferred in ["models/gemini-3.6-flash", "models/gemini-2.5-flash", "gemini-3.6-flash", "gemini-2.5-flash"]:
            if preferred in available:
                return genai.GenerativeModel(model_name=preferred, system_instruction=SYSTEM_PROMPT)
        if available:
            return genai.GenerativeModel(model_name=available[0], system_instruction=SYSTEM_PROMPT)
    except Exception:
        pass
    
    # Direct fallback if listing models is restricted
    return genai.GenerativeModel(model_name="gemini-3.6-flash", system_instruction=SYSTEM_PROMPT)

# Initialize message history list
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "model",
            "parts": ["Grace and peace to you! I am here to listen, offer biblical encouragement, pray with you, or walk through whatever is on your heart today. How can I support you right now?"]
        }
    ]

# Display all past messages in UI
for msg in st.session_state.messages:
    role = "assistant" if msg["role"] == "model" else "user"
    with st.chat_message(role):
        st.markdown(msg["parts"][0])

# Process user input
if prompt := st.chat_input("Share what's on your mind..."):
    # Render user prompt
    st.session_state.messages.append({"role": "user", "parts": [prompt]})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate assistant response
    with st.chat_message("assistant"):
        try:
            model = get_model()
            
            # Pass past message history (excluding current user prompt)
            chat = model.start_chat(history=st.session_state.messages[:-1])
            response = chat.send_message(prompt)
            
            st.markdown(response.text)
            st.session_state.messages.append({"role": "model", "parts": [response.text]})
        except Exception as e:
            st.error(f"Error communicating with Gemini: {e}")
