def hex_to_array(hex_value):
    # Convertimos el valor hexadecimal a una cadena sin el prefijo '0x'
    hex_str = f"{hex_value:04x}"

    # Dividimos la cadena en partes de dos caracteres
    hex_array = [hex_str[i:i + 2] for i in range(0, len(hex_str), 2)]

    # Convertimos cada parte a un valor hexadecimal
    result = [int(x, 16) for x in hex_array]

    return result


def hex_string_to_array(hex_string):
    # Quitamos el prefijo '0x' si está presente
    hex_value = hex_string.replace("0x", "")

    # Aseguramos que el valor tenga una longitud múltiplo de dos
    if len(hex_value) % 2 != 0:
        hex_value = "0" + hex_value

    # Dividimos la cadena en partes de dos caracteres
    hex_array = [hex_value[i:i + 2] for i in range(0, len(hex_value), 2)]

    # Convertimos cada parte a un valor hexadecimal
    result = []

    # Ejemplo de uso
    # hex_value = 0x0001
    # result = hex_to_array(hex_value)
    # print(result)  # Output: [0, 1]
    for x in hex_array:
        try:
            result.append(int(x, 16))
        except ValueError:
            # Si hay un error al convertir, manejarlo según sea necesario
            print(f"Error: '{x}' no es un valor hexadecimal válido.")
            # Aquí puedes decidir cómo manejar el error, por ejemplo, ignorarlo o lanzar una excepción

    return result
# Ejemplo de uso
# hex_string = "0x0000"
# result = hex_string_to_array(hex_string)
# print([hex(val) for val in result])  # Output: ['0x0', '0x0']

def hexadecimal_string_to_int(hex_string):
    if hex_string.startswith("0x"):
        hex_string = hex_string[2:]

    try:
        if hex_string.lower() == "n/a":
            raise ValueError("Valor no disponible (N/A)")
        return int(hex_string, 16)
    except ValueError:
        raise ValueError(f"No es un valor hexadecimal válido: '{hex_string}'")

# Ejemplo de uso
# hex_value = "0xC4"
# integer_value = hexadecimal_string_to_int(hex_value)
# print(f"Valor hexadecimal '{hex_value}' convertido a entero: {integer_value}")




