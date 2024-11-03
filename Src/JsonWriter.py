import json
import os

class JsonWriter:
    def __init__(self, file_path: str = None):
        self.file_path = file_path

    def set_file_path(self, file_path: str):
        """Establece la ruta del archivo JSON."""
        self.file_path = file_path
        print(f"Ruta del archivo JSON establecida en: {self.file_path}")

    def write_json(self, data: dict):
        """Escribe el diccionario proporcionado en el archivo JSON."""
        self._validate_file_path()

        # Escribe los datos en el archivo JSON
        with open(self.file_path, 'w') as file:
            json.dump(data, file, indent=4)
            print(f"Datos escritos en el archivo JSON: {self.file_path}")

    def append_results(self, results: list, total_no_response: int):
        """Agrega una lista de resultados y el total de pruebas sin respuesta al archivo JSON."""
        self._validate_file_path()

        # Verificar si el archivo existe y no está vacío
        data = {}
        if os.path.exists(self.file_path):
            if os.path.getsize(self.file_path) > 0:  # Verificar si el archivo no está vacío
                with open(self.file_path, 'r') as file:
                    try:
                        data = json.load(file)
                    except json.JSONDecodeError:
                        print("Advertencia: El archivo JSON estaba vacío o fue limpiado. Se reinicializará.")
            else:
                print("Advertencia: El archivo JSON está vacío. Se reinicializará.")
        
        # Inicializar con una estructura básica si el archivo estaba vacío o era inválido
        if not data:
            data = {"Resultados": [], "Total sin respuesta": 0}

        # Actualizar el contenido con los nuevos resultados
        data["Resultados"] = results
        data["Total sin respuesta"] = total_no_response

        # Guardar los cambios en el archivo JSON
        with open(self.file_path, 'w') as file:
            json.dump(data, file, indent=4)
            print(f"Resultados actualizados en el archivo JSON: {self.file_path}")

    def _validate_file_path(self):
        """Valida que la ruta del archivo esté definida."""
        if not self.file_path:
            raise ValueError("La ruta del archivo JSON no está definida.")
