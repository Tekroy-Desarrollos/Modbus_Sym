import tkinter as tk
from tkinter import messagebox, filedialog, ttk  # Importar messagebox, filedialog y ttk para Combobox
from Serial_Client import SerialClient  # Asegúrate de tener SerialClient definido correctamente
from Reader_Json import ReaderJson
import serial.tools.list_ports as list_ports
import sys
import glob
import time
import modbus_Decoder as ModbusDecoder

# Crear una instancia de SerialClient
client = SerialClient(port='/dev/ttyUSB0', baudrate=9600)

class App:
    def __init__(self, root):
        self.ModbusDecoder = ModbusDecoder.ModbusDecoder()
        self.root = root
        self.root.title("Modbus Client")

        # Inicializar el lector de JSON con la ruta del archivo aún no especificada
        self.reader = ReaderJson()

        # Variables de uso general
        self.serial_client = None
        self.File_path = None
        self.response = None
        self.ResponseDecoderModbus = None

        # Crear la interfaz gráfica del selector de puerto
        self.port_label = tk.Label(root, text="Puerto:")
        self.port_label.grid(row=0, column=0, padx=10, pady=5, sticky='w')
        self.port_combobox = ttk.Combobox(root)
        self.port_combobox.grid(row=0, column=1, padx=10, pady=5, sticky='ew')

        # Crear la interfaz gráfica del selector de baudrate
        self.baudrate_label = tk.Label(root, text="Baudrate:")
        self.baudrate_label.grid(row=1, column=0, padx=10, pady=5, sticky='w')
        self.baudrate_combobox = ttk.Combobox(root, values=["9600", "19200", "38400", "57600", "115200"])
        self.baudrate_combobox.grid(row=1, column=1, padx=10, pady=5, sticky='ew')
        self.baudrate_combobox.set("9600")  # Establecer el baudrate inicial

        # Botón para buscar puertos
        self.scan_button = tk.Button(root, text="Buscar Puertos", command=self.scan_ports)
        self.scan_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky='ew')

        # Botón para conectar
        self.connect_button = tk.Button(root, text="Conectar", command=self.connect)
        self.connect_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky='ew')

        # Botón para seleccionar archivo
        self.Seleccionar_Archivo = tk.Button(root, text="Seleccionar Archivo", command=self.open_file)
        self.Seleccionar_Archivo.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky='ew')

        # Botón para iniciar la prueba
        self.button_Init_Test = tk.Button(root, text="Iniciar Prueba", command=self.init_test)
        self.button_Init_Test.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky='ew')

        # Función para actualizar baudrate cuando se seleccione uno nuevo
        self.baudrate_combobox.bind("<<ComboboxSelected>>", self.update_baudrate)

        self.center_window()
        self.make_responsive()
        
        self.no_response_count = 0  # Contador de respuestas no recibidas
        self.timeout = 2  # Tiempo de espera para la respuesta en segundos (puedes ajustar este valor)

    # Función para centrar la ventana en la pantalla
    def center_window(self):
        # Centrar la ventana en la pantalla
        window_width = self.root.winfo_reqwidth()
        window_height = self.root.winfo_reqheight()
        position_right = int(self.root.winfo_screenwidth() / 2 - window_width / 2)
        position_down = int(self.root.winfo_screenheight() / 2 - window_height / 2)
        self.root.geometry(f'+{position_right}+{position_down}')

    # Función para hacer la interfaz responsiva
    def make_responsive(self):
        for i in range(6):
            self.root.grid_rowconfigure(i, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=2)

    # Función para buscar puertos disponibles
    def scan_ports(self):
        self.tty_ports = []

        # Verificar el sistema operativo
        if sys.platform.startswith('win'):
            # Windows
            ports = list_ports.comports()
            self.tty_ports = [port.device for port in ports]
        elif sys.platform.startswith('linux') or sys.platform.startswith('darwin'):
            # Linux o macOS
            self.tty_ports = glob.glob('/dev/ttyUSB*') + glob.glob('/dev/ttyACM*')
        else:
            print("Sistema operativo no soportado")
            return

        # Imprimir la lista de dispositivos encontrados (solo para propósitos de prueba)
        if len(self.tty_ports) == 0:
            print("No hay puertos disponibles")
        else:
            print("Puertos disponibles:")
            for i, port in enumerate(self.tty_ports):
                print(f"[{i}] {port}")

        # Actualizar los valores del Combobox con los puertos encontrados
        self.port_combobox['values'] = self.tty_ports

    # Función para conectar al puerto seleccionado
    def connect(self):
        port = self.port_combobox.get()
        baudrate = int(self.baudrate_combobox.get())
        self.serial_client = SerialClient(port, baudrate)
        try:
            self.serial_client.connect()
            messagebox.showinfo("Conexión", "Conectado exitosamente")
        except Exception as e:
            messagebox.showerror("Error de Conexión", str(e))

    # Función para actualizar el baudrate
    def update_baudrate(self, event):
        if self.serial_client:
            baudrate = float(self.baudrate_combobox.get())
            TimeOutStatus = self.serial_client.Set_TimeOut(baudrate)
            self.serial_client.set_baudrate(baudrate)
            print(TimeOutStatus)
        else:
            print("Error: No se ha establecido una conexión serial")

    # Función para iniciar la prueba
    def init_test(self):
        #self.timeout = self.serial_client.Set_TimeOut(float(self.baudrate_combobox.get()))
        self.timeout = 2
        statusflag = False
        if self.File_path:
            print("Iniciando Prueba")
            self.reader.set_file_path(self.File_path)
            data = self.reader.read_json()

            for i in range(len(data)):
                self.response = self.serial_client.send_data(bytearray(data[i]))
                time.sleep(0.1)

                # Esperar una respuesta del dispositivo
                if self.response == "Error: La conexión serial no está abierta":
                    statusflag = True
                    return False
                if not self.wait_for_response():
                    self.no_response_count += 1
                    print(f"Prueba {i + 1}: No hubo respuesta")
                else:
                    print(f"Prueba {i + 1}: Respuesta recibida")
                    self.ResponseDecoderModbus = self.ModbusDecoder.decode(self.response)
                    print(f"Respuesta decodificada: {self.ResponseDecoderModbus}")
                print("--------------------------------------------------")
                time.sleep(1)

            
        if statusflag == False:
            messagebox.showinfo("Prueba finalizada", f"Total de pruebas sin respuesta: {self.no_response_count}")
        if statusflag:
            messagebox.showerror("Error", "Error al enviar datos al dispositivo")
        else:
            messagebox.showwarning("Advertencia", "Por favor, selecciona un archivo antes de iniciar la prueba.")
        self.no_response_count = 0
        

    # Función para esperar la respuesta del dispositivo
    def wait_for_response(self):
        """
        Espera una respuesta del dispositivo dentro del tiempo de espera (timeout).
        Devuelve True si se recibe una respuesta, False si no.
        """
        start_time = time.time()
        
        while (time.time() - start_time) < self.timeout:
            self.response = self.serial_client.read_data()  # Método que lee la respuesta del dispositivo
            
            if self.response:
                print(f"Respuesta: {self.response}")
                if(self.response == "[Errno 5] Input/output error"):
                    break
                
                return True
            time.sleep(0.1)  # Pausa pequeña para evitar sobrecargar la CPU
        
        # No se recibió respuesta en el tiempo límite
        return False

    # Función para abrir un archivo
    def open_file(self):
        self.File_path = filedialog.askopenfilename()
        print(self.File_path)  # Imprime la ruta del archivo seleccionado

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()