import json
import os
import Data_Transformer as func

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
                message = []

                # Obtener los campos del JSON
                try:
                    slave_address = func.hexadecimal_string_to_int(test.get('Slave_Address'))
                    function_code = func.hexadecimal_string_to_int(test.get('Function_code'))
                    starting = func.hex_string_to_array(test.get('Starting_address'))
                    quantity = func.hex_string_to_array(test.get('Quantity'))

                    message.extend([slave_address, function_code])
                    message.extend(starting)
                    message.extend(quantity)
                    message.extend([func.hexadecimal_string_to_int(test.get('CRC_MSB')), func.hexadecimal_string_to_int(test.get('CRC_LSB'))])

                    messages.append(message)

                except ValueError as e:
                    print(f"Error procesando prueba {test.get('Number_Test')}: {e}")

            return messages

    def set_file_path(self, file_path):
        self.file_path = file_path
        print(f"File path set to: {self.file_path}")
