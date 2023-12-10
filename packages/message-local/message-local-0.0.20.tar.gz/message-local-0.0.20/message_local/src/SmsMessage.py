# TODO Please create SmsMessage class which inherit from Message class
from .Message import MessageLocal
from abc import ABC, abstractmethod
from logger_local import Logger

logger = Logger()

SMS_MESSAGE_LENGTH = 160
UNICODE_SMS_MESSAGE_LENGTH = 70

class SmsMessage(MessageLocal, ABC):

    def check_message(self):
        #TODO Check that there is only body without subject
        #TODO Check that there is no HTML
        #TODO Check the length of the self._body_after_text_template is in the right length
        if self._body_after_text_template_length > SMS_MESSAGE_LENGTH:
            logger.error("Message too long")
            # TODO Add customized Exception
            raise
        if self._subject_after_text_template is not None:
            logger.error("Can't send subject over SMS")
            # TODO Add customized Exception
            raise
