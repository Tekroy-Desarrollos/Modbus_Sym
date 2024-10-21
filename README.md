# Simulador de Dispositivo ModBus RTU Master

Este proyecto es un simulador de dispositivo ModBus RTU Master desarrollado en Python. Utiliza una interfaz gráfica construida con `tkinter` para gestionar la comunicación serial y realizar pruebas con datos proporcionados en archivos JSON.

## Estructura del Proyecto

- `main.py`: Archivo principal que contiene la interfaz gráfica y la lógica principal del programa.
- `Serial_Client.py`: Módulo que maneja la comunicación serial.
- `Reader_Json.py`: Módulo que lee y procesa archivos JSON.
- `Data_Transformer.py`: Módulo con funciones para convertir valores hexadecimales a arreglos y enteros.

## Requisitos

- Python 3.x
- Tkinter
- pyserial

## Instalación

1. Clona el repositorio:
    ```bash
    git clone git@github.com:Tekroy-Desarrollos/Modbus_Sym.git

    cd Modbus_Sym
    ```

2. Instala las dependencias en Ubuntu:

    
    ```bash
    pip install pyserial
    ```
    
    ```bash
    sudo apt install python3-tk
    ```

## Uso en Ubuntu/Pop_Os!
1. Ingrese a la carpeta principal llamada Src

2. Ejecuta el archivo principal con la siguiente linea:

    ```bash
    python3 main.py
    ```

3. En la interfaz gráfica:
    - Presione el boton "Buscar Puertos".
    - Selecciona el puerto serial y el baudrate del dispositivo esclavo.
    - Presione el boton "Conectar" para establecer la comunicacion Serial con el dispositivo.
    - Selecciona un archivo JSON haciendo clic en "Seleccionar Archivo"E.
    - Inicia la prueba haciendo clic en "Iniciar Prueba".

## Uso de archivo de prueba

Dentro de la carpeta pruebas podra ver que existe una carpeta llamada prubeas,
en esa carpeta se encuentra un archivo Json, la estructura de ese archivo es 
similar al ejemplo que se encuentra mas abajo.

para poder realizar cualquier prueba uno debe configurar un archivo Json con la extructura:

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
```
para entender que significa cada elemento se deja la siguiente columna:

| Items            | Descripcion |
|------------------|-----------|
| Slave_Address    | Id del dispositivo esclavo    |
| Function_Code    | Codigo de funcion Modbus      |
| Starting_Address | valor del registro a modificar   |
| Quantity         | Registro a ser modificado     |
| CRC_MSB          | par de bit mas significativos del CRC   |
| CRC_LSB          | Par de bit menos significativos del CRC |
| NUmber_Test      | Numero de prueba actual a realizarse    |


Un ejemplo de configuracion puede ser el siguiente.

Suponiendo que el esclavo modbus tiene ID 1 (0x01), que el codigo de funcion
sera el 6 (0x06) (Write Single Register), el valor del registro sera 1000 (0x03E8)
el registro a modificar sera el 10 (0x000A) y el CRC es 35261 (0x89DB).

Quedaria segun la tabla anterior dividido de la siguiente forma
| Items            | Valor |
|------------------|-------|
| Slave_Address    | 0x01 |
| Function_Code    | 0x06  |
| Starting_Address | 0x03E8|
| Quantity         | 0x000A|
| CRC_MSB          | 0x89  |
| CRC_LSB          | 0xDB  |
| NUmber_Test      | 2     |

Ahora traspasando esto al formato del Json quedaria de la siguiente forma

```json
{
    "Pruebas": [
        {
            "Slave_Address": "0x01",
            "Function_code": "0x06",
            "Starting_address": "0x03E8",
            "Quantity": "0x000A",
            "CRC_MSB": "0x89",
            "CRC_LSB": "0xDB",
            "Number_Test": 1
        }
    ]
}
```


