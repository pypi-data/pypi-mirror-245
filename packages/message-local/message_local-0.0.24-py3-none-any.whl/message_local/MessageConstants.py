from logger_local.Logger import Logger
from logger_local.LoggerComponentEnum import LoggerComponentEnum

MESSAGE__LOCAL_PYTHON_COMPONENT_ID = ""
MESSAGE_LOCAL_PYTHON_COMPONENT_COMPONENT_NAME = ""
DEVELOPER_EMAIL = 'jenya.b@circ.zone'
object_message = {
    'component_id': MESSAGE__LOCAL_PYTHON_COMPONENT_ID,
    'component_name': MESSAGE_LOCAL_PYTHON_COMPONENT_COMPONENT_NAME,
    'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
    'developer_email': DEVELOPER_EMAIL
}
logger = Logger.create_logger(object=object_message)

DEFAULT_HEADERS = {"Content-Type": "application/json"}

TEST_API_TYPE_ID = 4
AWS_SMS_MESSAGE_PROVIDER_ID = 1
SMS_MESSAGE_CHANNEL_ID = 2
WHATSAPP_CHANNEL_ID = 11
INFORU_MESSAGE_PROVIDER_ID = 2
