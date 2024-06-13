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
    
    def read_holding_registers(self, address, count):
        if not self.serial_connection or not self.serial_connection.is_open:
            raise Exception("No hay conexión abierta")

        # Construir el mensaje Modbus RTU para leer registros de retención
        slave_id = 1  # Ajustar según tu configuración de esclavo
        function_code = 0x03  # Código de función para leer registros de retención
        message = struct.pack('>BBHH', slave_id, function_code, address, count)

        # Añadir CRC al mensaje
        crc = self.calculate_crc(message)
        message += struct.pack('<H', crc)

        # Enviar mensaje al dispositivo Modbus
        self.serial_connection.write(message)

        # Leer la respuesta del dispositivo Modbus
        response = self.serial_connection.read(5 + 2 * count)
        if not response:
            raise Exception("No se recibió respuesta")

        # Validar CRC de la respuesta recibida
        received_crc = struct.unpack('<H', response[-2:])[0]
        calculated_crc = self.calculate_crc(response[:-2])
        if received_crc != calculated_crc:
            raise Exception("CRC inválido en la respuesta")

        # Extraer y devolver los datos de los registros de retención
        data = response[3:-2]
        return data

    def write_multiple_holding_registers(self, starting_address, values):
        if not self.serial_connection or not self.serial_connection.is_open:
            raise Exception("No hay conexión abierta")

        # Validar que los valores a escribir sean una lista o tupla
        if not isinstance(values, (list, tuple)):
            raise ValueError("Los valores deben ser proporcionados como una lista o tupla")

        # Construir el mensaje Modbus RTU para escribir múltiples registros de retención
        slave_id = 1  # Ajustar según tu configuración de esclavo
        function_code = 0x10  # Código de función para escribir múltiples registros de retención

        # Número de registros a escribir y número de bytes de datos
        quantity_of_registers = len(values)
        byte_count = quantity_of_registers * 2  # Cada registro es de 2 bytes

        # Empaquetar el mensaje Modbus RTU
        message = struct.pack('>BBHHB', slave_id, function_code, starting_address, quantity_of_registers, byte_count)

        # Añadir los valores a escribir en los registros
        for value in values:
            message += struct.pack('>H', value)

        # Añadir CRC al mensaje
        crc = self.calculate_crc(message)
        message += struct.pack('<H', crc)

        # Enviar mensaje al dispositivo Modbus
        self.serial_connection.write(message)

        # Leer la respuesta del dispositivo Modbus
        response = self.serial_connection.read(8)
        if not response:
            raise Exception("No se recibió respuesta")

        # Validar CRC de la respuesta recibida
        received_crc = struct.unpack('<H', response[-2:])[0]
        calculated_crc = self.calculate_crc(response[:-2])
        if received_crc != calculated_crc:
            raise Exception("CRC inválido en la respuesta")

        # Extraer y devolver el contenido de la respuesta
        function_code_received = response[1]
        if function_code_received != function_code:
            raise Exception(f"El dispositivo respondió con un código de función incorrecto: {function_code_received}")

        # Devolver el número de registros escritos correctamente
        starting_address_received = struct.unpack('>H', response[2:4])[0]
        quantity_of_registers_received = struct.unpack('>H', response[4:6])[0]

        return quantity_of_registers_received
    
    def read_input_registers(self, address, count):
        if not self.serial_connection or not self.serial_connection.is_open:
            raise Exception("No hay conexión abierta")

        # Construir el mensaje Modbus RTU para leer registros de entrada
        slave_id = 1  # Ajustar según tu configuración de esclavo
        function_code = 0x04  # Código de función para leer registros de entrada
        message = struct.pack('>BBHH', slave_id, function_code, address, count)

        # Añadir CRC al mensaje
        crc = self.calculate_crc(message)
        message += struct.pack('<H', crc)

        # Enviar mensaje al dispositivo Modbus
        self.serial_connection.write(message)

        # Leer la respuesta del dispositivo Modbus
        response = self.serial_connection.read(5 + 2 * count)
        if not response:
            raise Exception("No se recibió respuesta")

        # Validar CRC de la respuesta recibida
        received_crc = struct.unpack('<H', response[-2:])[0]
        calculated_crc = self.calculate_crc(response[:-2])
        if received_crc != calculated_crc:
            raise Exception("CRC inválido en la respuesta")

        # Extraer y devolver los datos de los registros de entrada
        data = response[3:-2]
        return data
    
    
    def write_multiple_holding_registers(self, starting_address, values):
        if not self.serial_connection or not self.serial_connection.is_open:
            raise Exception("No hay conexión abierta")

        # Validar que los valores a escribir sean una lista o tupla
        if not isinstance(values, (list, tuple)):
            raise ValueError("Los valores deben ser proporcionados como una lista o tupla")

        # Construir el mensaje Modbus RTU para escribir múltiples registros de retención
        slave_id = 1  # Ajustar según tu configuración de esclavo
        function_code = 0x10  # Código de función para escribir múltiples registros de retención

        # Número de registros a escribir y número de bytes de datos
        quantity_of_registers = len(values)
        byte_count = quantity_of_registers * 2  # Cada registro es de 2 bytes

        # Empaquetar el mensaje Modbus RTU
        message = struct.pack('>BBHHB', slave_id, function_code, starting_address, quantity_of_registers, byte_count)

        # Añadir los valores a escribir en los registros
        for value in values:
            message += struct.pack('>H', value)

        # Añadir CRC al mensaje
        crc = self.calculate_crc(message)
        message += struct.pack('<H', crc)

        # Enviar mensaje al dispositivo Modbus
        self.serial_connection.write(message)

        # Leer la respuesta del dispositivo Modbus
        response = self.serial_connection.read(8)
        if not response:
            raise Exception("No se recibió respuesta")

        # Validar CRC de la respuesta recibida
        received_crc = struct.unpack('<H', response[-2:])[0]
        calculated_crc = self.calculate_crc(response[:-2])
        if received_crc != calculated_crc:
            raise Exception("CRC inválido en la respuesta")

        # Verificar el código de función recibido
        function_code_received = response[1]
        if function_code_received != function_code:
            raise Exception(f"El dispositivo respondió con un código de función incorrecto: {function_code_received}")

        # Extraer y devolver el número de registros escritos correctamente
        starting_address_received = struct.unpack('>H', response[2:4])[0]
        quantity_of_registers_received = struct.unpack('>H', response[4:6])[0]

        return quantity_of_registers_received
    
    
    def run_test(self):
        # Ejemplo de cómo usar la función read_register
        try:
            # Leer 10 registros a partir de la dirección 0
            registers = self.read_register(0, 10)
            print(registers)
        except Exception as e:
            print(f"Error: {e}")
            return
