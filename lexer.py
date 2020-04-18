# ------------------------------------------------------------
# lexer.py
# Alejandro Longoria y Nissim Betesh
#
# lex example for simple Covid19 Language
# using PLY (a lex/yacc implementation for Python)
# code samples from: https://ply.readthedocs.io/en/latest/ply.html
# ------------------------------------------------------------

import ply.lex as lex

# Rule to match reserved words and identifiers
reserved = {
    'program': 'PROGRAM',
    'function': 'FUNCTION',

    'if': 'IF',
    'then': 'THEN',
    'else': 'ELSE',

    'var': 'VAR',
    'return': 'RETURN',

    'main': 'MAIN',

    'read': 'READ',
    'write': 'WRITE',
    'load': 'LOAD',

    # loops
    'while': 'WHILE',
    'do': 'DO',
    'from': 'FROM',
    'to': 'TO',

    # data types
    'int': 'INT',
    'float': 'FLOAT',
    'string': 'STRING',
    'char': 'CHAR',
    'void': 'VOID',
    'dataFrame': 'DATAFRAME'
}

# List of token names.   This is always required
tokens = [
    'EQUAL',
    'DIFF',
    'CTE_F',
    'CTE_I',
    'ID',
    'CTE_STRING',
    'CTE_CHAR',
] + list(reserved.values())

literals = '+-*/=<>(){}:;,'

# Regular expression rules for simple tokens
t_DIFF = r'<>'
t_EQUAL = r'=='
t_CTE_STRING = r'\".*\"'
t_CTE_CHAR = r'\'.\''


# Expression rule to detect and convert floating point numbers
def t_CTE_F(t):
    r'(\d+[.])\d+'
    t.value = float(t.value)
    return t


# A regular expression rule with some action code
def t_CTE_I(t):
    r'\d+'
    t.value = int(t.value)
    return t


# Expression rule to match possible id names
def t_ID(t):
    r'[a-zA-Z][a-zA-Z0-9]*'
    t.type = reserved.get(t.value, 'ID')  # Check for reserved words
    return t


# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# A string containing ignored characters (spaces and tabs)
t_ignore = ' \t'


# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


lex.lex()

# EJEMPLO PARA PROBAR SEGÚN LA VARIABLE DATA

# data = '''
# program donpato;
# var numero:float;
# {
#     numeroPi = 3.1;
# 	if (numeroPi < 3.14) {
# 		numeroPi = 3.14159;
# 	}
#     else
#     {
# 		print("Coronavirus will destroy math");
# 	};
# }
# '''

# # Give the lexer some input
# lex.input(data)

# # Tokenize
# while True:
#     tok = lex.token()
#     if not tok:
#         break      # No more input
#     print(tok)
