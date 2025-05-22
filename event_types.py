service_to_event_types_map = {
    "access_management": [
        "access_management_access_request",
        "access_management_access_request_approval",
        "access_management_association_change",
        "access_management_workflow_create",
        "access_management_workflow_update",
        "access_management_workflow_delete",
        "access_management_workflow_settings_update",
    ],
    "saas_management": [
        "saas_management_enable",
        "saas_management_disable",
        "saas_management_settings_update",
        "saas_management_application_discover",
        "saas_management_event_application_review",
        "saas_management_application_update",
        "saas_management_application_access_restriction_update",
        "saas_management_application_license_update",
    ],
    "alert": [
        "alert_created",
        "alert_updated",
        "alert_status_updated",
        "rule_created",
        "rule_modified",
        "rule_deleted",
    ],
    "object_storage": [
        "object_storage_create",
        "object_storage_upload_validation_result",
        "object_storage_get_download_url_request",
        "object_storage_delete",
    ],
    "notification_channel": [
        "notification_channel_created",
        "notification_channel_updated",
        "notification_channel_deleted",
    ],
    "mdm": [
        "mdm_command_result",
        "device_enrollment",
        "configuration_file_download",
    ],
    "ldap": [
        "ldap_bind",
        "ldap_search",
    ],
    "software": [
        "software_add",
        "software_change",
        "software_remove",
    ],
    "sso": [
        "sso_auth",
    ],
    "radius": [
        "radius_auth",
    ],
    "directory": [
        "admin_unsuspend",
        "admin_create",
        "admin_delete",
        "admin_lockout",
        "admin_login_attempt",
        "admin_password_reset_request",
        "admin_suspended",
        "admin_update",
        "organization_create",
        "organization_update",
        "provider_update",
        "mtp_download_invoice",
        "msp_ticket_create",
        "activedirectory_create",
        "activedirectory_delete",
        "idsource_create",
        "idsource_delete",
        "idsource_update",
        "sambadomain_create",
        "command_create",
        "command_delete",
        "command_run",
        "command_update",
        "commandresult_delete",
        "file_create",
        "file_delete",
        "file_update",
        "policy_create",
        "policy_delete",
        "policy_update",
        "authnpolicy_create",
        "authnpolicy_delete",
        "authpolicy_update",
        "iplist_create",
        "iplist_delete",
        "iplist_update",
        "admin_create",
        "admin_delete",
        "admin_login_attempt",
        "admin_password_reset_request",
        "admin_update",
        "admin_totp_start_enrollment",
        "admin_totp_finish_enrollment",
        "admin_totp_disable",
        "totp_start_enrollment",
        "totp_finish_enrollment",
        "totp_delete_enrollment",
        "user_create",
        "user_delete",
        "user_lockout",
        "user_login_attempt",
        "user_mfa_exclusion_expired",
        "user_password_expired",
        "user_password_reset_request",
        "user_password_warning_email",
        "user_update",
        "user_password_change",
        "user_activated",
        "user_activation_email",
        "user_password_set",
        "user_unlocked",
        "user_suspended",
        "user_unsuspended",
        "user_activation_schedule_create",
        "user_activation_schedule_delete",
        "user_suspension_schedule_create",
        "user_suspension_schedule_delete",
        "admin_password_change",
        "user_create_provision",
        "user_update_provision",
        "user_delete_provision",
        "user_admin_granted",
        "user_admin_revoked",
        "application_create",
        "application_delete",
        "application_update",
        "association_change",
        "group_create",
        "group_delete",
        "group_update",
        "integrationattribute_include",
        "integrationattribute_exclude",
        "invoice_download",
        "notification_delete",
        "organization_create",
        "organization_update",
        "system_create",
        "system_delete",
        "system_update",
        "radiusserver_create",
        "radiusserver_delete",
        "radiusserver_update",
        "user_group_admin_grant",
        "user_group_admin_revoke",
        # These should ideally be in the software service but are not
        "software_add_request",
        "software_change_request",
        "software_remove_request",
    ]
}

event_types_list = [
    # Access Management Events
    "access_management_access_request",
    "access_management_access_request_approval",
    "access_management_association_change",
    "access_management_workflow_create",
    "access_management_workflow_update",
    "access_management_workflow_delete",
    "access_management_workflow_settings_update",

    # SaaS Management Events
    "saas_management_enable",
    "saas_management_disable",
    "saas_management_settings_update",
    "saas_management_application_discover",
    "saas_management_event_application_review",
    "saas_management_application_update",
    "saas_management_application_access_restriction_update",
    "saas_management_application_license_update",

    # Alert Events
    "alert_created",
    "alert_updated",
    "alert_status_updated",
    "rule_created",
    "rule_modified",
    "rule_deleted",

    # Object Storage Events
    "object_storage_create",
    "object_storage_upload_validation_result",
    "object_storage_get_download_url_request",
    "object_storage_delete",

    # Notification Channel Events
    "notification_channel_created",
    "notification_channel_updated",
    "notification_channel_deleted",

    # MDM Events
    "mdm_command_result",
    "device_enrollment",
    "configuration_file_download",

    # LDAP Events
    "ldap_bind",
    "ldap_search",

    # Software Events
    "software_add",
    "software_change",
    "software_remove",
    "software_add_request",
    "software_change_request",
    "software_remove_request",

    # SSO Events
    "sso_auth",

    # RADIUS Events
    "radius_auth",

    # Directory - MTP/MSP Events
    "admin_unsuspend",
    "admin_create",
    "admin_delete",
    "admin_lockout",
    "admin_login_attempt",
    "admin_password_reset_request",
    "admin_suspended",
    "admin_update",
    "organization_create",
    "organization_update",
    "provider_update",
    "mtp_download_invoice",
    "msp_ticket_create",

    # Directory - Integrations
    "activedirectory_create",
    "activedirectory_delete",
    "idsource_create",
    "idsource_delete",
    "idsource_update",
    "sambadomain_create",


    # Directory - Command and Policy Events
    "command_create",
    "command_delete",
    "command_run",
    "command_update",
    "commandresult_delete",
    "file_create",
    "file_delete",
    "file_update",
    "policy_create",
    "policy_delete",
    "policy_update",
    "authnpolicy_create",
    "authnpolicy_delete",
    "authpolicy_update",
    "iplist_create",
    "iplist_delete",
    "iplist_update",

    # Directory - User and Admin Events
    "admin_create",
    "admin_delete",
    "admin_login_attempt",
    "admin_password_reset_request",
    "admin_update",
    "admin_totp_start_enrollment",
    "admin_totp_finish_enrollment",
    "admin_totp_disable",
    "totp_start_enrollment",
    "totp_finish_enrollment",
    "totp_delete_enrollment",
    "user_create",
    "user_delete",
    "user_lockout",
    "user_login_attempt",
    "user_mfa_exclusion_expired",
    "user_password_expired",
    "user_password_reset_request",
    "user_password_warning_email",
    "user_update",
    "user_password_change",
    "user_activated",
    "user_activation_email",
    "user_password_set",
    "user_unlocked",
    "user_suspended",
    "user_unsuspended",
    "user_activation_schedule_create",
    "user_activation_schedule_delete",
    "user_suspension_schedule_create",
    "user_suspension_schedule_delete",
    "admin_password_change",
    "user_create_provision",
    "user_update_provision",
    "user_delete_provision",
    "user_admin_granted",
    "user_admin_revoked",

    # Directory - Object Events
    "application_create",
    "application_delete",
    "application_update",
    "association_change",
    "group_create",
    "group_delete",
    "group_update",
    "integrationattribute_include",
    "integrationattribute_exclude",
    "invoice_download",
    "notification_delete",
    "organization_create",
    "organization_update",
    "system_create",
    "system_delete",
    "system_update",
    "radiusserver_create",
    "radiusserver_delete",
    "radiusserver_update",
    "user_group_admin_grant",
    "user_group_admin_revoke",
]


def get_event_type_to_service_map():
    """
    Returns a dictionary mapping each event_type to its service (single string).
    """
    event_type_to_service = {}
    for service, event_types in service_to_event_types_map.items():
        for event_type in event_types:
            event_type_to_service[event_type] = service
    return event_type_to_service


# Precompute event_type to service map at startup
EVENT_TYPE_TO_SERVICE_MAP = get_event_type_to_service_map()

def get_service_for_event_type(event_type):
    """
    Retrieves the service for a given event type.
    Returns None if the event type is not found in the map.
    """
    return EVENT_TYPE_TO_SERVICE_MAP.get(event_type)


def get_event_types_for_service(service):
    """
    Returns a list of event types for a given service.
    """
    return service_to_event_types_map.get(service, [])
