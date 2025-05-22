from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import requests
from litellm import completion, exceptions
import json
import datetime
from event_schema_registry import get_event_schema
from event_types import event_types_list, EVENT_TYPE_TO_SERVICE_MAP
from system_prompt import system_prompt_content
from llm_api_tools import api_tools, get_event_schema_function_declaration

load_dotenv()

# --- Load config at startup ---
LITELLM_MODEL_NAME = os.getenv("LITELLM_MODEL_NAME", "gemini-2.0-flash")
LITELLM_API_BASE = os.getenv("LITELLM_API_BASE", "")
LITELLM_API_KEY = os.getenv("LITELLM_API_KEY", "")
JC_API_BASE_URL = os.getenv("JC_API_BASE_URL", "")
DI_EVENTS_API_ENDPOINT = os.getenv("DI_EVENTS_API_ENDPOINT", "")
SI_DI_EVENTS_API_ENDPOINT = os.getenv("SI_DI_EVENTS_API_ENDPOINT", "")
JC_API_KEY_VALUE = os.getenv("JC_API_KEY", "")

# Precompute full API URLs if needed
LITELLM_FULL_API_URL = LITELLM_API_BASE + LITELLM_MODEL_NAME
JC_DI_EVENTS_API_URL = JC_API_BASE_URL + DI_EVENTS_API_ENDPOINT

app = Flask(__name__)

# --- Flask API endpoint ---
@app.route('/question', methods=['POST'])
def handle_post():
    data = request.get_json()
    if not data or 'prompt' not in data:
        return jsonify({'error': 'Missing prompt in request body'}), 400
    prompt = data['prompt']
    response = ask_custom_llm(prompt)
    return jsonify({'llm_response': response}), 200


# --- Function to execute the tools called by the LLM ---
def execute_tool_call(tool_call):
    """
    Execute the tool call requested by the LLM.
    This function should be modified to call your actual API.
    """
    function_name = tool_call.function.name
    function_args = json.loads(tool_call.function.arguments)
    print(f"Executing tool call: {function_name} with arguments: {function_args}")


    if function_name == "query_events":
        # Fix search_term key if needed
        if "search_term" in function_args:
            st = function_args["search_term"]
            print(f"search_term: {st}")
            # Check if the top-level key is one of "and", "or", or "not"
            for key in list(st.keys()):
                if key not in ("and", "or", "not"):
                    # Attempt to fix common LLM mistakes like "and1"
                    if key.startswith("and"):
                        st["and"] = st.pop(key)
                    elif key.startswith("or"):
                        st["or"] = st.pop(key)
                    elif key.startswith("not"):
                        st["not"] = st.pop(key)

        # Extract the arguments from the tool call
        arguments = function_args  # Already a dict, no need to json.loads
        
        # 1. Check if 'service' was explicitly provided by the LLM (from user query)
        user_provided_service = arguments.get("service")

        if user_provided_service:
            # If the user (via LLM) provided a service, use it directly.
            # Ensure it's a list for consistency with the API schema.
            if not isinstance(user_provided_service, list):
                arguments["service"] = [user_provided_service]
                print(f"Using user-provided service: {arguments['service']}")
            else:
                # 2. If no service was provided, try to infer from event_type
                inferred_service = ["all"]
                if "search_term" in arguments and arguments["search_term"]:
                    search_term_obj = arguments["search_term"]
                    for logical_op in ["and", "or", "not"]:
                        if logical_op in search_term_obj:
                            for filter_obj in search_term_obj[logical_op]:
                                if "event_type" in filter_obj:
                                    event_types_in_query = filter_obj["event_type"]
                                    if event_types_in_query:
                                        # Get service for the first event type found
                                        first_event_type = event_types_in_query[0]
                                        if first_event_type in EVENT_TYPE_TO_SERVICE_MAP:
                                            inferred_service = [EVENT_TYPE_TO_SERVICE_MAP[first_event_type]]
                                            print(f"Inferred service: {inferred_service[0]} for event type: {first_event_type}")
                                            break
                            if inferred_service != ["all"]:
                                # If service was inferred, break outer loop
                                break
                if inferred_service != ["all"] and arguments.get("service") != inferred_service:
                    arguments["service"] = inferred_service
                    print(f"Overriding service to: {arguments['service']}")
                elif "service" not in arguments: # If LLM didn't provide service, use default
                    arguments["service"] = inferred_service
                    print(f"Setting default service to: {arguments['service']}")

        print(f"\n--- Executing query_events with payload: {json.dumps(function_args, indent=2)} ---")

        # Call your API here with the arguments
        # For demonstration, we will just return a mock response
        try:
            api_response = requests.post(
                JC_DI_EVENTS_API_URL,
                json=arguments,
                headers={
                    "Content-Type": "application/json",
                    "x-api-key": JC_API_KEY_VALUE
                }
            )
            api_response.raise_for_status()  # Raise an error for bad responses
            response_data = api_response.json()
            print(f"API Response: {json.dumps(response_data, indent=2)}")
            return response_data
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            return {"error": str(http_err)}
        except requests.exceptions.RequestException as e:
            print(f"JC DI API call failed: {e}")
            return {"error": str(e)}
        return {"status": "success", "data": "Mock data from query_events"}

    elif function_name == "get_event_schema":
        event_type_name = function_args.get("event_type_name")
        print(f"\n--- Executing get_event_schema for '{event_type_name}' ---")
        schema = get_event_schema(event_type_name)
        if schema:
            return {"event_schema": schema}
        else:
            # print(f"Schema for '{event_type_name}' not found.")
            # return {"error": f"Schema for event type '{event_type_name}' not found."}
        
            # IMPORTANT: Provide a clear error message that can guide the LLM
            # even if the event_type_name was in the enum, but no schema is defined.
            # You might want to return a generic schema or just confirm its existence.
            known_event_types = list(get_event_schema_function_declaration['function']['parameters']['properties']['event_type_name']['enum'])
            if event_type_name not in known_event_types:
                 print(f"Error: '{event_type_name}' is not a recognized event type.")
                 return {"error": f"Event type '{event_type_name}' is not recognized. Please choose from: {', '.join(known_event_types)}."}
            else:
                 print(f"Schema for '{event_type_name}' found in enum but not fully defined in registry.")
                 # If you don't have a full schema, return a minimal "found but no details" response
                 # or a placeholder schema that just confirms its existence
                 return {
                     "event_schema": get_event_schema(event_type_name),
                 }

    elif function_name == "get_current_date":
        # Return the current date in RFC3339 format
        current_date = datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
        return {"current_date": current_date}

    else:
        raise ValueError(f"Unknown function name: {tool_call.function.name}")

def ask_custom_llm(prompt):
    """
    Interact with a custom LLM using litellm's completion API.
    Assumes LLM config is set via environment variables (see litellm docs).
    """
    print(f"Prompt: {prompt}")

    model = "hosted_vllm/" + LITELLM_MODEL_NAME
    print(f"Model: {model}")

    api_base = LITELLM_FULL_API_URL    
    print(f"API Base: {api_base}")

    if not api_base.startswith("http://") and not api_base.startswith("https://"):
        raise ValueError(f"api_base is missing protocol: {api_base}")

    messages = [
        {
            "role": "system", "content": system_prompt_content,
        },
        {
            "role": "user", "content": prompt
        }
    ]

    try:
        response = completion(
            model=model,
            api_base=api_base,
            api_key=LITELLM_API_KEY,
            custom_llm_provider="gemini",
            messages=messages,
            tools=api_tools,
            tool_choice="auto",
        )

        # Loop for potential multi-turn tool calls
        while response.choices[0].message.tool_calls:
            tool_calls = response.choices[0].message.tool_calls

            # Add the tool_calls to the conversation history
            messages.append(response.choices[0].message)
            print(f"\n--- Gemini requested {len(tool_calls)} tool call(s) ---")

            # Execute each tool call requested by the model
            for tool_call in tool_calls:
                tool_output = execute_tool_call(tool_call)
                
                # Add the tool's output to the conversation history
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(tool_output)
                })
            
            # Call Gemini again with the updated conversation history (including tool outputs)
            response = completion(
                model=model,
                api_base=api_base,
                api_key=LITELLM_API_KEY,
                custom_llm_provider="gemini",
                messages=messages,
                tools=api_tools,
                tool_choice="auto"
            )

            # --- NEW: Final Summarization Step ---
            # If the loop finishes, it means Gemini has generated a final text response,
            # OR it made a tool call (like query_events) and now needs to summarize its output.
            
            # Check if the last turn was a tool call that generated data for summarization.
            # This will be true if the `while` loop exited because `response.choices[0].message.tool_calls` was None
            # but the last message in `messages` was a 'tool' role with data.

        # If the loop finishes, Gemini has generated a final text response
        if response.choices[0].message.content:
            print("\n--- Gemini's Final Response ---")
            print(response.choices[0].message.content)
        else:
            print("No final text content generated.")

        if messages and messages[-1]["role"] == "tool":
            print("\n--- Finalizing response with Gemini (Summarization) ---")
            # Make a final call to Gemini to summarize the results.
            # We explicitly set tool_choice to "none" to ensure it generates text.
            final_response = completion(
                model=model,
                api_base=api_base,
                api_key=LITELLM_API_KEY,
                custom_llm_provider="gemini",
                messages=messages,
                tools=api_tools, # Still pass tools, but tool_choice overrides
                tool_choice="none" # Crucial: Force text generation, no more tool calls
            )
            
            if final_response.choices and final_response.choices[0].message.content:
                print("\n--- Gemini's Summary of API Results ---")
                print(final_response.choices[0].message.content)
            else:
                print("Gemini did not provide a final summary.")
        elif response.choices and response.choices[0].message.content:
            # This handles cases where no tool call was needed, and Gemini gave a direct answer
            # (e.g., "What is the capital of France?")
            print("\n--- Gemini's Direct Response (No API Call) ---")
            print(response.choices[0].message.content)
        else:
            print("No content generated or an error occurred from Gemini (empty final response).")
        return response.choices[0].message.content
    except exceptions.APIError as e:
        print(f"LiteLLM API error: {e}")
    except Exception as e:
        return f"Error: {str(e)}"

# --- Run interactions with dynamic schema awareness ---
# Example usage
#ask_custom_llm("Show me failed admin logins for user someuser@gmail.com for last 15 days.")
#ask_custom_llm("Show me all admin logins from US for last 2 days.")

if __name__ == '__main__':
    app.run(debug=True)
