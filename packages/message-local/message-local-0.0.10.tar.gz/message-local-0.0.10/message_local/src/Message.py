"""imports"""
from abc import ABC, abstractmethod
from enum import Enum

from item_local.item import Item
from api_management_local.api_management_local import APIManagmentLocal
from api_management_local.indirect import InDirect
from logger_local.Logger import Logger
from logger_local.LoggerComponentEnum import LoggerComponentEnum

from MessagesLocal import logger
from MessagesLocal import MessagesLocal


class MessageImportance(Enum):
    """Enum class"""
    logger.start()
    LOW = 10
    MEDIUM = 20
    HIGH = 30
    logger.end()


class Message(Item, ABC):
    """Message Class"""

    def __init__(self, body: str, importance: MessageImportance, subject: str = None) -> None:
        # TODO We should add all fields from message schema in the database
        # (i.e. message_id, scheduled_sent_timestamp, message_sent_status : MessageSentStatus  ...)
        logger.start()
        self.body = body
        self.importance = importance
        self.subject = subject
        logger.end()

    # TODO Create a new Class of Recipient
    @abstractmethod
    # TODO Please add scheduled_timestamp_start = None and scheduled_timestamp_end = None parameters
    def send(self, recipients: list, cc: list = None, bcc: list = None) -> None:
        """send method"""
        logger.start()
        # TODO if scheduled_timestamp_start <> None then message_outbox_queue.push() - @akiva
        message_channel = MessagesLocal._get_message_channel_id()
        provider_id = MessagesLocal._get_message_provider_id(message_channel)
        # TODO Based on message_channel and provider assign value to _is_direct_api
        # and create the relevant Message object
        # TODO Based on _is_direct_api call API-Management Direct or
        # InDirect (see API Management tests direct.py)
        logger.end()
        raise NotImplementedError("Subclasses must implement this method.")

    @abstractmethod
    def was_read(self) -> bool:
        """read method"""
        logger.start()
        logger.error("Subclasses must implement this method.")
        logger.end()

    def get_importance(self) -> MessageImportance:
        """get method"""
        return self.importance

    @abstractmethod
    def __can_send(self) -> bool:
        InDirect().before_call_api
        raise NotImplementedError(
            APIManagmentLocal()._get_hard_limit_by_api_type_id(MessageImportance.HIGH))

    @abstractmethod
    def _after_send_attempt(self) -> None:
        InDirect().before_call_api
        """Update the DB if sent successfully, or with the problem details"""
        raise NotImplementedError(
            "Update the DB if sent successfully, or with the problem details")

    def display(self):
        print(self.body)