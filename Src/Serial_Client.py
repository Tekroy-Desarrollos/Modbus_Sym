import serial
import time

class SerialClient:
    def __init__(self, port, baudrate=9600):
        self.port = port
        self.baudrate = baudrate
        self.serial_connection = None
        self.timeout = 100  # Tiempo de espera para la respuesta
        self.TimeOutFactor = 50  # Factor usado para calcular el timeout basado en el baudrate
        self.min_bytes = 8  # Mínimo número de bytes esperados
        self.max_bytes = 255  # Máximo número de bytes esperados

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
            return "Error: La conexión serial no está abierta"

    def receive_data(self):
        """
        Método para recibir datos desde el puerto serial.
        Lee los datos recibidos y verifica si están dentro del rango permitido.
        """
        if self.serial_connection and self.serial_connection.is_open:
            try:
                received_data = b''
                start_time = time.time()
                # Calcula el timeout en función del baudrate
                self.timeout = self.TimeOutFactor * (self.min_bytes * 10) / self.baudrate

                while True:
                    # Verifica si hay datos suficientes disponibles en el buffer
                    if self.serial_connection.in_waiting >= self.min_bytes:
                        # Lee los datos disponibles
                        received_data = self.serial_connection.read(self.serial_connection.in_waiting)
                        break
                    elif time.time() - start_time > self.timeout:
                        print("Timeout: No se recibieron todos los bytes esperados.")
                        break

                if self.min_bytes <= len(received_data) <= self.max_bytes:
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
    def read_data(self):
        """
        Método para leer los datos recibidos desde el puerto serial.
        """
        if self.serial_connection and self.serial_connection.is_open:
            try:
                received_data = self.serial_connection.read(self.serial_connection.in_waiting)
                return received_data
            except Exception as e:
                print(f"Error al leer datos: {e}")
                self.disconnect()
                return None
        else:
            print("Error: La conexión serial no está abierta")
            self.disconnect()
            return None
    def Set_TimeOut(self, baudrate):
        """
        Método para establecer el tiempo de espera (timeout) en función del baudrate.
        """
        self.baudrate = baudrate
        self.timeout = self.TimeOutFactor * (self.min_bytes * 10) / self.baudrate
        return self.timeout
