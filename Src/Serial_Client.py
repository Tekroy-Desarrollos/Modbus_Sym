# Serial_Client.py
import serial
import struct


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

    def run_test(self):
        try:
            self.connect()
        except Exception as e:
            print(f"Error: {e}")
        finally:
            self.disconnect()
