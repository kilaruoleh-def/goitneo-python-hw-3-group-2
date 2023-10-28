import re
from typing import Optional

from errors.error_decorator import input_error
from models.adress_book import AddressBook
from models.field import Birthday
from models.record import Record
from storage.storage import Storage


class AssistantBot:
    def __init__(self) -> None:
        """Initialize the bot with an empty contacts dictionary."""
        self.book = AddressBook(Storage.load_from_file())

    def execute_command(self, command: str) -> str:
        """Execute a given command and return the bot's response."""
        command_pattern = re.compile(r'(\w+(?:-\w+)?)(?:\s+(.*))?')
        match = command_pattern.match(command)

        if not match:
            return "Invalid command."

        cmd, args = match.groups()
        cmd = cmd.lower()

        command_function = {
            "hello": self.hello,
            "add": self.add_contact,
            "change": self.change_contact,
            "phone": self.show_phone,
            "all": self.show_all,
            "add-birthday": self.add_birthday,
            "show-birthday": self.show_birthday,
            "birthdays": self.birthdays
        }.get(cmd)

        if command_function:
            return command_function(args)

        if cmd in ["close", "exit"]:
            Storage.save_to_file(self.book.data)
            raise SystemExit("Good bye!")

        return "Invalid command."

    def hello(self, _: Optional[str]) -> str:
        """Handle the 'hello' command."""
        return "How can I help you?"

    @input_error
    def add_contact(self, args: Optional[str]) -> str:
        """Add a contact to the book's data dictionary."""
        if not args or len(args.split()) != 2:
            raise ValueError
        name, phone = map(str.strip, args.split(None, 1))
        self.book.data[name] = Record(name, phone)
        return "Contact added."

    @input_error
    def change_contact(self, args: Optional[str]) -> str:
        """Change the phone number of an existing contact."""
        if not args or len(args.split()) != 2:
            raise ValueError
        name, new_phone = map(str.strip, args.split())
        if name not in self.book.data:
            raise KeyError
        self.book.data[name].change_phone(new_phone)
        return "Contact updated."

    @input_error
    def show_phone(self, args: Optional[str]) -> str:
        """Show the phone number for a given contact name."""
        if not args:
            raise ValueError
        name = args.strip()
        record = self.book.find(name)
        if not record:
            raise KeyError
        return record.show_phone()

    @input_error
    def show_all(self, _: Optional[str]) -> str:
        """Show all saved contacts and their phone numbers."""
        if not self.book.data:
            raise IndexError
        return '\n'.join([f"{name}: {record.show_phone()}" for name, record in self.book.data.items()])

    @input_error
    def add_birthday(self, args):
        if not args:
            return "Invalid format for adding birthday. Use 'add-birthday [name] [DD.MM.YYYY]'."
        name, birthday = args.split(None, 1)
        record = self.book.find(name)
        if record:
            record.add_birthday(Birthday(birthday))
            return f"Birthday added for {name}."
        return f"No contact found for name: {name}."

    @input_error
    def show_birthday(self, args):
        name = args.strip()
        record = self.book.find(name)
        if record and record.birthday:
            return record.birthday.value
        return f"No birthday data found for name: {name}."

    @input_error
    def birthdays(self, _):
        upcoming_birthdays = self.book.get_birthdays_per_week()
        if not upcoming_birthdays:
            return "No birthdays in the upcoming week."
        output = []
        for day, names in upcoming_birthdays.items():
            output.append(f"{day}: {', '.join(names)}")
        return '\n'.join(output)
