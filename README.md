# Simulador de Dispositivo ModBus RTU Master

Este proyecto es un simulador de dispositivo ModBus RTU Master desarrollado en Python. Utiliza una interfaz gráfica construida con `tkinter` para gestionar la comunicación serial y realizar pruebas con datos proporcionados en archivos JSON.

## Estructura del Proyecto

- `main.py`: Archivo principal que contiene la interfaz gráfica y la lógica principal del programa.
- `Serial_Client.py`: Módulo que maneja la comunicación serial.
- `Reader_Json.py`: Módulo que lee y procesa archivos JSON.
- `Data_Transformer.py`: Módulo con funciones para convertir valores hexadecimales a arreglos y enteros.

## Requisitos

- Python 3.x
- tkinter
- pyserial

## Instalación

1. Clona el repositorio:
    ```bash
    git clone https://github.com/tu-usuario/tu-repositorio.git
    cd tu-repositorio
    ```

2. Instala las dependencias:
    ```bash
    pip install pyserial
    ```

## Uso

1. Ejecuta el archivo principal:
    ```bash
    python main.py
    ```

2. En la interfaz gráfica:
    - Selecciona el puerto serial y el baudrate.
    - Haz clic en "Buscar Puertos" para listar los puertos disponibles.
    - Selecciona un puerto de la lista y haz clic en "Conectar".
    - Selecciona un archivo JSON haciendo clic en "Seleccionar Archivo".
    - Inicia la prueba haciendo clic en "Iniciar Prueba".

## Ejemplos de Archivos JSON

```json
{
    "Pruebas": [
        {
            "Slave_Address": "0x01",
            "Function_code": "0x03",
            "Starting_address": "0x006B",
            "Quantity": "0x0003",
            "CRC_MSB": "0x76",
            "CRC_LSB": "0x87",
            "Number_Test": 1
        }
    ]
}

