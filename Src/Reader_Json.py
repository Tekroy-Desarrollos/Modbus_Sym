import json
import os
import Data_Transformer as func

class ReaderJson:
    def __init__(self, file_path: str = None):
        self.file_path = file_path
        self.data = None

    def read_json(self) -> list:
        """Lee el archivo JSON y procesa las pruebas."""
        self._validate_file()

        with open(self.file_path, 'r') as file:
            self.data = json.load(file)
            messages = []

            for test in self.data.get("Pruebas", []):
                message = self._process_test(test)
                if message:  # Solo agrega si el mensaje no es una lista vacía
                    messages.append(message)

            return messages

    def set_file_path(self, file_path: str):
        """Establece la ruta del archivo."""
        self.file_path = file_path
        print(f"File path set to: {self.file_path}")

    def _validate_file(self):
        """Valida si el archivo existe y si la ruta está definida."""
        if not self.file_path:
            raise ValueError("File path is not set.")
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"File '{self.file_path}' not found.")

    def _process_test(self, test: dict) -> list:
        """Procesa una prueba individual y la convierte en un mensaje."""
        try:
            # Obtener valores, y usar 0 como valor por defecto si alguno no está presente
            slave_address = func.hexadecimal_string_to_int(test.get('Slave_Address', '0x00'))
            function_code = func.hexadecimal_string_to_int(test.get('Function_code', '0x00'))
            starting = func.hex_string_to_array(test.get('Starting_address', '0x0000'))
            quantity = func.hex_string_to_array(test.get('Quantity', '0x0000'))
            crc_msb = func.hexadecimal_string_to_int(test.get('CRC_MSB', '0x00'))
            crc_lsb = func.hexadecimal_string_to_int(test.get('CRC_LSB', '0x00'))

            # Construir el mensaje
            message = [slave_address, function_code] + starting + quantity + [crc_msb, crc_lsb]
            return message
        except ValueError as e:
            print(f"Error procesando prueba {test.get('Number_Test', 'Desconocido')}: {e}")
            return []
