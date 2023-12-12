"""imports"""
import http
import json
import time
from typing import List, Union
from datetime import datetime

from api_management_local.api_limit_status import APILimitStatus
from api_management_local.API_Mangement_Manager import APIMangementManager
from api_management_local.direct import Direct
from api_management_local.Exception_API import (ApiTypeDisabledException,
                                                ApiTypeIsNotExistException,
                                                PassedTheHardLimitException)
from api_management_local.indirect import InDirect
from item_local.item import Item
from logger_local.Logger import Logger
# circular import
# from sms_message_aws_sns_local.SendAwsSms import SmsMessageAwsSns
from star_local.exception_star import NotEnoughStarsForActivityException
from variable_local.template import ReplaceFieldsWithValues

from .ChannelConstants import SMS_MESSAGE_CHANNEL_ID
from .MessageConstants import (AWS_SMS_MESSAGE_PROVIDER_ID, DEFAULT_HEADERS,
                               object_message)
from .MessageImportance import MessageImportance
from .Recipient import Recipient

logger = Logger.create_logger(object=object_message)


class MessageLocal(Item):
    """Message Local Class"""

    _is_http_api = None
    _api_type_id = None
    _endpoint = None
    _headers = None
    __used_cache = None
    __original_body: str = None
    __original_subject: str = None
    __external_user_id: int = None

    # body_after_text_template and all the rest should be protected as SmsMessage should check it
    __subject_after_text_template: str = None

    __body_after_text_template: dict = None
    __body_after_html_template: str = None

    def __init__(self, original_body: str, original_subject: str = None,
                 is_http_api: bool = None, api_type_id: int = None, endpoint: str = None,
                 importance: MessageImportance = MessageImportance.MEDIUM,
                 headers: dict = DEFAULT_HEADERS, external_user_id: int = None) -> None:
        # TODO We should add all fields from message schema in the database
        # (i.e. message_id, scheduled_sent_timestamp, message_sent_status : MessageSentStatus  ...)
        logger.start()
        self.__original_subject = original_subject
        self.__original_body = original_body
        self.importance = importance
        self._is_http_api = is_http_api
        self._api_type_id = api_type_id
        self._endpoint = endpoint
        self._headers = headers
        self.__external_user_id = external_user_id
        self.__indirect = InDirect()
        self.__direct = Direct()
        logger.end()

    def get_id(self):
        pass

    # Should be public as MessagesLocal use it
    def get_message_channel_id(self, recipient: Recipient) -> int:
        # TODO: implement
        return SMS_MESSAGE_CHANNEL_ID
        # circular import
        """
        try:
            if self.__class__ == SmsMessageAwsSns and self.check_message():
                return SMS_MESSAGE_CHANNEL_ID
        except Exception as exception:
            logger.exception("Can't determine the Message Channel", object=exception)
        """

    # Should be public as MessagesLocal use it
    def get_message_provider_id(self, message_channel_id: int, recipient: Recipient) -> int:
        """return message provider"""
        logger.start()
        if message_channel_id == SMS_MESSAGE_CHANNEL_ID and recipient.get_canonical_telephone().startswith("972"):
            return AWS_SMS_MESSAGE_PROVIDER_ID
        else:
            # TODO raise customized Exceptions
            raise Exception("Can't determine the Message Provider")
        """
        elif message_channel_id == AWS_SMS_MESSAGE_PROVIDER_ID:
            return AWS_SMS_MESSAGE_PROVIDER_ID
        elif message_channel_id == WHATSAPP_CHANNEL_ID:
            return INFORU_MESSAGE_PROVIDER_ID"""
        logger.end()

    def _set_recipient(self, recipient: Recipient) -> None:
        """set method"""
        logger.start()
        self.__to_recipient = recipient

        if self.__original_body is not None:
            template = ReplaceFieldsWithValues(message=self.__original_body, language='en', variable='')
            self.__body_after_text_template = template.get_variable_values_and_chosen_option()

        logger.end()
        return

    # Used by SmsMessage to check the length after template processing
    def check_message(self):
        raise NotImplementedError("Subclasses must implement this method.")

    def _set_recipients(self, to_recipients: List[Recipient], cc_recipients: List[Recipient]) -> None:
        """set method"""
        logger.start()
        self.__to_recipients = to_recipients
        # TODO Replace 'en' with language-python-local-package const/enum
        template = ReplaceFieldsWithValues(message=self.__original_body, language='en', variable='')
        for recipient in to_recipients:
            self.__body_after_text_template[recipient.get_person_id()][
                "body_after_text_template"] = template.get_variable_values_and_chosen_option()
        logger.end()

    def _get_body_after_text_template(self) -> dict:
        return self.__body_after_text_template

    def _get_body_after_html_template(self) -> str:
        return self.__body_after_html_template

    def _get_number_of_attachment(self) -> int:
        return 0

    def _get_subject_after_html_template(self) -> str:
        # Unresolved attribute reference '__subject_after_html_template' for class 'MessageLocal'
        return self.__subject_after_html_template

    def _get_type_of_attachments(self):
        return None

    def _can_send(self, sender_profile_id: int = None, api_data: dict = None, outgoing_body: dict = None) -> bool:
        if self._is_http_api:
            return self._can_send_direct(sender_profile_id=self.__external_user_id, api_data=api_data)
        else:
            return self._can_send_indirect(sender_profile_id=self.__external_user_id, outgoing_body=outgoing_body)

    def _can_send_direct(self, sender_profile_id: int = None, api_data: dict = None) -> bool:
        try:
            # TODO: change try_to_call_api typing
            try_to_call_api_result = self.__direct.try_to_call_api(
                external_user_id=self.__external_user_id,
                api_type_id=self._api_type_id,
                endpoint=self._endpoint,
                outgoing_body=json.dumps(api_data, separators=(",", ":")),  # data
                outgoing_header=json.dumps(self._headers)
            )
            x = try_to_call_api_result['status_code']
            if x != http.HTTPStatus.OK:
                raise Exception(try_to_call_api_result['text'])
            else:
                return True
        except PassedTheHardLimitException:
            # example_instance=APIManagementsLocal()
            x = APIMangementManager.seconds_to_sleep_after_passing_the_hard_limit(
                api_type_id=self._api_type_id)
            if x > 0:
                logger.info("sleeping : " + str(x) + " seconds")
                time.sleep(x)
            else:
                logger.info("No sleeping needed : x= " + str(x) + " seconds")
        except NotEnoughStarsForActivityException:
            logger.warn("Not Enough Stars For Activity Exception")

        except ApiTypeDisabledException:
            logger.error("Api Type Disabled Exception")

        except ApiTypeIsNotExistException:
            logger.error("Api Type Is Not Exist Exception")

        except Exception as exception:
            logger.exception(object=exception)
            logger.info(str(exception))
        return False

    def _can_send_indirect(self, sender_profile_id: int = None, outgoing_body: dict = None) -> bool:
        # TODO: return true/false
        http_status_code = None
        try:
            api_check, self.__api_call_id, arr = self.__indirect.before_call_api(
                external_user_id=self.__external_user_id, api_type_id=self._api_type_id,
                endpoint=self._endpoint,
                outgoing_header=json.dumps(self._headers),
                outgoing_body=json.dumps(outgoing_body)
            )
            if arr is None:
                self.__used_cache = False
                if api_check == APILimitStatus.BETWEEN_SOFT_LIMIT_AND_HARD_LIMIT:
                    logger.warn("You excced the soft limit")
                if api_check != APILimitStatus.GREATER_THAN_HARD_LIMIT:
                    try:
                        # user = user_context.login_using_user_identification_and_password(outgoing_body)
                        http_status_code = http.HTTPStatus.OK.value
                    except Exception as exception:
                        logger.exception(object=exception)
                        http_status_code = http.HTTPStatus.BAD_REQUEST.value
                else:
                    logger.info(" You passed the hard limit")
                    x = APIMangementManager.seconds_to_sleep_after_passing_the_hard_limit(
                        api_type_id=self._api_type_id)
                    if x > 0:
                        logger.info("sleeping : " + str(x) + " seconds")
                        time.sleep(x)
                        # raise PassedTheHardLimitException

                    else:
                        logger.info("No sleeping needed : x= " + str(x) + " seconds")
            else:
                self.__used_cache = True
                logger.info("result from cache")
                # print(arr)
                http_status_code = http.HTTPStatus.OK.value
        except ApiTypeDisabledException:
            logger.error("Api Type Disabled Exception")

        except ApiTypeIsNotExistException:
            logger.error("Api Type Is Not Exist Exception")
        logger.info("http_status_code: " + str(http_status_code))

    def send(self, recipients: List[Recipient], cc: List[Recipient] = None, bcc: List[Recipient] = None,
             scheduled_timestamp_start: Union[str, datetime] = None,
             scheduled_timestamp_end: Union[str, datetime] = None) -> None:
        """send method"""
        logger.start()

        # message_channel = MessagesLocal._get_message_channel_id()
        # provider_id = MessagesLocal._get_message_provider_id(message_channel)
        # TODO Based on message_channel and provider assign value to _is_direct_api
        # and create the relevant Message object
        # TODO Based on _is_direct_api call API-Management Direct or
        # InDirect (see API Management tests direct.py)
        logger.end()

    def _after_send_attempt(self, sender_profile_id: int = None, outgoing_body: dict = None,
                            incoming_message: str = None,
                            http_status_code: int = None, response_body: str = None) -> None:
        if self._is_http_api:
            self.after_direct_send()
        else:
            self.after_indirect_send(sender_profile_id=self.__external_user_id,
                                     outgoing_body=outgoing_body,
                                     incoming_message=incoming_message,
                                     http_status_code=http_status_code,
                                     response_body=response_body)

    def display(self):
        print(self.__original_body)

    def after_indirect_send(self, sender_profile_id: int, outgoing_body: dict, incoming_message: str,
                            http_status_code: int, response_body: str):
        self.__indirect.after_call_api(external_user_id=self.__external_user_id,
                                       api_type_id=self._api_type_id,
                                       endpoint=self._endpoint,
                                       outgoing_header=json.dumps(self._headers),
                                       outgoing_body=json.dumps(outgoing_body),
                                       incoming_message=incoming_message,
                                       http_status_code=http_status_code,
                                       response_body=response_body,
                                       api_call_id=self.__api_call_id,
                                       used_cache=self.__used_cache)

    def after_direct_send(self):
        pass

    def was_read(self) -> bool:
        """read method"""
        pass

    def get_importance(self) -> MessageImportance:
        """get method"""
        return self.importance
