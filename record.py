from typing import List, Optional

from errors import PhoneValidationError, ItemNotFoundError
from fields import Phone, Name, Birthday


class Record:
    def __init__(self, name: str):
        self.name = Name(name)
        self.phones: List[Phone] = []
        self.birthday: Optional[Birthday] = None

    def add_birthday(self, string):
        self.birthday = Birthday(string)

    def add_phone(self, value: str) -> None:
        self.phones.append(Phone(value))

    def remove_phone(self, value: str) -> None:
        for phone in self.phones:
            if phone.value == value:
                self.phones.remove(phone)
                return
        raise ItemNotFoundError(value)

    def find_phone(self, value: str) -> Optional[Phone]:
        matching_phones = [
            phone for phone in self.phones if phone.value == value]
        return matching_phones[0] if matching_phones else None

    def edit_phone(self, old_value: str, new_value: str) -> None:
        if Phone.validate(new_value):
            self.remove_phone(old_value)
            self.add_phone(new_value)
        else:
            raise PhoneValidationError()

    def __str__(self) -> str:
        return f"Contact name: {self.name.value}, phones: {
            '; '.join(p.value for p in self.phones)}"
