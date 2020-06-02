# ------------------------------------------------------------
# lexer.py
# Alejandro Longoria y Nissim Betesh
#
# lex example for simple Covid19 Language
# using PLY (a lex/yacc implementation for Python)
# code samples from: https://ply.readthedocs.io/en/latest/ply.html
# ------------------------------------------------------------
import re

import ply.lex as lex

from .AVAIL import avail

# Rule to match reserved words and identifiers
reserved = {
    'program'      : 'PROGRAM',
    'function'     : 'FUNCTION',

    'if'           : 'IF',
    'then'         : 'THEN',
    'else'         : 'ELSE',

    'var'          : 'VAR',
    'return'       : 'RETURN',

    'main'         : 'MAIN',

    'read'         : 'READ',
    'write'        : 'WRITE',
    'load'         : 'LOAD',

    # loops
    'while'        : 'WHILE',
    'do'           : 'DO',
    'from'         : 'FROM',
    'to'           : 'TO',

    # data types
    'int'          : 'INT',
    'float'        : 'FLOAT',
    'string'       : 'STRING',
    'char'         : 'CHAR',
    'void'         : 'VOID',
    'dataFrame'    : 'DATAFRAME',
    'bool'         : "BOOL",

    'true'         : "TRUE",
    'false'        : "FALSE",

    # Métodos Estadísticos
    'getMean'      : 'MEAN',
    'getMode'      : 'MODE',
    'variance'     : 'VARIANCE',
    'getNormal'    : 'NORMAL',
    'getGamma'     : 'GAMMA',
    # Graficar variables simples
    'graphBar'     : 'GRAPH',
    'normalGraph'  : 'NORMAL_GRAPH',
    # Correlación entre dos variables
    'getCovariance': 'COV',
    # Correlación gráfica entre dos variables
    'scatter'      : 'SCATTER'
}

# List of token names.   This is always required
tokens = [
             'EQUAL',
             'DIFF',
             'CTE_F',
             'CTE_I',
             'CTE_STRING',
             'CTE_CHAR',
             'OR',
             'AND',
             'ID',
         ] + list(reserved.values())

literals = '+-*/=<>(){}:;,[]'

# Regular expression rules for simple tokens
t_DIFF = r'<>'
t_EQUAL = r'=='
t_OR = r'\|\|'
t_AND = r'\&\&'

def t_FALSE(t):
    r'false'
    t.type = "FALSE"
    const_dir = avail.get_next_const("bool", "false")
    t.value = const_dir
    return t

def t_TRUE(t):
    r'true'
    t.type = "TRUE"
    const_dir = avail.get_next_const("bool", "true")
    t.value = const_dir
    return t

# Expression rule to detect and convert floating point numbers
def t_CTE_F(t):
    r'(\d+[.])\d+'
    const_dir = avail.get_next_const("float", str(t.value))
    t.value = const_dir
    return t

def t_DATAFRAME(t):
    r'dataframe'
    const_dir = avail.get_next_const("dataframe", t.value)
    t.value = const_dir
    return t

# A regular expression rule with some action code
def t_CTE_I(t):
    r'\d+'
    const_dir = avail.get_next_const("int", str(t.value))
    t.value = const_dir
    return t

def t_CTE_STRING(t):
    r'\"[^"]*\"'
    regex = re.search(r'\"([^"]*)\"', t.value)
    const_dir = avail.get_next_const("string", regex.group(1))
    t.value = const_dir
    return t

def t_CTE_CHAR(t):
    r'\'.\''
    const_dir = avail.get_next_const("char", t.value)
    t.value = const_dir
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

data = '''
program donpato;
var float:numero[0][0], mat[1], wat, dude;
    int: data, custom, suma;
    char: a;
    string: hi;
    
function void hello() 
    var string: hello, world;
    {
        return (hello + world);
    }
function void there() 
    var string: hello, world;
    {
        return (hello + world);
    }
    
main() {
    numeroPi = 3.1;
	if (numeroPi && 5 < hi) then {
		numeroPi = 3.14159;
	}
    else
    {
		print("Coronavirus will destroy math");
	}
    if (3 > 2) then {
        numero = 5.5;
    }
    scatter(numero)
}
'''
# # Give the lexer some input
# lex.input(data)

# # Tokenize
# while True:
#     tok = lex.token()
#     if not tok:
#         break      # No more input
#     print(tok)
