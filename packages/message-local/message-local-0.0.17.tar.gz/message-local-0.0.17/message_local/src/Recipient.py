
from enum import Enum, auto

class ReferenceType(Enum):
    PERSON_ID = auto()
    CONTACT_ID = auto()
    USER_ID = auto()
    PROFILE_ID = auto()

class RecipientType(Enum):
    TELEPHONE_NUMBER = auto()
    EMAIL_ADDRESS = auto()
    
    UNKNOWN = auto()

class Recipient():

    __main_recipient_type: RecipientType = None

    def __init__(self, contact_id:int = None, person_id: int = None,  user_id: int = None, profile_id:int = None,
                 telephone_number: str = None, email_address: str = None):
        self.__person_id = person_id
        self.__email_address = email_address
        self.__contact_id = contact_id
        self.__user_id = user_id
        self.__profile_id = profile_id
        self.__telephone_number = telephone_number

        for key, value in self.__dict__.items():
            if value is not None:
                self.__recipient_type = RecipientType[key.upper()]
                
    def is_telephon_number(self):
        return self.__telephone_number != None     

    def is_email_address(self):
        return self.__telephone_number != None     


    

