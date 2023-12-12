# TODO Please create SmsMessage class which inherit from Message class
from abc import ABC

from .MessageLocal import MessageLocal

SMS_MESSAGE_LENGTH = 160
UNICODE_SMS_MESSAGE_LENGTH = 70


class SmsMessage(MessageLocal, ABC):
    pass

    def check_message():
        # TODO Check that there is only body without subject
        # TODO Check that there is no HTML
        # TODO Check the length of the self.__body_after_text_template is in the right length
        pass
