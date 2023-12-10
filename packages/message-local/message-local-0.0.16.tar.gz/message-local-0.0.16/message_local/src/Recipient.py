
from enum import Enum, auto


class RecipientType(Enum):
    PERSON_ID = auto()
    CONTACT_ID = auto()
    USER_ID = auto()
    PROFILE_ID = auto()

    
    TELEPHONE_NUMBER = auto()
    EMAIL_ADDRESS = auto()
    

class Recipient():

    __recipient_type: RecipientType = None    

    def __init__(self, person_id: int = None, email_address: str = None, contact_id:int = None, user_id: int = None, profile_id:int = None, telephone_number: str = None):
        self.person_id = person_id
        self.email_address = email_address
        self.contact_id = contact_id
        self.user_id = user_id
        self.profile_id = profile_id
        self.telephone_number = telephone_number
        for key, value in self.__dict__.items():
            if value is not None:
                self.__recipient_type = RecipientType[key.upper()]
                
        



    

