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
        self.__person_id = person_id
        self.__email_address = email_address
        self.__contact_id = contact_id
        self.__user_id = user_id
        self.__profile_id = profile_id
        self.__telephone_number = telephone_number

        for key, value in self.to_json().items():
            if not key.endswith("id"):
                self._recipient_type = RecipientType[key.upper()]  # remove the first underscore

    def get_person_id(self) -> int:
        return self.__person_id

    def is_email_address(self):
        return self.__telephone_number is not None

    def is_telephone_number(self):
        return self.__telephone_number is not None

    def get_email_address(self):
        return self.__email_address is not None

    def get_telephone_address(self):
        return self.__telephone_number is not None

    def get_canonical_telephone(self):
        return self.__telephone_number

    def to_json(self):
        return {k.replace("_Recipient__", ""): v for k, v in self.__dict__.items() if v is not None and k != "_recipient_type"}


if __name__ == '__main__':
    recipient = Recipient(person_id=1, email_address="test@test")
    print(recipient.to_json())
