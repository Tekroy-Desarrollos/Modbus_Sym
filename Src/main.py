from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton,
    QMessageBox, QFileDialog, QTextEdit, QGroupBox, QGridLayout
)
from modbus_client_logic import ModbusClientLogic
import sys

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.logic = ModbusClientLogic()
        self.file_path = None
        self.result_file_path = None  # Ruta del archivo de resultados
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Modbus Client")
        self.setGeometry(100, 100, 500, 400)

        # Layout principal
        main_layout = QVBoxLayout()

        # Sección de configuración de conexión
        connection_group = QGroupBox("Configuración de Conexión")
        connection_layout = QGridLayout()
        
        # Puerto
        self.port_label = QLabel("Puerto:")
        connection_layout.addWidget(self.port_label, 0, 0)
        self.port_combobox = QComboBox()
        connection_layout.addWidget(self.port_combobox, 0, 1)

        # Baudrate
        self.baudrate_label = QLabel("Baudrate:")
        connection_layout.addWidget(self.baudrate_label, 1, 0)
        self.baudrate_combobox = QComboBox()
        self.baudrate_combobox.addItems(["9600", "19200", "38400", "57600", "115200"])
        self.baudrate_combobox.setCurrentText("9600")
        connection_layout.addWidget(self.baudrate_combobox, 1, 1)

        # Botones de conexión y búsqueda de puertos
        self.scan_button = QPushButton("Buscar Puertos")
        self.scan_button.clicked.connect(self.scan_ports)
        connection_layout.addWidget(self.scan_button, 2, 0, 1, 2)

        self.connect_button = QPushButton("Conectar")
        self.connect_button.clicked.connect(self.connect)
        connection_layout.addWidget(self.connect_button, 3, 0, 1, 2)

        connection_group.setLayout(connection_layout)
        main_layout.addWidget(connection_group)

        # Sección de selección de archivo de prueba
        file_group = QGroupBox("Archivos")
        file_layout = QVBoxLayout()
        
        # Botón de selección de archivo de prueba
        self.select_file_button = QPushButton("Seleccionar Archivo de Prueba")
        self.select_file_button.clicked.connect(self.open_file)
        file_layout.addWidget(self.select_file_button)

        # Botón de selección de archivo de resultados
        self.select_result_file_button = QPushButton("Seleccionar Archivo de Resultados")
        self.select_result_file_button.clicked.connect(self.open_result_file)
        file_layout.addWidget(self.select_result_file_button)

        file_group.setLayout(file_layout)
        main_layout.addWidget(file_group)

        # Sección de resultados
        self.result_display = QTextEdit()
        self.result_display.setReadOnly(True)
        main_layout.addWidget(self.result_display)

        # Botón para iniciar prueba
        self.start_test_button = QPushButton("Iniciar Prueba")
        self.start_test_button.clicked.connect(self.init_test)
        main_layout.addWidget(self.start_test_button)

        self.setLayout(main_layout)

    def scan_ports(self):
        ports = self.logic.scan_ports()
        self.port_combobox.clear()
        self.port_combobox.addItems(ports)
        self.result_display.append("Puertos actualizados")

    def connect(self):
        port = self.port_combobox.currentText()
        baudrate = int(self.baudrate_combobox.currentText())
        success, message = self.logic.connect(port, baudrate)
        if success:
            QMessageBox.information(self, "Conexión", message)
            self.result_display.append("Conexión exitosa")
        else:
            QMessageBox.critical(self, "Error de Conexión", message)
            self.result_display.append(f"Error de conexión: {message}")

    def init_test(self):
        if self.file_path and self.result_file_path:
            success, message = self.logic.init_test(self.file_path, self.result_file_path)
            if success:
                QMessageBox.information(self, "Prueba finalizada", message)
                self.result_display.append("Prueba finalizada correctamente")
            else:
                QMessageBox.critical(self, "Error", message)
                self.result_display.append(f"Error en la prueba: {message}")
        else:
            QMessageBox.warning(self, "Advertencia", "Selecciona los archivos necesarios antes de iniciar la prueba.")
            self.result_display.append("Advertencia: Selecciona los archivos necesarios")

    def open_file(self):
        self.file_path, _ = QFileDialog.getOpenFileName(self, "Seleccionar Archivo de Prueba")
        if self.file_path:
            self.result_display.append(f"Archivo de prueba seleccionado: {self.file_path}")

    def open_result_file(self):
        self.result_file_path, _ = QFileDialog.getOpenFileName(self, "Seleccionar Archivo de Resultados")
        if self.result_file_path:
            self.result_display.append(f"Archivo de resultados seleccionado: {self.result_file_path}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec())
