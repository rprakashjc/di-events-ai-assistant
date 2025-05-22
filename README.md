# Minimal Flask LLM Event Query App

This project is a minimal Flask web application that exposes a POST endpoint at `/question` for querying events using a custom LLM via LiteLLM. It supports dynamic event schema querying, robust search/filter logic, and uses environment variables for configuration.

## How to run

1. Copy the environment template and update your API keys:
   ```bash
   cp .env_template .env
   # Edit .env to add your API keys and configuration
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the app:
   ```bash
   python app.py
   ```

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
