import ply.yacc as yacc
import ply.lex as lex

# palabras reservadas
# { "escritura": "representacion" }
reserved = {
    "program": "PROGRAM",
    "var": "VAR",
    "int": "INT",
    "float": "FLOAT",
}

# todos los tokens del sintaxis
tokens = [
    "NUMBER", "ID",
    "STRING"
] + list(reserved.values())

# literales
literals = [
    '+', '-', '*', '\\',
    '}', '{', ';', ',',
    ':', '(', ')', '=',
    '<', '>'
]

# definiciones de tokens
t_NUMBER = r'[0-9]+'
t_STRING = r'"[a-zA-Z0-9\\s]"'


def t_ID(t):
    r'[a-zA-Z][a-zA-Z0-9]*'
    # identificadores inician con letras seguidos por caracteres
    if t.value in reserved.keys():
        t.return_type = reserved.get(t.value, 'ID')
    return t

# gramatica
# p_regla(p):


def p_empty(p):
    'empty :'
    pass


def p_programa(p):
    '''
    '''
    pass


if __name__ == "__main__":
    import sys

    # crear instancia del analizador lexico
    lexer = lex.lex()
    # crear instancia de parser
    parser = yacc.yacc(start="programa")

    # if len(sys.argv) != 2:
    # raise ValueError("Favor de ingresar el nombre del archivo a parsear")

    # filename = sys.argv[1]

    filename = input("Ingrese el nombre del archivo")

    file = open(filename)
    fileLines = "".join(file.readlines())

    try:
        print("Iniciando parseo")
        yacc.parse(fileLines)
        print("parseo exitoso")
    except Exception:
        print("Error al parsear %s" % filename)
