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


class Recipient:
    __main_recipient_type: RecipientType = None

    def __init__(self, contact_id: int = None, person_id: int = None, user_id: int = None, profile_id: int = None,
                 telephone_number: str = None, email_address: str = None):
        self.person_id = person_id
        self.email_address = email_address
        self.contact_id = contact_id
        self.user_id = user_id
        self.profile_id = profile_id
        self.telephone_number = telephone_number

        for key, value in self.to_json().items():
            self._recipient_type = RecipientType[key.upper()]

    def is_email_address(self):
        return self.telephone_number is not None

    def is_telephone_number(self):
        return self.telephone_number is not None

    def get_email_address(self):
        return self.email_address is not None

    def get_telephone_address(self):
        return self.telephone_number is not None

    def to_json(self):
        return {k: v for k, v in self.__dict__.items() if v is not None and not k.startswith("_")}
