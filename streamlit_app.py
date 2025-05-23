# --- Streamlit UI for Bot Interaction ---

import streamlit as st
import requests

# Add a sidebar
st.sidebar.title("JumpCloud Directory Insights Assistant")
st.sidebar.markdown("""
Interact with the JumpCloud Directory Insights Event Assistant. Ask questions about events, logins, software, and more!
- **Ask about recent events:** "What are the recent admin login attempts?"
- **Inquire about specific actions:** "show details about softwares added in last week"
- **Request event summaries:** "List all failed login attempts in the last 24 hours."
- **Get details on specific events:** "find any admin update event happening in last 2 days"
- **Explore user activities:** "List all admin lockouts in the last 15 days."
- **Get help with event types:** "What are the available event types?"
- **Get help with event schemas:** "What is the schema for user login attempts?"
""")

# Main chat UI with scrollable chat history
st.title("JumpCloud Directory Insights Assistant")

if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

user_input = st.text_input("Ask a Question", key="user_input", placeholder="Ask a question about DI events")

# Remove Send button and only allow pressing Enter to send
if user_input and st.session_state.get('last_user_input') != user_input:
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
    st.session_state['last_user_input'] = user_input
    #st.experimental_rerun()

# Make chat history scrollable and visually appealing
chat_html = """
<style>
body {
    background: linear-gradient(135deg, #e0e7ff 0%, #f9fafb 100%);
}
.chat-container {
    height: 300px;
    overflow-y: auto;
    border: 1px solid #b6b6b6;
    padding: 10px;
    background: #f4f8fb;
    border-radius: 12px;
    margin-bottom: 1em;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}
.user-msg {
    color: #1a73e8;
    background: #e3f0fc;
    padding: 10px 16px;
    border-radius: 16px;
    margin-bottom: 10px;
    text-align: right;
    font-size: 1.05em;
    max-width: 80%;
    margin-left: 20%;
    box-shadow: 0 1px 4px rgba(26,115,232,0.07);
}
.bot-msg {
    color: #222;
    background: #eafbe7;
    border-left: 4px solid #34a853;
    padding: 10px 16px;
    border-radius: 16px;
    margin-bottom: 10px;
    text-align: left;
    font-size: 1.05em;
    max-width: 80%;
    margin-right: 20%;
    box-shadow: 0 1px 4px rgba(52,168,83,0.07);
}
</style>
<div>
"""
for role, msg in st.session_state['chat_history']:
    if role == "user":
        chat_html += f"<div class='user-msg'>{msg}</div>"
    else:
        chat_html += f"<div class='bot-msg'>{msg}</div>"
chat_html += "</div>"
st.markdown(chat_html, unsafe_allow_html=True)
