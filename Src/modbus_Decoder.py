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
        match function_code:
            case 3:  # Lectura de registros
                print("Decodificando lectura de registros")
                return self.decode_read_holding_registers(data)
            case 16:  # Escritura múltiple de registros
                print("Decodificando escritura múltiple de registros")
                return self.decode_write_multiple_registers(data)
            case 6:  # Escritura de un solo registro
                print("Decodificando escritura de un solo registro")
                return self.decode_write_single_register(data)
            case 4:  # Lectura de registros de entrada
                print("Decodificando lectura de registros de entrada")
                return self.decode_read_input_registers(data)
            
            case _:  # Código de función no soportado
                print("Decodificando mensaje de error")
                return self.Decode_Error_Message(frame)


    def Decode_Error_Message(self,data):
        """Decodifica un mensaje de error"""
        error_code = data[1]
        return {
            'data': data.hex(' '),  # Datos en formato hexadecimal legible
            'error_code': f"0x{error_code:02X}"  # Código de error en formato hexadecimal
    }
        
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
        


