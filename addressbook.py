import pickle
from typing import List, Dict, Optional
from collections import UserDict
from datetime import datetime, timedelta

from record import Record
from errors import ItemNotFoundError


class AddressBook(UserDict):
    def get_upcoming_birthdays(self) -> List[Dict[str, datetime]]:
        today = datetime.now()
        today_plus_seven_days = today + timedelta(days=7)
        upcoming_birthdays = []

        for record in self.data.values():
            greeting_date = None  # Initialize greeting_date
            if record.birthday:
                birthday_this_year = datetime.strptime(
                    str(record.birthday), "%d.%m.%Y").replace(year=today.year)

                if today <= birthday_this_year <= today_plus_seven_days:
                    greeting_date = birthday_this_year

                elif birthday_this_year < today:
                    birthday_next_year = birthday_this_year.replace(
                        year=today.year + 1)
                    if birthday_next_year <= today_plus_seven_days:
                        greeting_date = birthday_next_year

                if greeting_date and greeting_date.weekday() >= 5:
                    greeting_date += timedelta(days=(7 -
                                               greeting_date.weekday()))

                if greeting_date:
                    upcoming_birthdays.append(
                        {"name": str(record.name),
                            "birthday": greeting_date.strftime('%d.%m.%Y')}
                    )

        return upcoming_birthdays if upcoming_birthdays else 'There are no upcoming birthdays yet'

    def add_record(self, record: Record) -> None:
        self.data[record.name.value] = record

    def find(self, name: str) -> Optional[Record]:
        return self.data.get(name)

    def delete(self, name: str) -> None:
        if name in self.data:
            del self.data[name]
        else:
            raise ItemNotFoundError(item=name)

    def save_data(self, filename="addressbook.pkl"):
        with open(filename, "wb") as f:
            pickle.dump(self, f)

    @classmethod
    def load_data(cls, filename="addressbook.pkl"):
        try:
            with open(filename, "rb") as f:
                return pickle.load(f)
        except FileNotFoundError:
            return cls()

    def __str__(self) -> str:
        return '\n'.join(str(record) for record in self.data.values())