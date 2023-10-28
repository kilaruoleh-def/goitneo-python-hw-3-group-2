import calendar
from collections import UserDict
from datetime import datetime, timedelta, date


def is_leap_year(year: int) -> bool:
    """Check if a year is a leap year."""
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


class AddressBook(UserDict):
    def add_record(self, record):
        if record.name.value not in self.data:
            self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def get_birthdays_per_week(self):
        days_mapping = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        today = datetime.today().date()
        end_of_week = today + timedelta(days=6)

        birthdays_per_week = {day: [] for day in days_mapping}

        for name, record in self.data.items():
            if record.birthday:
                birthday_str = record.show_birthday()
                if not birthday_str:
                    continue

                birthday = datetime.strptime(birthday_str, '%d.%m.%Y').date()
                birthday_this_year = birthday.replace(year=today.year)

                if birthday.month == 2 and birthday.day == 29 and not calendar.isleap(today.year):
                    birthday_this_year = birthday_this_year.replace(day=28)

                if birthday_this_year < today:
                    birthday_this_year = birthday_this_year.replace(year=today.year + 1)

                if today <= birthday_this_year <= end_of_week:
                    day_of_week_index = birthday_this_year.weekday()
                    if day_of_week_index >= 5:
                        day_of_week_index = 0
                    day_of_week = days_mapping[day_of_week_index]
                    birthdays_per_week[day_of_week].append(name)

        result = {day: names for day, names in birthdays_per_week.items() if names}

        return result
