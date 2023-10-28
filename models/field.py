import re


class Field:
    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value

    def __str__(self):
        return str(self._value)


class Name(Field):
    def __init__(self, value):
        super().__init__(value)
        if not value:
            raise ValueError("Name is a required field and cannot be empty.")
        self.value = value


class Phone(Field):
    def __init__(self, value):
        if not (len(value) == 10 and value.isdigit()):
            raise ValueError("Invalid phone number format!")
        super().__init__(value)


class Birthday(Field):
    def __init__(self, value):
        # Date format: DD.MM.YYYY
        pattern = r'\d{2}\.\d{2}\.\d{4}'
        if not re.fullmatch(pattern, value):
            raise ValueError("Invalid birthday format!")
        super().__init__(value)
