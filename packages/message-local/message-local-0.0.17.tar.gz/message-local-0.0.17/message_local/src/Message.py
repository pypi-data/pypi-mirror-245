"""imports"""
from abc import ABC, abstractmethod
from enum import Enum
from .MessageConstants import *
from .MessageImportance import MessageImportance
from item_local.item import Item
from api_management_local.api_management_local import APIManagementsLocal
from api_management_local.indirect import InDirect
from api_management_local.Exception_API import ApiTypeDisabledException,ApiTypeIsNotExistException,PassedTheHardLimitException
from api_management_local.api_limit_status import APILimitStatus
from api_management_local.API_Mangement_Manager import APIMangementManager
from api_management_local.direct import Direct
from star_local.exception_star import NotEnoughStarsForActivityException
from variable_local.replace_fields_with_values import ReplaceFieldsWithValues

from .Recipient import *
import http
import json
import time

class Message(Item, ABC):
    """Message Class"""
    
    _is_direct_api = None
    _api_type_id = None
    _endpoint = None
    _headers = None
    __used_cache = None
    __original_body: str = None
    __original_subject: str = None
    __external_user_id: int = None

    __body_after_text_template = None
    __body_after_html_template = None
    __body_after_text_template_length = None
    __body_after_html_template_length = None


    def __init__(self, original_body: str, importance: MessageImportance, is_direct_api: bool, api_type_id:int, endpoint:str,
                 original_subject: str = None, headers: dict = DEFAULT_HEADERS, external_user_id: int = None ) -> None:
        # TODO We should add all fields from message schema in the database
        # (i.e. message_id, scheduled_sent_timestamp, message_sent_status : MessageSentStatus  ...)
        logger.start()
        self.__original_subject = original_subject
        self.__original_body = original_body
        self.importance = importance
        self._is_direct_api = is_direct_api
        self._api_type_id = api_type_id
        self._endpoint = endpoint
        self._headers = headers
        self.__external_user_id = external_user_id
        self.__indirect = InDirect()
        self.__direct = Direct()
        logger.end()

    def set_recipient(self, recipient: Recipient) -> None:
        """set method"""
        logger.start()
        self.__to_recipient = recipient
        
        if self.__original_body is not None:
            template = ReplaceFieldsWithValues( message = self.__original_body, language = 'en', variable = ''  )
            self.__body_after_text_template = template.get_variable_values_and_chosen_option()
            self.__body_after_text_template_length = len(self.__body_after_text_template)
            
        logger.end()
        return 

    def set_recipients(self, to_recipients: list, cc_recipients: list(Recipient)) -> None:
        """set method"""
        logger.start()
        self.__to_recipients = to_recipients
        template = ReplaceFieldsWithValues( message = self.__original_body, language = 'en', variable = ''  )
        for recipient in to_recipients:
            self.__body_after_text_template[recipient].body_after_text_template = template.get_variable_values_and_chosen_option()
        logger.end()

    def get_message_after_text_template(self):
        pass       

    def get_message_after_html_template(self):
        pass

    def __get_message_after_text_template_length(self):
        pass

    def __get_message_after_html_template_length(self):
        pass

    def __get_number_of_attachment(self):
        pass

    def get_body_after_html_template(self):
        return __body_after_html_template
        
    def __get_body_after_text_template_length(self):
        return __body_after_text_template_length

    def __get_message_after_html_template_length(self):
        return __body_after_html_template_length

    def __get_number_of_attachment(self):
        return 0

    def __get_type_of_attachments(self):
        return None


    @abstractmethod
    def _can_send(self, sender_profile_id: int = None, api_data: dict = None, outgoing_body: dict = None ) -> bool:
        if self._is_direct_api:
            self._can_send_direct( sender_profie_id=self.__external_user_id, api_data=api_data)
        else:
            self._can_send_indirect( sender_profile_id=self.__external_user_id, outgoing_body=outgoing_body)

    def _can_send_direct(self, sender_profile_id: int = None, api_data: dict = None) -> bool:
        try:
            try_to_call_api_result = self.__direct.try_to_call_api(external_user_id=self.__external_user_id,
                                                                        api_type_id=self._api_type_id,
                                                                        endpoint=self._endpoint,
                                                                        outgoing_body=json.dumps(
                                                                        api_data, separators=(",", ":")),  # data
                                                                        outgoing_header=self._headers
                                                                        )
            x = try_to_call_api_result['status_code']
            if x != http.HTTPStatus.OK:
                raise Exception(try_to_call_api_result['text'])
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
            logger.error ("Api Type Is Not Exist Exception")
                
        except Exception as exception:
            logger.exception(object=exception)
            logger.info(str(exception))

    def _can_send_indirect(self, sender_profile_id:int = None, outgoing_body: dict = None):
        try:
            api_check, self.__api_call_id, arr = self.__indirect.before_call_api( external_user_id=self.__external_user_id, api_type_id=self._api_type_id,
                                                                        endpoint=self._endpoint,
                                                                        outgoing_header=self._headers,
                                                                        outgoing_body=outgoing_body
                                                                    )
            if arr == None:
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
            logger.error ("Api Type Is Not Exist Exception")

    # TODO Create a new Class of Recipient
    @abstractmethod
    # TODO Please add scheduled_timestamp_start = None and scheduled_timestamp_end = None parameters
    def send(self, recipients: list, cc: list = None, bcc: list = None) -> None:
        """send method"""
        logger.start()
        # TODO if scheduled_timestamp_start <> None then message_outbox_queue.push() - @akiva
        #message_channel = MessagesLocal._get_message_channel_id()
        #provider_id = MessagesLocal._get_message_provider_id(message_channel)
        # TODO Based on message_channel and provider assign value to _is_direct_api
        # and create the relevant Message object
        # TODO Based on _is_direct_api call API-Management Direct or
        # InDirect (see API Management tests direct.py)
        logger.end()
        raise NotImplementedError("Subclasses must implement this method.")


    @abstractmethod
    def _after_send_attempt(self, sender_profile_id:int = None, outgoing_body:dict = None, incoming_message:str = None, http_status_code:int = None, response_body:str = None) -> None:
        if self._is_direct_api:
            self.after_direct_send()
        else:
            self.after_indirect_send(external_user_id=self.__external_user_id,
                                            outgoing_body=outgoing_body,
                                            incoming_message=incoming_message,
                                            http_status_code=http_status_code,
                                            response_body=response_body)

    def display(self):
        print(self.body)
    
    def after_indirect_send(self, sender_profile_id:int, outgoing_body:dict, incoming_message:str, http_status_code:int, response_body:str):
        self.__indirect.after_call_api(external_user_id=self.__external_user_id,
                                            api_type_id=self._api_type_id,
                                            endpoint=self._endpoint,
                                            outgoing_header=self._headers,
                                            outgoing_body=outgoing_body,
                                            incoming_message=incoming_message,
                                            http_status_code=http_status_code,
                                            response_body=response_body, 
                                            api_call_id=self.__api_call_id,
                                            used_cache=self.__used_cache)
        
    def after_direct_send(self):
        pass

    @abstractmethod
    def was_read(self) -> bool:
        """read method"""
        logger.start()
        logger.error("Subclasses must implement this method.")
        logger.end()

    def get_importance(self) -> MessageImportance:
        """get method"""
        return self.importance

