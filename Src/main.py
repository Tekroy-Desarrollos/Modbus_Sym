import tkinter as tk
from tkinter import ttk, messagebox
from Serial_Client import SerialClient

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Modbus Client")

        # Aplicar un tema moderno
        ttk.Style().theme_use('clam')

        self.serial_client = None

        self.port_label = ttk.Label(root, text="Puerto:")
        self.port_label.grid(row=0, column=0, padx=10, pady=5, sticky='w')

        self.port_combobox = ttk.Combobox(root)
        self.port_combobox.grid(row=0, column=1, padx=10, pady=5, sticky='ew')

        self.baudrate_label = ttk.Label(root, text="Baudrate:")
        self.baudrate_label.grid(row=1, column=0, padx=10, pady=5, sticky='w')

        self.baudrate_combobox = ttk.Combobox(root, values=["9600", "19200", "38400", "57600", "115200"])
        self.baudrate_combobox.grid(row=1, column=1, padx=10, pady=5, sticky='ew')
        self.baudrate_combobox.current(0)  # Establecer el baudrate inicial

        self.connect_button = ttk.Button(root, text="Conectar", command=self.connect)
        self.connect_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky='ew')

        self.address_label = ttk.Label(root, text="Dirección:")
        self.address_label.grid(row=3, column=0, padx=10, pady=5, sticky='w')

        self.address_entry = ttk.Entry(root)
        self.address_entry.grid(row=3, column=1, padx=10, pady=5, sticky='ew')

        self.count_label = ttk.Label(root, text="Cantidad:")
        self.count_label.grid(row=4, column=0, padx=10, pady=5, sticky='w')

        self.count_entry = ttk.Entry(root)
        self.count_entry.grid(row=4, column=1, padx=10, pady=5, sticky='ew')

        self.read_button = ttk.Button(root, text="Leer Registro", command=self.read_register)
        self.read_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky='ew')

        # Botón para buscar puertos
        self.scan_button = ttk.Button(root, text="Buscar Puertos", command=self.scan_ports)
        self.scan_button.grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky='ew')

        # Función para actualizar baudrate cuando se seleccione uno nuevo
        self.baudrate_combobox.bind("<<ComboboxSelected>>", self.update_baudrate)

        # Centrar la ventana en la pantalla
        self.center_window()

    def center_window(self):
        # Centrar la ventana en la pantalla
        window_width = self.root.winfo_reqwidth()
        window_height = self.root.winfo_reqheight()
        position_right = int(self.root.winfo_screenwidth() / 2 - window_width / 2)
        position_down = int(self.root.winfo_screenheight() / 2 - window_height / 2)
        self.root.geometry(f'+{position_right}+{position_down}')

    def scan_ports(self):
        ports = SerialClient.list_ports()
        self.port_combobox['values'] = ports
        if ports:
            self.port_combobox.current(0)

    def connect(self):
        port = self.port_combobox.get()
        baudrate = int(self.baudrate_combobox.get())
        self.serial_client = SerialClient(port, baudrate)
        try:
            self.serial_client.connect()
            messagebox.showinfo("Conexión", "Conectado exitosamente")
        except Exception as e:
            messagebox.showerror("Error de Conexión", str(e))

    def read_register(self):
        if not self.serial_client:
            messagebox.showerror("Error", "No hay conexión Modbus")
            return

        address = int(self.address_entry.get())
        count = int(self.count_entry.get())
        try:
            response = self.serial_client.read_register(address, count)
            data = ' '.join(format(x, '02x') for x in response)
            messagebox.showinfo("Respuesta", f"Datos: {data}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update_baudrate(self, event):
        if self.serial_client:
            baudrate = int(self.baudrate_combobox.get())
            self.serial_client.set_baudrate(baudrate)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
