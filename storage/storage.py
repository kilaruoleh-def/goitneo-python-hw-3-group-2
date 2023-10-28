import json

from models.record import Record


class Storage:

    @staticmethod
    def save_to_file(data, filename="address_book.json"):
        serializable_data = {key: record.to_dict() for key, record in data.items()}
        with open(filename, 'w') as file:
            json.dump(serializable_data, file)

    @staticmethod
    def load_from_file(filename="address_book.json"):
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
                return {name: Record.from_dict(record_data) for name, record_data in data.items()}
        except FileNotFoundError:
            return {}
