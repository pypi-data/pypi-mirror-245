from logger_local.LoggerComponentEnum import LoggerComponentEnum


class EventRemoteConstants:
    DEVELOPER_EMAIL = 'gil.a@circ.zone'
    EVENT_REMOTE_COMPONENT_ID = 248
    EVENT_REMOTE_PYHTON_COMPONENT_NAME = 'event-remote-restapi-python-package'
    EVENT_REMOTE_CODE_LOGGER_OBJECT = {
        'component_id': EVENT_REMOTE_COMPONENT_ID,
        'component_name': EVENT_REMOTE_PYHTON_COMPONENT_NAME,
        'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
        'developer_email': DEVELOPER_EMAIL
    }
    EVENT_REMOTE_TEST_LOGGER_OBJECT = {
        'component_id': EVENT_REMOTE_COMPONENT_ID,
        'component_name': EVENT_REMOTE_PYHTON_COMPONENT_NAME,
        'component_category': LoggerComponentEnum.ComponentCategory.Unit_Test.value,  # noqa: E501
        # TODO Please add the framework you use
        'developer_email': DEVELOPER_EMAIL
    }

    # TODO Please replace <ENTITY> i.e. COUNTRY
    # UNKNOWN_<ENTITY>_ID = 0


# TODO In the case you use non-ML Table, please replace <entity> i.e. country
    EXTERNAL_EVENT_TABLE_NAME = 'event_external_table'

    EXTERNAL_EVENT_SCHEMA_NAME = 'event_external'

    EXTERNAL_EVENT_ID_COLUMN_NAME = 'event_external_id'

    EXTERNAL_EVENT_VIEW_NAME = 'event_external_view'
    # <ENTITY>_VIEW_NAME = '<entity>_ml_table'

    # TODO In the case you use ML Table, please replace <entity> i.e. country
    # <ENTITY>_TABLE_NAME = '<entity>_table'
    # <ENTITY>_ML_TABLE_NAME = '<entity>_ml_table'
    # <ENTITY>_ML_VIEW_NAME = '<entity>_ml_view'
