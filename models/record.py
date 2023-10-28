from models.field import Name, Phone, Birthday


class Record:
    def __init__(self, name, phone):
        self.name = Name(name)
        self.phone = Phone(phone)
        self.birthday = None

    def show_phone(self):
        return self.phone.value

    def change_phone(self, new_phone):
        self.phone = Phone(new_phone)

    def add_birthday(self, date):
        self.birthday = Birthday(date)

    def show_birthday(self):
        return self.birthday.value if self.birthday else "No birthday added."

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {self.phone.value}"

    def to_dict(self):
        return {
            "name": self.name.value,
            "phone": self.phone.value,
            "birthday": self.birthday.value if self.birthday else None
        }

    @classmethod
    def from_dict(cls, data):
        record = cls(data["name"], data["phone"])
        if data["birthday"]:
            record.birthday = Birthday(data["birthday"])
        return record
