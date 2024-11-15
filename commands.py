from typing import Dict, List
from abc import ABC, abstractmethod
from enum import Enum

from addressbook import AddressBook
from record import Record
from errors import InputErrorHandler


class Command(ABC):
    def __init__(self, book: AddressBook, args: List[str] = []):
        self.args = args
        self.book = book

    @abstractmethod
    def execute(self) -> str:
        pass


class AddContactCommand(Command):
    def execute(self) -> str:
        name, phone = self.args[0], self.args[1]
        record = self.book.find(name)
        if record:
            record.add_phone(phone)
            return "Contact updated."
        else:
            record = Record(name)
            self.book.add_record(record)
            record.add_phone(phone)
            return "Contact added."


class ChangeContactCommand(Command):
    def execute(self) -> str:
        name = self.args[0]
        old_phone, new_phone, *_ = self.args[1], self.args[2]

        record = self.book.find(name)
        if record is None:
            return f'Contact {name} not found.'

        record.edit_phone(old_phone, new_phone)
        return f'Contact {name} updated successfully.'


class AddBirthdayCommand(Command):
    def execute(self) -> str:
        name, birthday = self.args[0], self.args[1]
        record = self.book.find(name)
        if record is None:
            return f'Contact {name} not found.'
        record.add_birthday(birthday)
        return "Contact updated."


class ShowBirthdayCommand(Command):
    def execute(self) -> str:
        name = self.args[0]
        record = self.book.find(name)
        if record is None:
            return f'Birthday for {name} not found.'
        return record.birthday if record.birthday else 'Birthday is None'


class ShowPhoneCommand(Command):
    def execute(self) -> str:
        name = self.args[0]
        record = self.book.find(name)
        if record is None:
            return f'Contact {name} not found.'
        return ', '.join(
            [str(phone) for phone in record.phones]
        ) if record.phones else 'No phones found.'


class ShowAllCommand(Command):
    def execute(self):
        if not self.book:
            return "No contacts."

        header = f'{"name":^12}|{"birthday":^12}|{"phones":^12}'
        rows = []

        for name, record in self.book.data.items():
            birthday_str = str(record.birthday) if record.birthday else ' '
            phones_str = ", ".join(str(phone) for phone in record.phones)
            row = f'{name:^12}|{birthday_str:^12}|{phones_str:^12}'
            rows.append(row)

        return header + '\n' + '\n'.join(rows)


class BirthdaysCommand(Command):
    def execute(self):
        upcoming_birthdays = self.book.get_upcoming_birthdays()
        if isinstance(upcoming_birthdays, str):  # If there's a message instead of a list
            return upcoming_birthdays
        else:
            return '\n'.join([f"{entry['name']} : {entry['birthday']}" for entry in upcoming_birthdays])


class EnumCommandsType(str, Enum):
    ADD = "add"
    CHANGE = "change"
    EXIT = "exit"
    CLOSE = "close"
    HELLO = "hello"
    PHONE = "phone"
    ALL = "all"
    BIRTHDAYS = "birthdays"
    ADD_BIRTHDAY = "add-birthday"
    SHOW_BIRTHDAY = "show-birthday"


command_map = {
    EnumCommandsType.ADD: AddContactCommand(),
    EnumCommandsType.CHANGE: ChangeContactCommand(),
    EnumCommandsType.PHONE: ShowPhoneCommand(),
    EnumCommandsType.ALL: ShowAllCommand(),
    EnumCommandsType.BIRTHDAYS: BirthdaysCommand(),
    EnumCommandsType.ADD_BIRTHDAY: AddBirthdayCommand(),
    EnumCommandsType.SHOW_BIRTHDAY: ShowBirthdayCommand(),
    EnumCommandsType.EXIT: "Good bye!",
    EnumCommandsType.CLOSE: "Closing the program...",
    EnumCommandsType.HELLO: "How can I help you?",
}

class InvokerInterface(ABC):
    @abstractmethod
    def __init__(self, command: EnumCommandsType, args: List[str], book):
        self.command = command
        self.args = args
        self.book = book
    @abstractmethod
    def execute_command(self, command_map: Dict[EnumCommandsType, Command]=command_map):
        pass


class Invoker:
    def __init__(self, command: EnumCommandsType, args: List[str], book):
        self.command = command
        self.args = args
        self.book = book

    @InputErrorHandler.handle_error
    def execute_command(self, command_map=command_map):
        command_class = command_map.get(self.command)
        if command_class:
            if isinstance(command_class, str):
                return command_class
            return command_class.execute(self.args, self.book)
        else:
            return "Invalid command."
