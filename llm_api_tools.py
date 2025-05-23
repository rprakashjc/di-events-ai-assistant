from event_types import event_types_list

# --- Tool 1: query_events ---
# Define the function declaration for your POST /events/list API in OpenAI-compatible format
query_events_function_declaration = {
    "type": "function",
    "function": {
        "name": "query_events", # This should ideally match your OpenAPI operationId or be descriptive
        "description": "Queries events from the system. This function is used to retrieve event logs based on various parameters. The user can specify the service, time range, fields to return, and filters for the events.",
        "parameters": { # This directly mirrors the JSON Schema of your requestBody
            "type": "object",
            "required": ["service", "start_time"],
            "properties": {
                "service": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "enum": [
                            "alerts",
                            "all",
                            "directory",
                            "ldap",
                            "mdm",
                            "notifications",
                            "object_storage",
                            "password_manager",
                            "radius",
                            "reports",
                            "saas_app_management",
                            "software",
                            "sso",
                            "systems",
                            "access_management"
                        ]
                    },
                    "description": "Service name(s) to query. Use 'all' if not specified in the user request."
                },
                "start_time": {
                    "type": "string",
                    "format": "date-time",
                    "description": "Query start time, UTC in RFC3339 format."
                },
                "end_time": {
                    "type": "string",
                    "format": "date-time",
                    "description": (
                        "Optional query end time, UTC in RFC3339 format. "
                        "Omit this field entirely if the user does not specify an end time in the query. "
                        "Do not include it as null or empty string."
                        "Example with end_time omitted:\n"
                        "{\n"
                        "  \"service\": [\"all\"],\n"
                        "  \"start_time\": \"2025-05-01T00:00:00Z\"\n"
                        "  // end_time is not present\n"
                        "}\n"
                        "Invalid example (do not do this):\n"
                        "{\n"
                        "  \"service\": [\"all\"],\n"
                        "  \"start_time\": \"2025-05-01T00:00:00Z\",\n"
                        "  \"end_time\": null\n"
                        "}\n"
                    )
                },
                "fields": {
                    "type": "array",
                    "items": { "type": "string" },
                    "description": "Optional list of fields to return from query."
                },
                "limit": {
                    "type": "integer",
                    "description": "Max number of rows to return."
                },
                # "q": {
                #     "type": "string",
                #     "description": "Optional string for specifying a full text query."
                # },
                "search_after": {
                    "type": "array",
                    "items": { "type": "object" },
                    "description": "Specific query to search after, see x-* response headers for next values."
                },
                "search_term": {
                    "type": "object",
                    "description": (
                        "A structured JSON object for filtering events."
                        "Only one of 'and', 'or', or 'not' is allowed as the top-level key. "
                        "Each key maps to an array of filter objects. Each filter object must contain a single key-value pair where: "
                        "- The key is a precise event field path (e.g., 'initiated_by.email', 'geoip.country_code', 'success', 'useragent.os_name'). "
                        "- The value is an array of strings or booleans that the field must match. Boolean values should be represented as 'true' or 'false' strings. "
                        "**Crucially, use the 'get_event_schema' tool first to discover available field paths for specific event types.**\n\n"
                        "Examples:\n"
                        "1. Any events that have a username of either 'root' or 'admin':\n"
                        "   {\n  \"and\": [\n    {\"username\": [\"root\", \"admin\"]}\n  ]\n}\n"
                        "2. All events that have either a username of 'root' or 'admin' OR a client_ip of '1.2.3.4' or '2.3.4.5':\n"
                        "   {\n  \"or\": [\n    {\"username\": [\"root', 'admin']},\n    {\"client_ip': ['1.2.3.4', '2.3.4.5']}\n  ]\n}\n"
                        "3. Get all successful admin login attempts:\n"
                        "   {\n  \"and\": [\n    {\"event_type\": [\"admin_login_attempt\"]},\n    {\"success\": [\"true\"]}\n  ]\n}\n"
                        "4. Get all events for a specific user by email:\n"
                        "   {\n  \"and\": [\n    {\"initiated_by.email\": [\"rprakash@gmail.com\"]}\n  ]\n}\n"
                        "5. Events from the US or Canada:\n"
                        "   {\n  \"or\": [\n    {\"geoip.country_code\": [\"US\"]},\n    {\"geoip.country_code\": [\"CA\"]}\n  ]\n}\n"
                        "6. Admin logins from Mac OS:\n"
                        "   {\n  \"and\": [\n    {\"event_type\": [\"admin_login_attempt\"]},\n    {\"useragent.os_name\": [\"Mac OS X\"]}\n  ]\n}\n"
                        "7. Failed RADIUS login attempts for user 'paul' with an 'and' with nested or:\n"
                        "   {\n  \"service\": [\"radius\"],\n  \"start_time\": \"2020-01-01T14:00:00Z\",\n  \"search_term\": {\n    \"and\": [\n      {\"success\": [\"false\"]},\n      {\"or\": [\n        {\"initiated_by.username\": [\"paul\"]},\n        {\"username\": [\"paul\"]}\n      ]}\n    ]\n  }\n}\n"
                        "8. Query for admin or user login attempts (using 'or' on event_type):\n"
                        "   {\n  \"or\": [\n    {\"event_type\": [\"admin_login_attempt\"]},\n    {\"event_type\": [\"user_login_attempt\"]}\n  ]\n}\n"
                    ),
                    
                    "properties": {
                        "and": {
                            "type": "array",
                            "items": { # Now we define the structure of the items more precisely
                                "type": "object",
                                "minProperties": 1,
                                "maxProperties": 1,
                                "patternProperties": { # This is key: enforce field-value pairs
                                    "^[a-zA-Z0-9_\\.]+$": { # Pattern for valid field paths (alphanumeric, underscore, dot)
                                        "type": "array",
                                        "items": { "type": ["string", "boolean"] } # Values can be string or boolean for exact match
                                    }
                                },
                                "description": "A filter object: {'field.path': ['value1', 'value2']}"
                            }
                        },
                        "or": {
                            "type": "array",
                            "items": { # Same structure as 'and'
                                "type": "object",
                                "minProperties": 1,
                                "maxProperties": 1,
                                "patternProperties": {
                                    "^[a-zA-Z0-9_\\.]+$": {
                                        "type": "array",
                                        "items": { "type": ["string", "boolean"] }
                                    }
                                },
                                "description": "A filter object: {'field.path': ['value1', 'value2']}"
                            }
                        },
                        "not": { # For 'not', it's usually a single object or array of objects to negate
                            "type": "array", # Changed to array, as your example shows "not" containing multiple conditions
                            "items": {
                                "type": "object",
                                "minProperties": 1,
                                "maxProperties": 1,
                                "patternProperties": {
                                    "^[a-zA-Z0-9_\\.]+$": {
                                        "type": "array",
                                        "items": { "type": ["string", "boolean"] }
                                    }
                                },
                                "description": "A filter object to negate: {'field.path': ['value']}"
                            }
                        }
                    },
                    "minProperties": 1, # Ensure at least one of 'and', 'or', 'not' is present
                    "maxProperties": 1, # Ensure only one of 'and', 'or', 'not' is present
                    "additionalProperties": False # CRITICAL for preventing arbitrary keys at top level
                },
                "sort": {
                    "type": "string",
                    "enum": ["ASC", "DESC"],
                    "description": "ASC or DESC order for timestamp."
                }
            }
        }
    }
}

# --- Tool 2: get_event_schema (Utility tool for LLM to get schema) ---
get_event_schema_function_declaration = {
    "type": "function",
    "function": {
        "name": "get_event_schema",
        "description": (
            "Retrieves the JSON schema for a specific event type. "
            "Use this when the user asks for filters on a specific event type and you need to understand its internal fields (e.g., 'admin_login_attempt', 'user_signup'). "
            "This will help you formulate the 'search_term' for the 'query_events' tool. "
            "**Important:** Recognize common user phrasing for event types. For example: "
            "- 'user logins', 'user log in', 'user logged in' typically map to 'user_login_attempt'. "
            "- 'admin logins', 'admin log in', 'admin logged in' typically map to 'admin_login_attempt'. "
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "event_type_name": {
                    "type": "string",
                    "enum": event_types_list,
                    "description": "The exact name of the event type whose schema is required (e.g., 'admin_login_attempt')."
                }
            },
            "required": ["event_type_name"]
        },
        "parameters": {
            "type": "object",
            "properties": {
                "event_type_name": {
                    "type": "string",
                    "description": "The exact name of the event type whose schema is required (e.g., 'admin_login_attempt')."
                }
            },
            "required": ["event_type_name"]
        }
    }
}

# --- Tool 3: get_current_date (Utility for LLM) ---
get_current_date_function_declaration = {
    "type": "function",
    "function": {
        "name": "get_current_date",
        "description": "Provides the current date in UTC RFC3339 format. Use this to resolve time queries like 'x mins before', 'yesterday', 'tomorrow', 'next week', or 'next month'. start_time is mandatory, end_time is optional and should be omitted if not specified in the user query.",
        "parameters": {
            "type": "object",
            "properties": {}, # No parameters needed for this function
            "required": []
        }
    }
}

# The tools list passed to litellm.completion
api_tools = [
    query_events_function_declaration,
    get_event_schema_function_declaration,
    get_current_date_function_declaration,
]
