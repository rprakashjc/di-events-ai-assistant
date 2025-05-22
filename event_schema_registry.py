# --- Simulate a schema registry/storage ---
event_schemas_registry = {
    "admin_login_attempt": {
        "type": "object",
        "description": "Schema for an 'admin_login_attempt' event.",
        "properties": {
            "initiated_by":{
                "type": "object",
                "properties": {
                    "id": {"type": "string"},
                    "type": {"type": "string", "description": "Type of the user. Example 'admin'"},
                    "email": {"type": "string", "format": "email", "description": "Email address of the user, use this field when someone asks for a user email."},
                }
            },
            "geoip": {
                "type": "object",
                "properties": {
                    "timezone": {"type": "string"},
                    "country_code": {"type": "string", "description": "2-letter ISO country code"},
                    "continent_code": {"type": "string", "description": "2-letter ISO continent code"},
                    "region_name": {"type": "string", "description": "Region name. Example 'Oregon'"},
                    "region_code": {"type": "string", "description": "2-letter ISO Region code. Example 'OR'"},
                }
            },
            "useragent": {
                "type": "object",
                "properties": {
                    "minor": {"type": "string"},
                    "os": {"type": "string"},
                    "os_minor": {"type": "string"},
                    "os_version": {"type": "string"},
                    "os_major": {"type": "string"},
                    "version": {"type": "string"},
                    "os_patch": {"type": "string"},
                    "patch": {"type": "string"},
                    "os_full": {"type": "string"},
                    "major": {"type": "string"},
                    "name": {"type": "string", "description": "Browser name"},
                    "os_name": {"type": "string", "description": "Operating system name"},
                    "device": {"type": "string", "description": "Device type. example 'Mac'"},
                }
            },
            "mfa": {"type": "boolean", "description": "Multi-Factor Authentication status"},
            "event_type": {"type": "string", "enum": ["admin_login_attempt"]},
            "success": {"type": "boolean"},
            "service": {"type": "string", "description": "Service name. Example 'directory'"},
            "organization": {"type": "string"},
            "client_ip": {"type": "string", "description": "Client IP address (IPv4 or IPv6 format)."},
            "id": {"type": "string"},
            "timestamp": {"type": "string", "format": "date-time"}
        }
    },
    "user_login_attempt": {
        "type": "object",
        "description": "Schema for a 'user_login_attempt' event.",
        "properties": {
            "initiated_by":{
                "type": "object",
                "properties": {
                    "id": {"type": "string"},
                    "type": {"type": "string", "description": "Type of the user. Example 'user'"},
                    "username": {"type": "string", "description": "Username of the user"},
                    "administrator": {"type": "boolean", "description": "Indicates if the user is an administrator"},
                }
            },
            "error_message": {"type": "string", "description": "Error message if the login attempt failed"},
            "geoip": {
                "type": "object",
                "properties": {
                    "timezone": {"type": "string"},
                    "country_code": {"type": "string", "description": "2-letter ISO country code"},
                    "continent_code": {"type": "string", "description": "2-letter ISO continent code"},
                    "region_name": {"type": "string", "description": "Region name. Example 'Oregon'"},
                    "region_code": {"type": "string", "description": "2-letter ISO Region code. Example 'OR'"},
                }
            },
            "target_resource": {
                "type": "object",
                "properties": {
                    "type": {"type": "string", "description": "Type of the resource. Example 'user_portal'"},
                }
            },
            "auth_context": {
                "type": "object",
                "properties": {
                    "auth_methods": {
                        "type": "object",
                        "properties": {
                            "password": {"type": "boolean", "description": "Indicates if password was used"},
                            "mfa": {"type": "boolean", "description": "Indicates if MFA was used"},
                            "sso": {"type": "boolean", "description": "Indicates if SSO was used"},
                        }
                    },
                }
            },
            "useragent": {
                "type": "object",
                "properties": {
                    "minor": {"type": "string"},
                    "os": {"type": "string"},
                    "os_minor": {"type": "string"},
                    "os_version": {"type": "string"},
                    "os_major": {"type": "string"},
                    "version": {"type": "string"},
                    "os_patch": {"type": "string"},
                    "patch": {"type": "string"},
                    "os_full": {"type": "string"},
                    "major": {"type": "string"},
                    "name": {"type": "string", "description": "Browser name"},
                    "os_name": {"type": "string", "description": "Operating system name"},
                    "device": {"type": "string", "description": "Device type. example 'Mac'"},
                }
            },
            "mfa": {"type": "boolean", "description": "Multi-Factor Authentication status"},
            "event_type": {"type": "string", "enum": ["user_login_attempt"]},
            "success": {"type": "boolean"},
            "service": {"type": "string", "description": "Service name. Example 'directory'"},
            "organization": {"type": "string"},
            "client_ip": {"type": "string", "format": "ipv4 or ipv6"},
            "id": {"type": "string"},
            "timestamp": {"type": "string", "format": "date-time"},
        }
    },
    # Add more schemas here as key-value pairs
}

def get_common_schema(event_type_name):
    common_event_schema = {
        "type": "object",
        "description": f"No detailed schema available for '{event_type_name}' but it is a recognized event type. You can query for it directly using 'event_type': ['{event_type_name}'].",
        "properties": {
            "initiated_by":{
                "type": "object",
                "properties": {
                    "id": {"type": "string"},
                    "type": {"type": "string", "description": "Type of the user. Example 'admin'"},
                    "email": {"type": "string", "format": "email", "description": "Email address of the user, use this field when someone asks for a user email."},
                }
            },
            "geoip": {
                "type": "object",
                "properties": {
                    "timezone": {"type": "string"},
                    "country_code": {"type": "string", "description": "2-letter ISO country code"},
                    "continent_code": {"type": "string", "description": "2-letter ISO continent code"},
                    "region_name": {"type": "string", "description": "Region name. Example 'Oregon'"},
                    "region_code": {"type": "string", "description": "2-letter ISO Region code. Example 'OR'"},
                }
            },
            "event_type": {"type": "string", "description": "Type of the event"},
            "success": {"type": "boolean"},
            "service": {"type": "string", "description": "Service name"},
            "organization": {"type": "string", "description": "Organization name"},
            "id": {"type": "string", "description": "Unique identifier for the event"},
            "timestamp": {"type": "string", "format": "date-time", "description": "Timestamp of the event"},
        }
    }
    return common_event_schema

def get_event_schema(event_type_name):
    """
    Retrieve the schema for a specific event type.
    If the event type is not found, return a common schema indicating it's a recognized event type.
    """
    if event_type_name in event_schemas_registry:
        return event_schemas_registry[event_type_name]
    else:
        return get_common_schema(event_type_name)
