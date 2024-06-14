import json
import os

class ReaderJson:
    def __init__(self, file_path=None):
        self.file_path = file_path
        self.data = None

    def read_json(self):
        if not self.file_path:
            raise ValueError("File path is not set.")

        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"File '{self.file_path}' not found.")

        with open(self.file_path, 'r') as file:
            self.data = json.load(file)
            pruebas = self.data.get("Pruebas", [])

            for prueba in pruebas:
                # Resto del código para procesar el JSON
                tipo_de_trama = prueba.get("TipoDeTrama")
                registro_de_inicio = prueba.get("RegistroDeInicio")
                nuevo_valor_del_registro = prueba.get("NuevoValorDelRegistro")
                respuesta_esperada = prueba.get("RespuestaEsperada")
                numero_de_prueba = prueba.get("NumeroDePrueba")

                # Imprimir los valores para verificar
                print(f"Prueba {numero_de_prueba}:")
                print("  Tipo de Trama:", tipo_de_trama)
                print("  Registro de Inicio:", registro_de_inicio)
                print("  Nuevo Valor del Registro:", nuevo_valor_del_registro)
                print("  Respuesta Esperada:", respuesta_esperada)
                print()

    def set_file_path(self, file_path):
        self.file_path = file_path
        print(f"File path set to: {self.file_path}")
