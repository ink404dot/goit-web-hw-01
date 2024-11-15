from typing import Callable
from enum import Enum


class ErrorMessageEnum(Enum):
    PHONE_LENGTH = "The phone number must be 10 characters long."
    NAME_LENGTH = "Length must be at least 1 character in string format."
    BIRTHDAY_FORMAT = "Invalid date format. Use DD.MM.YYYY"
    ITEM_NOT_FOUND = "Item not found"
    INVALID_COMMAND = "Invalid command."


class PhoneValidationError(Exception):
    def __init__(self, message: str = ErrorMessageEnum.PHONE_LENGTH.value) -> None:
        self.message = message
        super().__init__(self.message)


class NameValidationError(Exception):
    def __init__(self, message: str = ErrorMessageEnum.NAME_LENGTH.value) -> None:
        self.message = message
        super().__init__(self.message)


class BirthdayValidationError(Exception):
    def __init__(self, message: str = ErrorMessageEnum.BIRTHDAY_FORMAT.value) -> None:
        self.message = message
        super().__init__(self.message)


class ItemNotFoundError(Exception):
    def __init__(self, item: str = "") -> None:
        self.message = f"{ErrorMessageEnum.ITEM_NOT_FOUND.value}: {item}"
        super().__init__(self.message)


class InputErrorHandler:
    @staticmethod
    def handle_error(func: Callable) -> Callable:
        def inner(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except ValueError:
                return "Give right arguments, please.\n" +\
                    "\tDate format: string, use DD.MM.YYYY\n" +\
                    "\tName format: string, length more than 1\n" +\
                    "\tPhone format: all characters in a string are digits, length equal 10"
            except KeyError:
                return "This contact does not exist."
            except IndexError or TypeError:
                return "Not enough arguments."
            except (PhoneValidationError, NameValidationError, BirthdayValidationError, ItemNotFoundError) as e:
                return e
            except Exception as e:
                return e
        return inner
