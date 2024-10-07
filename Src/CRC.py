def CRC(frame):
        """Calcula el CRC de la trama Modbus RTU"""
        crc = 0xFFFF
        for pos in frame:
            crc ^= pos
            for _ in range(8):
                if (crc & 0x0001) != 0:
                    crc >>= 1
                    crc ^= 0xA001
                else:
                    crc >>= 1
        return crc