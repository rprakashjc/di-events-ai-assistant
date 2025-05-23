import gradio as gr
import requests

# Define the function to interact with the Flask backend
def chat_with_backend(message, history):
    try:
        response = requests.post("http://localhost:5000/question", json={"prompt": message})
        if response.ok:
            llm_response = response.json().get("llm_response", "No response")
        else:
            llm_response = f"Error: {response.status_code}"
    except Exception as e:
        llm_response = f"Request failed: {e}"
    return llm_response

iface = gr.ChatInterface(
    fn=chat_with_backend,
    type="messages",
    title="JumpCloud Directory Insights Event Assistant",
    description="Ask questions about JumpCloud Directory Insights events.",
    theme="light",
    autofocus=False,
    # examples=[
    #     ["What are the recent admin login attempts?", "What are the recent user signups?", "Show me all software added in the last 7 days."],
    #     ["List all failed login attempts in the last 24 hours.", "What are the recent password reset requests?"],
    #     ["List all admin lockouts in the last month."]
    # ],
    # cache_examples=True,
    #textbox=gr.Textbox(label="Ask a question:"),
    textbox=gr.Textbox(placeholder="Ask me to about DI events", container=False, scale=7),
)

iface.launch()
