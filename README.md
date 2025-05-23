# Minimal Flask LLM Event Query App

This project is a minimal Flask web application that exposes a POST endpoint at `/question` for querying events using a custom LLM via LiteLLM. It supports dynamic event schema querying, robust search/filter logic, and uses environment variables for configuration.

## How to run

1. **Copy the environment template and update your API keys:**
   ```bash
   cp .env_template .env
   # Edit .env to add your API keys and configuration
   ```
2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Start the app:
   ```bash
   python app.py
   ```

5. (Optional) Start the Streamlit UI:
   ```bash
   streamlit run streamlit_app.py
   ```
   This will launch a modern chat interface at http://localhost:8501 where you can interact with the backend using natural language prompts.

6. (Optional) Start the Gradio UI:
   ```bash
   python gradio_app.py
   ```
   This will launch a web-based chat interface at http://localhost:7860 where you can interact with the backend using natural language prompts.

## Usage
Send a POST request to:
```
http://localhost:5000/endpoint
```
with a JSON payload containing your event query parameters. The app will respond with the LLM-processed event query results in JSON format.

Example:
```
curl -X POST http://localhost:5000/question   -H "Content-Type: application/json"   -d '{"prompt": "find all user login attempts in the past week"}'
```

Example Prompts:
```
Show me failed admin logins for user someuser@gmail.com for last 15 days
Show me all admin logins from US for last 2 days
Show me all admin logins from IN for last 2 days
find any admin update event happening in last 2 days
show details about softwares added in last week
Show all login events in last 2 weeks in a tabular format
Show all login events in last 2 weeks with all details in a tabular format
```
