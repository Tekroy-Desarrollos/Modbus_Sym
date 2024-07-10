import serial
import time

class SerialClient:
    def __init__(self, port, baudrate=9600):
        self.port = port
        self.baudrate = baudrate
        self.serial_connection = None
        self.Timeout = 0.0
        self.TimeOutFactor = 3.5
        self.min_bytes = 8
        self.max_bytes = 255

    def connect(self):
        try:
            self.serial_connection = serial.Serial(self.port, self.baudrate, timeout=1)
            print("Conexión establecida en el puerto:", self.port)
        except Exception as e:
            print("Error al conectar:", e)
            self.serial_connection = None

    def disconnect(self):
        if self.serial_connection and self.serial_connection.is_open:
            self.serial_connection.close()

    def set_baudrate(self, baudrate):
        self.baudrate = baudrate
        if self.serial_connection and self.serial_connection.is_open:
            self.serial_connection.baudrate = baudrate

    def send_data(self, data):
        if self.serial_connection and self.serial_connection.is_open:
            try:
                self.serial_connection.write(data)
                print(f"Datos enviados: {data}")
            except Exception as e:
                print(f"Error al enviar datos: {e}")
        else:
            print("Error: La conexión serial no está abierta")

def receive_data(self):
    if self.serial_connection and self.serial_connection.is_open:
        try:
            received_data = b''
            start_time = time.time()
            while True:
                if self.serial_connection.in_waiting >= self.min_bytes:
                    # Leer al menos el mínimo de bytes necesarios
                    received_data = self.serial_connection.read(self.serial_connection.in_waiting)
                    break
                elif time.time() - start_time > self.timeout:
                    print("Timeout: No se recibieron todos los bytes esperados.")
                    break
            
            if self.min_bytes <= len(received_data) <= self.max_bytes:
                print(f"Datos recibidos: {received_data}")
                return received_data
            else:
                print("Error: La cantidad de bytes recibidos no está dentro del rango esperado.")
                return None
        
        except Exception as e:
            print(f"Error al recibir datos: {e}")
            return None
    
    else:
        print("Error: La conexión serial no está abierta")
        return None

        
    def Set_TimeOut(self, BaudRate):
        self.Timeout = self.TimeOutFactor / BaudRate
        serial.Timeout = self.Timeout
        return "Timeout set to: " + str(self.Timeout)
        
    def Get_TimeOut(self):
        return self.Timeout

    def run_test(self):
        try:
            self.connect()
            # Ejemplo de recepción de datos (lee 10 bytes)
            received_data = self.receive_data(10)
            if received_data:
                print("Datos recibidos exitosamente:", received_data)
            # Aquí puedes colocar más lógica para procesar los datos recibidos
        except Exception as e:
            print(f"Error: {e}")
        finally:
            self.disconnect()
