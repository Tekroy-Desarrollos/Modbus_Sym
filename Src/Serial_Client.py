import serial
import struct

class SerialClient:
    def __init__(self, port, baudrate=9600):
        self.port = port
        self.baudrate = baudrate
        self.serial_connection = None

    def connect(self):
        self.serial_connection = serial.Serial(self.port, self.baudrate, timeout=1)

    def disconnect(self):
        if self.serial_connection and self.serial_connection.is_open:
            self.serial_connection.close()

    def set_baudrate(self, baudrate):
        self.baudrate = baudrate
        if self.serial_connection and self.serial_connection.is_open:
            self.serial_connection.baudrate = baudrate

    def calculate_crc(self, data):
        crc = 0xFFFF
        for pos in data:
            crc ^= pos
            for _ in range(8):
                if (crc & 0x0001) != 0:
                    crc >>= 1
                    crc ^= 0xA001
                else:
                    crc >>= 1
        return crc

    def read_register(self, address, count):
        if not self.serial_connection or not self.serial_connection.is_open:
            raise Exception("No hay conexión abierta")

        # Construir el mensaje Modbus RTU para leer registros
        slave_id = 1  # Esto puede variar según tu configuración
        function_code = 0x03
        message = struct.pack('>BBHH', slave_id, function_code, address, count)

        # Añadir CRC
        crc = self.calculate_crc(message)
        message += struct.pack('<H', crc)

        self.serial_connection.write(message)

        # Leer respuesta
        response = self.serial_connection.read(5 + 2 * count)
        if not response:
            raise Exception("No se recibió respuesta")

        # Validar CRC de la respuesta
        received_crc = struct.unpack('<H', response[-2:])[0]
        calculated_crc = self.calculate_crc(response[:-2])
        if received_crc != calculated_crc:
            raise Exception("CRC inválido en la respuesta")

        return response[3:-2]  # Datos del registro
