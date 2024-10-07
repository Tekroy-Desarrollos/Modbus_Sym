import struct
import CRC as crc
class ModbusDecoder:
    def __init__(self):
        pass

    def decode(self, frame):
        print("Inicio de proceso de decodificación")
        print("Frame: ", frame)
        """Decodifica una trama Modbus RTU"""
        if len(frame) < 4:
            raise ValueError("Trama demasiado corta")

        # Separar los componentes de la trama
        address = frame[0]
        function_code = frame[1]
        data = frame[2:-2]
        crc_received = struct.unpack('<H', frame[-2:])[0]  # Últimos 2 bytes son CRC
        
        # Validar el CRC
        crc_calculated = crc.CRC(frame[:-2])
        if crc_calculated != crc_received:
            raise ValueError("Error de CRC: esperado {}, recibido {}".format(crc_calculated, crc_received))
        
        # Decodificar en base al código de función
        if function_code == 3:  # Lectura de registros
            print("Decodificando lectura de registros")
            return self.decode_read_holding_registers(data)
        
        elif function_code == 16:  # Escritura múltiple de registros
            print("Decodificando escritura múltiple de registros")
            return self.decode_write_multiple_registers(data)
        
        elif function_code == 6:  # Escritura de un solo registro
            print("Decodificando escritura de un solo registro")
            return self.decode_write_single_register(data)
        
        elif function_code == 4:  # Lectura de registros de entrada
            print("Decodificando lectura de registros de entrada")
            return self.decode_read_input_registers(data)
        
        else:
            print("Error: Código de función no soportado")
            raise ValueError("Código de función no soportado: {}".format(function_code))

    def decode_read_holding_registers(self, data):
        """Decodifica la respuesta de lectura de registros (función 3)"""
        byte_count = data[0]
        registers = []
        for i in range(1, byte_count, 2):
            registers.append(struct.unpack('>H', data[i:i+2])[0])  # Leer 2 bytes por registro
        return {
            'function': 3,
            'registers': registers
        }

    def decode_write_multiple_registers(self, data):
        """Decodifica la confirmación de escritura múltiple de registros (función 16)"""
        start_address = struct.unpack('>H', data[:2])[0]
        quantity_of_registers = struct.unpack('>H', data[2:4])[0]
        return {
            'function': 16,
            'start_address': start_address,
            'quantity_of_registers': quantity_of_registers
        }
    def decode_write_single_register(self, data):
        """Decodifica la confirmación de escritura de un solo registro (función 6)"""
        address = struct.unpack('>H', data[:2])[0]
        value = struct.unpack('>H', data[2:4])[0]
        return {
            'function': 6,
            'address': address,
            'value': value
        }
    def decode_read_input_registers(self, data):
        """Decodifica la respuesta de lectura de registros de entrada (función 4)"""
        byte_count = data[0]
        registers = []
        for i in range(1, byte_count, 2):
            registers.append(struct.unpack('>H', data[i:i+2])[0])
        return {
            'function': 4,
            'registers': registers
        }

# # Ejemplo de uso
# if __name__ == "__main__":
#     decoder = ModbusDecoder()

#     # Trama Modbus RTU simulada: Dirección 0x01, Función 0x03 (Leer Holding Registers)
#     # Trama: [0x01, 0x03, 0x04, 0x00, 0x0A, 0x00, 0x0B, CRC]
#     frame = bytearray([0x01, 0x06, 0x00, 0x0A, 0x03, 0xE8, 0xA9, 0x76])

#     try:
#         result = decoder.decode(frame)
#         print("Decodificación exitosa:", result)
#     except ValueError as e:
#         print("Error al decodificar la trama:", e)