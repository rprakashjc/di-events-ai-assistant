# --- Streamlit UI for Bot Interaction ---

import streamlit as st
import requests

st.title("Event Assistant Bot")

if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

user_input = st.text_input("Ask a question:", key="user_input")

if st.button("Send") and user_input:
    st.session_state['chat_history'].append(("user", user_input))
    try:
        response = requests.post("http://localhost:5000/question", json={"prompt": user_input})
        if response.ok:
            llm_response = response.json().get("llm_response", "No response")
        else:
            llm_response = f"Error: {response.status_code}"
    except Exception as e:
        llm_response = f"Request failed: {e}"
    st.session_state['chat_history'].append(("bot", llm_response))
    #st.experimental_rerun()

for role, msg in st.session_state['chat_history']:
    if role == "user":
        st.markdown(f"**You:** {msg}")
    else:
        st.markdown(f"**Bot:** {msg}")
