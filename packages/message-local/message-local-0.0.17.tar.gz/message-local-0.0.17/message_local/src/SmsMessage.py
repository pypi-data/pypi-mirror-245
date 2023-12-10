# TODO Please create SmsMessage class which inherit from Message class
from .Message import Message
from abc import ABC, abstractmethod

class SmsMessage(Message, ABC):
    pass