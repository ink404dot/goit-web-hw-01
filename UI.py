from commands import Invoker
from abc import ABC, abstractmethod
from typing import Tuple, List

from addressbook import AddressBook

def parse_input(user_input: str) -> Tuple[str, List]:
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, args


class UI(ABC):
    @abstractmethod
    def run(self):
        pass


class CLI_UI:
    def __init__(self):
        self.book = AddressBook.load_data() 

    def run(self):
        print("Welcome to the assistant bot!")
        while True:
            user_input = input("Enter a command: ")
            command, args = parse_input(user_input)
            invoker = Invoker(self.book, command, args)
            print(invoker.execute_command())
            if command.lower() in ("close", "exit"):
                break

