# ------------------------------------------------------------
# parser.py
# Alejandro Longoria y Nissim Betesh
# 
# yacc example for simple Covid19 Language
# using PLY (a lex/yacc implementation for Python) 
# code samples from: https://ply.readthedocs.io/en/latest/ply.html
# ------------------------------------------------------------

import ply.yacc as yacc

# Get the token map from the lexer.  This is required.
from lexer import tokens

def p_programa(p):
    '''programa : PROGRAM ID PUNTOCOMA programaP bloque'''
    p[0] = 'COMPILA'

def p_programaP(p):
    '''programaP :  vars 
                    | epsilon '''

def p_vars(p):
    '''vars : VAR varsPP'''

def p_varsP(p):
    '''varsP : COMA ID varsP
                | epsilon '''

def p_varsPP(p):
    '''varsPP : ID varsP DOSPUNTOS tipo PUNTOCOMA varsPP
                | epsilon '''

def p_tipo(p):
    '''tipo : INT 
            | FLOAT'''

def p_bloque(p):
    '''bloque : BRACKETIZQ bloqueP BRACKETDER'''

def p_bloqueP(p):
    '''bloqueP : estatuto bloqueP
                        | epsilon'''

def p_estatuto(p):
    '''estatuto : asignacion
                | condicion
                | escritura '''
                
def p_asignacion(p):
    '''asignacion : ID IGUAL expresion PUNTOCOMA'''

def p_expresion(p):
    '''expresion : exp expresionP'''

def p_expresionP(p):
    '''expresionP : expresionPP exp
                    | epsilon '''

def p_expresionPP(p):
    '''expresionPP : MAYOR
                    | MENOR
                    | DESIGUAL'''

def p_exp(p):
    '''exp : termino expP'''

def p_expP(p):
    '''expP : expPP termino expP
            | epsilon '''

def p_expPP(p):
    '''expPP : MAS
            | MENOS '''

def p_termino(p):
    '''termino : factor terminoP'''

def p_terminoP(p):
    '''terminoP : terminoPP factor terminoP
                | epsilon'''

def p_terminoPP(p):
    '''terminoPP : MULT
                | DIV '''

def p_factor(p):
    '''factor : PARIZQ expresion PARDER 
                | factorP var_cte'''

def p_factorP(p):
    '''factorP : MAS
                | MENOS
                | epsilon '''

def p_escritura(p):
    '''escritura : PRINT PARIZQ escrituraP PARDER PUNTOCOMA'''

def p_escrituraP(p):
    '''escrituraP : expresion escrituraPP
                | CTE_STRING escrituraPP'''

def p_escrituraPP(p):
    '''escrituraPP : COMA escrituraP
                    | epsilon'''

def p_condicion(p):
    '''condicion : IF PARIZQ expresion PARDER bloque condicionP PUNTOCOMA'''

def p_condicionP(p):
    '''condicionP : ELSE bloque 
                        | epsilon'''

def p_var_cte(p):
    '''var_cte : ID 
                | CTE_I 
                | CTE_F '''

def p_epsilon(p):
    '''epsilon :'''

# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")

# Build the parser
parser = yacc.yacc()

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

# if (parser.parse(data, tracking=True) == 'COMPILA'):
#         print ("Sintaxis aceptada")