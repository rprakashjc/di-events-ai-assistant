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

with gr.Blocks(theme="ocean") as demo:
    gr.Markdown("""
    # JumpCloud Directory Insights Event Assistant
    """)
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("""
            ## Instructions
            - Ask questions about JumpCloud Directory Insights events.
            - Example prompts:
                - What are the recent admin login attempts?
                - Show me all admin logins from IN for last 2 days
                - List all failed login attempts in the last 24 hours.
                - show details about softwares added in last week
                - What are the recent password reset requests?
                - List all admin lockouts in the last month.
            """)
        with gr.Column(scale=3):
            chatbot = gr.Chatbot()
            msg = gr.Textbox(placeholder="Ask me about DI events", container=False, scale=7)
            clear = gr.Button("Clear")

    def respond(message, history):
        response = chat_with_backend(message, history)
        # Gradio expects the chatbot history as a list of [user, bot] pairs
        if history is None:
            history = []
        history = history + [[message, response]]
        return history

    def clear_chat():
        return [], ""

    msg.submit(respond, [msg, chatbot], [chatbot, msg])
    clear.click(clear_chat, outputs=[chatbot, msg])

demo.launch()
