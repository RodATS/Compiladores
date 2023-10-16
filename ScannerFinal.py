import string
import re

keywords = ["str", "char", "int", "for", "in", "if"]
nom_funciones = ["crack", "mvp", "localiza", "saca", "wachea"]
simbolos = ['(', ')', '{', '}', '+', ',', '=']
comp_ops = ['igualq', 'difq', 'menorq', 'mayorq', '<=', '>=']

def saberSiKeyword(dato):
    return dato in keywords

def saberSiFunciones(dato):
    return dato in nom_funciones

def saberSiSimbolo(dato):
    return dato in simbolos

def saberSiCompOp(dato):
    return dato in comp_ops

def scan(input_code):
    tokens = []
    line_number = 1

    for line in input_code.split('\n'):
        line = line.strip()
        index = 0

        while index < len(line):
            char = line[index]

            if char in string.whitespace:
                index += 1
                continue

            if char in string.ascii_letters:
                # Identificadores y palabras clave
                token = char
                index += 1

                while index < len(line) and line[index] in string.ascii_letters + string.digits:
                    token += line[index]
                    index += 1

                if saberSiKeyword(token):
                    tokens.append(('KEYWORD', token, line_number))
                elif saberSiFunciones(token):
                    tokens.append(('FUNCTION', token, line_number))
                else:
                    tokens.append(('ID', token, line_number))

            elif char.isdigit():
                # Números enteros
                token = char
                index += 1

                while index < len(line) and line[index].isdigit():
                    token += line[index]
                    index += 1

                tokens.append(('INT', token, line_number))

            elif char == '"':
                # Cadenas
                token = char
                index += 1

                while index < len(line) and line[index] != '"':
                    token += line[index]
                    index += 1

                if index < len(line):
                    token += line[index]  # Agregar comilla de cierre
                    index += 1

                tokens.append(('STRING', token, line_number))

            elif char in simbolos:
                # Símbolos
                tokens.append(('SYMBOL', char, line_number))
                index += 1

            elif char == '<':
                # Operadores de comparación
                token = char
                index += 1

                while index < len(line) and line[index] != '>':
                    token += line[index]
                    index += 1

                if index < len(line):
                    token += line[index]  # Agregar '>'
                    index += 1

                if saberSiCompOp(token):
                    tokens.append(('COMPOP', token, line_number))
                else:
                    tokens.append(('INVALID', token, line_number))

            else:
                # Carácter no válido
                tokens.append(('INVALID', char, line_number))
                index += 1

        line_number += 1

    return tokens

# Ejemplo de uso:
input_code = """
str varString = var2
for i in range(10):
    if i < 5:
        wachea("Menor")
    else:
        wachea("Mayor o igual")
"""

tokens = scan(input_code)

for token in tokens:
    print(f"Token: {token[0]}, Valor: {token[1]}, Línea: {token[2]}")
