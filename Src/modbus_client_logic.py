import time
from tkinter import messagebox
from Serial_Client import SerialClient
from Reader_Json import ReaderJson
import modbus_Decoder as ModbusDecoder
import json
from JsonWriter import JsonWriter

class ModbusClientLogic:
    def __init__(self, port='/dev/ttyUSB0', baudrate=9600):
        self.serial_client = SerialClient(port, baudrate)
        self.reader = ReaderJson()
        self.ModbusDecoder = ModbusDecoder.ModbusDecoder()
        self.no_response_count = 0
        self.timeout = 2  # Tiempo de espera en segundos
        self.json_writer = JsonWriter() 

    def connect(self, port, baudrate):
        self.serial_client = SerialClient(port, baudrate)
        try:
            self.serial_client.connect()
            return True, "Conectado exitosamente"
        except Exception as e:
            return False, str(e)

    def update_baudrate(self, baudrate):
        if self.serial_client:
            self.serial_client.set_baudrate(baudrate)
            return self.serial_client.Set_TimeOut(baudrate)
        else:
            return "Error: No se ha establecido una conexión serial"

    def scan_ports(self):
        import sys, glob
        import serial.tools.list_ports as list_ports

        tty_ports = []
        if sys.platform.startswith('win'):
            ports = list_ports.comports()
            tty_ports = [port.device for port in ports]
        elif sys.platform.startswith('linux') or sys.platform.startswith('darwin'):
            tty_ports = glob.glob('/dev/ttyUSB*') + glob.glob('/dev/ttyACM*')
        return tty_ports

    def init_test(self, file_path, result_file_path):
        if file_path:
            self.reader.set_file_path(file_path)
            data = self.reader.read_json()
            results = []

            for i, test_data in enumerate(data):
                response = self.serial_client.send_data(bytearray(test_data))
                time.sleep(0.1)

                if response == "Error: La conexión serial no está abierta":
                    return False, "Error al enviar datos al dispositivo"

                if not self.wait_for_response():
                    self.no_response_count += 1
                    result = {
                        "Prueba": i + 1,
                        "Resultado": "Sin respuesta",
                        "Datos_enviados": test_data
                    }
                else:
                    decoded_response = self.ModbusDecoder.decode(response)
                    result = {
                        "Prueba": i + 1,
                        "Resultado": "Respuesta recibida",
                        "Respuesta decodificada": decoded_response,
                        "Datos_enviados": test_data
                    }

                results.append(result)
                time.sleep(1)

            # Escribir los resultados en JSON usando JsonWriter
            self.json_writer.set_file_path(result_file_path)
            self.json_writer.append_results(results, self.no_response_count)

            return True, f"Total de pruebas sin respuesta: {self.no_response_count}"
        else:
            return False, "Por favor, selecciona un archivo antes de iniciar la prueba."

    def wait_for_response(self):
        start_time = time.time()
        while (time.time() - start_time) < self.timeout:
            response = self.serial_client.read_data()
            if response:
                if response == "[Errno 5] Input/output error":
                    break
                return True
            time.sleep(0.1)
        return False
