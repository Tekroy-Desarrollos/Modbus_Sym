import customtkinter as ctk
from tkinter import messagebox, filedialog  # Importar messagebox y filedialog desde tkinter
from Serial_Client import SerialClient  # Asegúrate de tener SerialClient definido correctamente
from Reader_Json import ReaderJson
import serial.tools.list_ports as list_ports
import sys
import glob
import time

# Crear una instancia de SerialClient
client = SerialClient(port='/dev/ttyUSB0', baudrate=9600)

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Modbus Client")

        # Configurar el tema de CustomTkinter
        ctk.set_appearance_mode("light")  # Modo oscuro o claro basado en el sistema
        ctk.set_default_color_theme("blue")  # Tema de color predeterminado

        # Inicializar el lector de JSON con la ruta del archivo aún no especificada
        self.reader = ReaderJson()

        # Variables de uso general
        self.serial_client = None
        self.File_path = None

        # Crear la interfaz gráfica del selector de puerto
        self.port_label = ctk.CTkLabel(root, text="Puerto:")
        self.port_label.grid(row=0, column=0, padx=10, pady=5, sticky='w')
        self.port_combobox = ctk.CTkComboBox(root)
        self.port_combobox.grid(row=0, column=1, padx=10, pady=5, sticky='ew')

        # Crear la interfaz gráfica del selector de baudrate
        self.baudrate_label = ctk.CTkLabel(root, text="Baudrate:")
        self.baudrate_label.grid(row=1, column=0, padx=10, pady=5, sticky='w')
        self.baudrate_combobox = ctk.CTkComboBox(root, values=["9600", "19200", "38400", "57600", "115200"])
        self.baudrate_combobox.grid(row=1, column=1, padx=10, pady=5, sticky='ew')
        self.baudrate_combobox.set("9600")  # Establecer el baudrate inicial

        # Botón para buscar puertos
        self.scan_button = ctk.CTkButton(root, text="Buscar Puertos", command=self.scan_ports)
        self.scan_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky='ew')

        # Botón para conectar
        self.connect_button = ctk.CTkButton(root, text="Conectar", command=self.connect)
        self.connect_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky='ew')

        # Botón para seleccionar archivo
        self.Seleccionar_Archivo = ctk.CTkButton(root, text="Seleccionar Archivo", command=self.open_file)
        self.Seleccionar_Archivo.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky='ew')

        # Botón para iniciar la prueba
        self.button_Init_Test = ctk.CTkButton(root, text="Iniciar Prueba", command=self.init_test)
        self.button_Init_Test.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky='ew')

        # Función para actualizar baudrate cuando se seleccione uno nuevo
        self.baudrate_combobox.bind("<<ComboboxSelected>>", self.update_baudrate)

        self.center_window()
        self.make_responsive()

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
        self.port_combobox.configure(values=self.tty_ports)

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
        if self.File_path:
            # Aquí puedes llamar a la función que inicia tu prueba
            # Por ejemplo, si tienes una función llamada "run_test" en Serial_Client.py
            # solo debes hacer:
            print("Iniciando Prueba")

            self.reader.set_file_path(self.File_path)
            data = self.reader.read_json()
            for i in range(20):
                self.serial_client.send_data(bytearray(data[i]))
                
                time.sleep(0.1)
        else:
            messagebox.showwarning("Advertencia", "Por favor, selecciona un archivo antes de iniciar la prueba.")

    # Función para abrir un archivo
    def open_file(self):
        self.File_path = filedialog.askopenfilename()
        print(self.File_path)  # Imprime la ruta del archivo seleccionado

if __name__ == "__main__":
    root = ctk.CTk()
    app = App(root)
    root.mainloop()
