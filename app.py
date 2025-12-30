import streamlit as st
import google.generativeai as genai

# --------------------------
# Page Config
# --------------------------
st.set_page_config(
    page_title="Gemini Chat",
    page_icon="🤖",
    layout="centered",
)

st.title("Gemini Flash Chat 🤖")

# --------------------------
# API Configuration
# --------------------------
# SECURE FIX: Load key from secrets
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
except Exception as e:
    st.error("Missing API Key. Please configure .streamlit/secrets.toml")
    st.stop()

# Use the model (Ensure this model name is valid in your region)
MODEL_NAME = "gemini-1.5-flash" 
model = genai.GenerativeModel(MODEL_NAME)

# --------------------------
# Initialize Chat History
# --------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# --------------------------
# Display Previous Messages
# --------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --------------------------
# Chat Handler
# --------------------------
if user_input := st.chat_input("Type your message here..."):
    # 1. Display User Message
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # 2. Prepare History for Gemini
    gemini_history = []
    for msg in st.session_state.messages[:-1]:
        role = "user" if msg["role"] == "user" else "model"
        gemini_history.append({"role": role, "parts": [msg["content"]]})

    # 3. Generate Response
    try:
        chat = model.start_chat(history=gemini_history)
        
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            
            response = chat.send_message(user_input, stream=True)
            for chunk in response:
                full_response += chunk.text
                message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
        
        st.session_state.messages.append({"role": "assistant", "content": full_response})

    except Exception as e:
        st.error(f"Error: {e}")