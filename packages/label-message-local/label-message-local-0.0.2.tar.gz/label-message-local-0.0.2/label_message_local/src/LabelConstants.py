# TODO Please rename the filename from entity_constants.py to your entity. If your entity is country please change the file name to country_constants.py

from logger_local.LoggerComponentEnum import LoggerComponentEnum


# Please change everywhere there is "<Entity>" to your entity name i.e. "Country"  (Please pay attention the C is in uppercase)
# This is a class of all the constants of your entity
class LabelsLocalConstants:
    # TODO Please update your email
    DEVELOPER_EMAIL = 'tal.r@circ.zone'
    LABEL_MESSAGE_PACKAGE_COMPONENT_NAME = 'label_message_package'
    # TODO Please change everywhere in the code "LABEL_MESSAGE" to "COUNTRY_LOCAL_PYTHON" in case your entity is Country.
    # TODO Please send a message in the Slack to #request-to-open-component-id and get your COMPONENT_ID
    # For example COUNTRY_COMPONENT_ID = 34324
    LABEL_MESSAGE_PACKAGE_COMPONENT_ID = 254
    # TODO Please write your own COMPONENT_NAME
    LABEL_MESSAGE_COMPONENT_NAME = 'Country local Python package'
    LABEL_MESSAGE_CODE_LOGGER_OBJECT = {
        'component_id': LABEL_MESSAGE_PACKAGE_COMPONENT_ID,
        'component_name': LABEL_MESSAGE_PACKAGE_COMPONENT_NAME,
        'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
        'developer_email': DEVELOPER_EMAIL
    }
    LABEL_MESSAGE_TEST_LOGGER_OBJECT = {
        'component_id': LABEL_MESSAGE_PACKAGE_COMPONENT_ID,
        'component_name': LABEL_MESSAGE_PACKAGE_COMPONENT_NAME,
        'component_category': LoggerComponentEnum.ComponentCategory.Unit_Test.value,
        # TODO Please add the framework you use
        'developer_email': DEVELOPER_EMAIL
    }
    MESSAGE_OUTBOX_LABEL_ID = 18
