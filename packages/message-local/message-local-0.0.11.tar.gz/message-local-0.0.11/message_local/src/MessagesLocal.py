from logger_local.Logger import Logger
from logger_local.LoggerComponentEnum import LoggerComponentEnum
from sms_message_aws_sns_local.SendAwsSms import SmsMessageAwsSns, send_sms_using_aws_sms_using_api_getaway
import boto3

from .Message import Message, MessageImportance

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

AWS_SMS_MESSAGE_PROVIDER_ID = 1
SMS_MESSAGE_CHANNEL_ID = 2
WHATSAPP_CHANNEL_ID = 11
INFORU_MESSAGE_PROVIDER_ID = 2


# TODO: rewrite
class MessagesLocal(Message):
    def __init__(self, body: str, importance: MessageImportance, subject: str = None) -> None:
        super().__init__(body, importance, subject)

    def _get_message_channel_id(self) -> int:
        """return message channel"""
        "get message id"
        """channel_id = GenericCRUD("message",default_table_name="message_channel_ml_table",
                        default_id_column_name="message_channel_id").select_one_dict_by_id(
                            select_clause_value="name", id_column_value=2)"""
        return SMS_MESSAGE_CHANNEL_ID

    def _get_message_provider_id(self, message_channel_id: int) -> int:
        """return message provider"""
        logger.start()
        if message_channel_id == SMS_MESSAGE_CHANNEL_ID:
            return AWS_SMS_MESSAGE_PROVIDER_ID
        """
        elif message_channel_id == AWS_SMS_MESSAGE_PROVIDER_ID:
            return AWS_SMS_MESSAGE_PROVIDER_ID
        elif message_channel_id == WHATSAPP_CHANNEL_ID:
            return INFORU_MESSAGE_PROVIDER_ID"""
        logger.end()

    def send(self, recipients: list, cc: list = None, bcc: list = None) -> None:
        """send method"""
        logger.start()
        """
        for recipient in recipients:
            if "profile_id" in recipient:
                instance = self.get_instance()
                return instance.send(recipient)"""
        instance = self.get_instance()
        return instance.send(recipients)

    def was_read(self) -> bool:
        return False

    def _can_send(self) -> bool:
        return True

    def _after_send_attempt(self):
        pass

    def get_id(self):
        return 0

    def get_instance(self):
        channel_id = self._get_message_channel_id()
        provider_id = self._get_message_provider_id(channel_id)
        if channel_id == SMS_MESSAGE_CHANNEL_ID and provider_id == AWS_SMS_MESSAGE_PROVIDER_ID:
            return SmsMessageAwsSns(boto3.resource("sns"))