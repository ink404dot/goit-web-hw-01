from abc import ABC, abstractmethod
from datetime import datetime
from errors import NameValidationError, PhoneValidationError, BirthdayValidationError


class Field(ABC):
    @abstractmethod
    def __init__(self, value: str):
        self.value = value

    @abstractmethod
    def validate(self) -> bool:
        pass

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @abstractmethod
    def validate(value: str) -> bool:
        pass


class Name(Field):
    def __init__(self, value: str):
        if self.validate(value):
            super().__init__(value)
        else:
            raise NameValidationError()

    @staticmethod
    def validate(value: str) -> bool:
        return isinstance(value, str) and len(value) > 1


class Phone(Field):
    def __init__(self, value: str):
        if self.validate(value):
            super().__init__(value)
        else:
            raise PhoneValidationError()

    @staticmethod
    def validate(value: str) -> bool:
        return len(value) == 10 and value.isdigit()


class Birthday(Field):
    def __init__(self, value: str):
        if self.validate(value):
            super().__init__(value)
        else:
            raise BirthdayValidationError()

    @staticmethod
    def validate(value: str) -> bool:
        try:
            datetime.strptime(value, "%d.%m.%Y")
            return True
        except ValueError:
            return False
