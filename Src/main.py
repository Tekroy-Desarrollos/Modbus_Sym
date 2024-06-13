import tkinter as tk
from tkinter import messagebox, ttk
from Serial_Client import SerialClient

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Modbus Client")

        self.serial_client = None

        self.port_label = tk.Label(root, text="Puerto:")
        self.port_label.grid(row=0, column=0)
        self.port_combobox = ttk.Combobox(root)
        self.port_combobox.grid(row=0, column=1)

        self.baudrate_label = tk.Label(root, text="Baudrate:")
        self.baudrate_label.grid(row=1, column=0)
        self.baudrate_entry = tk.Entry(root)
        self.baudrate_entry.grid(row=1, column=1)

        self.connect_button = tk.Button(root, text="Conectar", command=self.connect)
        self.connect_button.grid(row=2, column=0, columnspan=2)

        self.address_label = tk.Label(root, text="Dirección:")
        self.address_label.grid(row=3, column=0)
        self.address_entry = tk.Entry(root)
        self.address_entry.grid(row=3, column=1)

        self.count_label = tk.Label(root, text="Cantidad:")
        self.count_label.grid(row=4, column=0)
        self.count_entry = tk.Entry(root)
        self.count_entry.grid(row=4, column=1)

        self.read_button = tk.Button(root, text="Leer Registro", command=self.read_register)
        self.read_button.grid(row=5, column=0, columnspan=2)
        
        

    def connect(self):
        port = self.port_entry.get()
        baudrate = int(self.baudrate_entry.get())
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
    
    def scan_ports(self):
        ports = SerialClient.list_ports()
        self.port_combobox['values'] = ports
        if ports:
            self.port_combobox.current(0)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
