import serial

class SerialClient:
    def __init__(self, port, baudrate=9600):
        self.port = port
        self.baudrate = baudrate
        self.serial_connection = None

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

    def receive_data(self, num_bytes):
        if self.serial_connection and self.serial_connection.is_open:
            try:
                received_data = self.serial_connection.read(num_bytes)
                print(f"Datos recibidos: {received_data}")
                return received_data
            except Exception as e:
                print(f"Error al recibir datos: {e}")
                return None
        else:
            print("Error: La conexión serial no está abierta")
            return None

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
