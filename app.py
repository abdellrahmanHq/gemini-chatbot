
#genai.configure(api_key="AIzaSyCUmCGyFr6E2jcW7Mu891X6gYaif_y3huw")

import streamlit as st
import google.generativeai as genai

# --------------------------
# Page Config
# --------------------------
st.set_page_config(
    page_title="Gemini 2.5 Chat",
    page_icon="🤖",
    layout="centered",
)

st.title("Gemini 2.5 Flash Chat 🤖")

# --------------------------
# API Configuration
# --------------------------
# Replace this with your actual key
GOOGLE_API_KEY = "AIzaSyCUmCGyFr6E2jcW7Mu891X6gYaif_y3huw" 
genai.configure(api_key=GOOGLE_API_KEY)

# Use the model you found in your list
MODEL_NAME = "gemini-2.5-flash"
model = genai.GenerativeModel(MODEL_NAME)

# --------------------------
# Initialize Chat History
# --------------------------
# We store messages in Streamlit session state
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
    # Add user message to Streamlit history
    st.session_state.messages.append({"role": "user", "content": user_input})

    # 2. Prepare History for Gemini (Context Memory)
    # We must convert Streamlit format (user/assistant) to Gemini format (user/model)
    gemini_history = []
    for msg in st.session_state.messages[:-1]: # Skip the last one (current input)
        role = "user" if msg["role"] == "user" else "model"
        gemini_history.append({"role": role, "parts": [msg["content"]]})

    # 3. Generate Response
    try:
        # Initialize chat with history
        chat = model.start_chat(history=gemini_history)
        
        with st.chat_message("assistant"):
            # Create a placeholder for streaming text
            message_placeholder = st.empty()
            full_response = ""
            
            # Stream the response
            response = chat.send_message(user_input, stream=True)
            for chunk in response:
                full_response += chunk.text
                # Add a blinking cursor effect
                message_placeholder.markdown(full_response + "▌")
            
            # Final update without cursor
            message_placeholder.markdown(full_response)
        
        # 4. Add Assistant Message to History
        st.session_state.messages.append({"role": "assistant", "content": full_response})

    except Exception as e:
        st.error(f"Error: {e}")