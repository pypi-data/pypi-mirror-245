# TODO Please rename the filename from entity_constants.py to your entity. If your entity is country please change the file name to country_constants.py

from logger_local.LoggerComponentEnum import LoggerComponentEnum

# Please change everywhere there is "<Entity>" to your entity name i.e. "Country"  (Please pay attention the C is in uppercase)
# This is a class of all the constants of your entity
class EventRemoteConstants:

    # TODO Please update your email
    DEVELOPER_EMAIL = 'gil.a@circ.zone'

    # TODO Please change everywhere in the code "<PROJECT_NAME>" to "COUNTRY_LOCAL_PYTHON" in case your entity is Country.
    # TODO Please send a message in the Slack to #request-to-open-component-id and get your COMPONENT_ID
    # For example COUNTRY_COMPONENT_ID = 34324
    EVENT_REMOTE_COMPONENT_ID = 248
    # TODO Please write your own COMPONENT_NAME
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
        'component_category': LoggerComponentEnum.ComponentCategory.Unit_Test.value,
        # TODO Please add the framework you use
        'developer_email': DEVELOPER_EMAIL
    }

    # TODO Please replace <ENTITY> i.e. COUNTRY
    # UNKNOWN_<ENTITY>_ID = 0

    # TODO Please update if you need default values i.e. for testing
    #DEFAULT_XXX_NAME = None
    #DEFAULT_XXX_NAME = None

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
