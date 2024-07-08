import json
import os

class ReaderJson:
    def __init__(self, file_path=None):
        self.file_path = file_path
        self.data = None

    def read_json(self):
        if not self.file_path:
            raise ValueError("File path is not set.")

        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"File '{self.file_path}' not found.")

        with open(self.file_path, 'r') as file:
            self.data = json.load(file)
            messages = []

            for test in self.data.get("Pruebas", []):
                message = f"Test {test.get('Number_Test', 'N/A')}: "
                message += f"Slave_Address: {test.get('Slave_Address', 'N/A')}, "
                message += f"Function_Code: {test.get('Function_code', 'N/A')}, "
                message += f"Starting_Address: {test.get('Starting_address', 'N/A')}, "
                message += f"Quantity: {test.get('Quantity', 'N/A')}, "
                message += f"CRC_MSB: {test.get('CRC_MSB', 'N/A')}, "
                message += f"CRC_LSB: {test.get('CRC_LSB', 'N/A')}"
                messages.append(message)
                print (message)

            return messages

    def set_file_path(self, file_path):
        self.file_path = file_path
        print(f"File path set to: {self.file_path}")
