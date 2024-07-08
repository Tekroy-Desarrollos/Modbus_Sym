def hex_to_array(hex_value):
    # Convertimos el valor hexadecimal a una cadena sin el prefijo '0x'
    hex_str = f"{hex_value:04x}"

    # Dividimos la cadena en partes de dos caracteres
    hex_array = [hex_str[i:i + 2] for i in range(0, len(hex_str), 2)]

    # Convertimos cada parte a un valor hexadecimal
    result = [int(x, 16) for x in hex_array]

    return result

# Ejemplo de uso
# hex_value = 0x0001
# result = hex_to_array(hex_value)
# print(result)  # Output: [0, 1]
