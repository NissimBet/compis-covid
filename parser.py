# ------------------------------------------------------------
# parser.py
# Alejandro Longoria y Nissim Betesh
#
# yacc example for simple Covid19 Language
# using PLY (a lex/yacc implementation for Python)
# code samples from: https://ply.readthedocs.io/en/latest/ply.html
# ------------------------------------------------------------

import logging
import ply.yacc as yacc

# Get the token map from the lexer.  This is required.
from lexer import tokens, literals


# program id ; VARS? function* main
def p_programa(p):
    '''programa     : PROGRAM ID ';' programa_1 main'''
    p[0] = "COMPILA"
    pass


def p_programa_1(p):
    '''programa_1   : vars programa_2
                    | programa_2 '''
    pass


def p_programa_2(p):
    '''programa_2   : function programa_2 
                    | epsilon'''
    pass


# var (tipo : lista_id ;)+
def p_vars(p):
    '''vars         : VAR vars_1 '''
    pass


def p_vars_1(p):
    '''vars_1       : tipo ':' lista_id ';' vars_2 '''
    pass


def p_vars_2(p):
    '''vars_2       : vars_1 
                    | epsilon '''
    pass


# lista_id : (id ,)+
def p_lista_id(p):
    '''lista_id     : id_completo lista_id_1'''


def p_lista_id_1(p):
    '''lista_id_1   : ',' lista_id_1 
                    | epsilon'''
    pass


# id dimension?
def p_id_completo(p):
    '''id_completo      : ID id_completo_1'''
    pass


def p_id_completo_1(p):
    '''id_completo_1    : dimension 
                        | epsilon'''
    pass


# TODO debe ser num_var entera
# [ num_var ] {0, 2}
def p_dimension(p):
    '''dimension    : '[' num_var ']' 
                    | dimension_1 '''
    pass


def p_dimension_1(p):
    '''dimension_1  : '[' num_var ']' 
                    | epsilon '''
    pass


def p_tipo(p):
    '''tipo : INT 
            | FLOAT
            | STRING
            | CHAR
            | DATAFRAME'''
    pass


# TODO definir bloque
# function tipo_retorno ID ( parameters? ) vars? { bloque? }
def p_function(p):
    '''function     : FUNCTION tipo_retorno ID  '(' function_1 ')' function_2 '{' bloque '}' '''
    pass


def p_function_1(p):
    '''function_1   : parameters 
                    | epsilon '''
    pass


def p_function_2(p):
    '''function_2   : vars 
                    | epsilon '''
    pass


def p_tipo_retorno(p):
    '''tipo_retorno : tipo 
                    | VOID '''
    pass


# expression ( ',' expression )*
def p_parameters(p):
    '''parameters       : expression parameters_1 '''
    pass


def p_parameters_1(p):
    '''parameters_1     : ',' expression 
                        | epsilon'''
    pass


def p_statement(p):
    '''statement    : assignment 
                    | func_call 
                    | return 
                    | read 
                    | write 
                    | load 
                    | condition 
                    | loop '''
    pass


# ID_COMPLETO '=' EXPRESsION ';'
def p_assignment(p):
    '''assignment   : id_completo '=' expression ';' '''
    pass


# ID ( EXPRESION* ) ;
def p_void_func_call(p):
    '''void_func_call    : ID '(' void_func_call_1 ')' ';' '''
    pass


def p_void_func_call_1(p):
    '''void_func_call_1  : expression void_func_call_1 
                        | epsilon '''
    pass


# return ( EXP ) ;
def p_return(p):
    '''return   : RETURN '(' exp ')' '''
    pass


# read ( LISTA_ID ) ;
def p_read(p):
    '''read     : READ '(' lista_id ')' ';' '''
    pass


# write '(' ( EXPRESION | string_var )+ ')' ;
def p_write(p):
    '''write    :  WRITE '(' write_1 write_2 ')' ';' '''
    pass


def p_write_1(p):
    '''write_1  : expression 
                | string_var '''
    pass


def p_write_2(p):
    '''write_2  : ',' write_1 write_2 
                | epsilon '''
    pass


# CargaArchivo ( id , ruta_acceso , num_var , num_var ) ;
def p_load(p):
    '''load     : LOAD '(' ID ',' string_var ',' string_var ',' num_var ')' ';' '''
    pass


def p_main(p):
    '''main     : MAIN '(' ')' main_1 '{' bloque '}'  '''
    pass


def p_main_1(p):
    '''main_1   : vars
                | epsilon '''
    pass


# TODO Revisar que los if-statements, cierren correctamente. Revisar clase de ceballos al inicio del semestre
# TODO Hacer else if
# if ( EXPRESION ) then { bloque? } ( else { bloque? } )?
def p_condition(p):
    '''condition    : IF '(' expression ')' '{' condition_1 '}' condition_2 '''
    pass


def p_condition_1(p):
    '''condition_1  : bloque 
                    | epsilon '''
    pass


def p_condition_2(p):
    '''condition_2  : ELSE '{' condition_1 '}'
                    | epsilon'''
    pass


def p_loop(p):
    '''loop     : conditional_loop 
                | no_condition_loop '''
    pass


# while ( EXPRESION ) do { bloque? }
def p_conditional_loop(p):
    '''conditional_loop     : WHILE '(' expression ')' DO '{' conditional_loop_1 '}' '''
    pass


def p_conditional_loop_1(p):
    '''conditional_loop_1   : bloque 
                            | epsilon '''
    pass


# desde ID_COMPLETO = EXP to EXP hacer { ESTATUTO* }
def p_no_condition_loop(p):
    '''no_condition_loop    : FROM id_completo '=' exp TO exp DO '{' no_condition_loop_1 '}'  '''
    pass


def p_no_condition_loop_1(p):
    '''no_condition_loop_1  : bloque 
                            | epsilon '''
    pass


def p_num_var(p):
    ''' num_var     : ID 
                    | CTE_I 
                    | CTE_F '''
    pass


def p_string_var(p):
    ''' string_var  : ID 
                    | CTE_STRING '''
    pass


def p_var_cte(p):
    '''var_cte      : ID 
                    | CTE_I 
                    | CTE_F 
                    | CTE_STRING 
                    | CTE_CHAR '''


# ( EXP | LLAMADA ) ( ( '>' | '<' | '==' | '<>' ) ( EXP | LLAMADA ) )?
def p_expression(p):
    ''' expression      : expression_1 expression_2 '''
    pass


def p_expression_1(p):
    '''expression_1     : exp 
                        | func_call '''
    pass


def p_expression_2(p):
    '''expression_2     : comparison_ops expression_1 
                        | epsilon'''
    pass


def p_comparison_ops(p):
    '''comparison_ops   : '<' 
                        | '>' 
                        | DIFF 
                        | EQUAL '''
    pass


# id (  ( TIPO id , )* )
def p_func_call(p):
    '''func_call    : ID '(' func_call_1 ')' '''
    pass


def p_func_call_1(p):
    '''func_call_1  : tipo ID func_call_2 
                    | epsilon '''
    pass


def p_func_call_2(p):
    '''func_call_2  : ',' tipo ID func_call_2 
                    | epsilon '''
    pass


# TERMINO ( ( '+' | '-' ) TERMINO )*
def p_exp(p):
    '''exp      : termino exp_1 '''
    pass


def p_exp1(p):
    '''exp_1    : exp_2 termino exp_1
                | epsilon'''
    pass


def p_exp_2(p):
    '''exp_2    : '+' 
                | '-' '''
    pass


# FACTOR ( ( '*' | '/' ) FACTOR )*
def p_termino(p):
    '''termino      : factor termino_1 '''
    pass


def p_termino_1(p):
    '''termino_1    : termino_2 factor termino_1 
                    | epsilon '''
    pass


def p_termino_2(p):
    '''termino_2    : '*' 
                    | '/' '''
    pass


def p_factor(p):
    '''factor       : '(' expression ')'
                    | factor_1 var_cte '''
    pass


def p_factor_1(p):
    '''factor_1     : '+' 
                    | '-' 
                    | epsilon '''
    pass


def p_bloque(p):
    '''bloque   : statement bloque_1'''
    pass


def p_bloque_1(p):
    '''bloque_1     : statement bloque_1 
                    | epsilon '''
    pass


def p_epsilon(p):
    '''epsilon :'''
    pass


# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")
    print(p)
    pass


# Build the parser
parser = yacc.yacc(start="programa")

data = '''
program donpato;
var float:numero;
main() {
    numeroPi = 3.1;
	if (numeroPi < hi) {
		numeroPi = 3.14159;
	}
    else
    {
		print("Coronavirus will destroy math");
	}
}
'''


logging.basicConfig(
    level=logging.DEBUG,
    filemode="w",
    filename="parselog.txt")

if (parser.parse(data, tracking=True, debug=logging.getLogger()) == 'COMPILA'):
    print("Sintaxis aceptada")
else:
    print("error de sintaxis")
