# ------------------------------------------------------------
# parser.py
# Alejandro Longoria y Nissim Betesh
#
# yacc example for simple Covid19 Language
# using PLY (a lex/yacc implementation for Python)
# code samples from: https://ply.readthedocs.io/en/latest/ply.html
# ------------------------------------------------------------

import logging
from typing import List, Any, Dict

import ply.yacc as yacc
# Get the token map from the lexer.  This is required.
from lexer import tokens, literals

from Stack import Stack
from DataUtils import FunctionTable, Variable, ParsingContext, VariableTable

function_table = FunctionTable()
variable_table = VariableTable()

global_context = ParsingContext()
global_context.set_function("global")
function_table.declare_function('global', 'void')

# program id ; VARS? function* main
def p_programa(p):
    '''programa     : PROGRAM ID ';' programa_1 main'''
    p[0] = "COMPILA"
    pass


def p_programa_1(p):
    '''programa_1   : vars programa_2
                    | programa_2 '''
    print("Programa ", p[1])
    pass


def p_programa_2(p):
    '''programa_2   : function programa_2 
                    | epsilon'''
    pass


# var (tipo : lista_id ;)+
def p_vars(p):
    '''vars         : VAR vars_1 '''
    # type = var_type_queue.get()
    # var = variable_stack.pop()
    # var = variable_stack.pop()
    # while not variable_stack.is_empty():
    #     if var is None:
    #         type = var_type_queue.get()
    #         var = variable_stack.pop()
    #         continue
    #     table.declare_variable(func_name=global_context.function,
    #                            var=Variable(type, var[0]))
    #     var = variable_stack.pop()
    pass


def p_set_var_type(p):
    '''set_var_type : '''
    global_context.set_type(p[-1])


def p_vars_1(p):
    '''vars_1       : tipo set_var_type ':' lista_id ';' vars_2 '''
    # print("vars_1", p[1], p[4], p[6])
    pass


def p_vars_2(p):
    '''vars_2       : vars_1 
                    | epsilon '''
    pass

def p_declare_var(p):
    '''declare_var  : '''
    function_table.declare_variable(global_context.function, Variable(global_context.var_type, p[-1][0], p[-1][1]))


# lista_id : (id ,)+
def p_lista_id(p):
    '''lista_id     : id_completo declare_var lista_id_1'''
    # print("lists_id ", [p[1], p[2]])
    # table.declare_variable(func_name=global_context.function,
    #                        var=Variable(global_context.var_type, p[1][0]))
    if p[2] is not None:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = [p[1]]
    pass

def p_lista_id_1(p):
    '''lista_id_1   : ',' id_completo declare_var lista_id_1
                    | epsilon'''
    if len(p) > 2:
        # table.declare_variable(func_name=global_context.function,
        #                        var=Variable(global_context.var_type, p[2][0]))
        # print("lista_id_1", p[2], p[3])
        if p[3] is not None:
            p[0] = [p[2]] + p[3]
        else:
            p[0] = [p[2]]
    pass


# id dimension?
def p_id_completo(p):
    '''id_completo      : ID id_completo_1'''
    # print("Id Completo",p[1], p[2])
    p[0] = p[1], p[2]
    pass


def p_id_completo_1(p):
    '''id_completo_1    : dimension 
                        | epsilon'''
    # print("Id_completo_1 ", p[1])
    p[0] = p[1]
    pass


# TODO debe ser num_var entera
# [ num_var ] {0, 2}
def p_dimension(p):
    '''dimension    : '[' num_var ']' dimension_1 '''
    # print("dimension", p[1:4])
    p[0] = (p[2], p[4])
    pass


def p_dimension_1(p):
    '''dimension_1  : '[' num_var ']' 
                    | epsilon '''
    # print("dimension x2", p[1:4])
    if len(p) > 2:
        p[0] = p[2]
    pass


def p_tipo(p):
    '''tipo : INT 
            | FLOAT
            | STRING
            | CHAR
            | DATAFRAME'''
    p[0] = p[1]
    pass


def p_declare_func(p):
    '''declare_func : '''
    global_context.set_function(p[-1])
    function_table.declare_function(func_name=p[-1], return_type=global_context.var_type)


# function tipo_retorno ID ( parameters? ) vars? { bloque? }
def p_function(p):
    '''function     : FUNCTION tipo_retorno ID declare_func '(' function_1 ')' function_2 '{' bloque '}' '''
    print("Function", p[3])
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
    p[0] = p[1]
    global_context.set_type(p[1])
    pass


# TIPO 'id' (',' TIPO 'id')*
def p_parameters(p):
    '''parameters       : tipo ID parameters_1
                        | epsilon'''
    if len(p) > 2:
        function_table.add_parameter(global_context.function, Variable(p[1], p[2]))


def p_parameters_1(p):
    '''parameters_1     : ',' tipo ID parameters_1
                        | epsilon'''
    if len(p) > 2:
        function_table.add_parameter(global_context.function, Variable(p[2], p[3]))


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
    print("Assign", p[1])
    # TODO buscar id en tabla de variables
    # find id_completo
    # match type of expression and id_completo
    pass


# return ( EXP ) ;
def p_return(p):
    '''return   : RETURN '(' exp ')' ';' '''
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
    '''condition    : IF '(' expression ')' THEN '{' condition_1 '}' condition_2 '''
    # print(p[3])
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
    print("num var", p[1])
    p[0] = p[1]
    pass


def p_string_var(p):
    ''' string_var  : ID 
                    | CTE_STRING '''
    pass


def p_var_cte(p):
    '''var_cte      : var_cte_1
                    | CTE_I 
                    | CTE_F 
                    | CTE_STRING 
                    | CTE_CHAR '''
    # print("Var_Cte", p[1])
    pass


def p_var_cte_1(p):
    '''var_cte_1    : ID var_cte_2'''
    # print("id?", p[1], p[2])
    pass


def p_var_cte_2(p):
    '''var_cte_2    : func_call_1
                    | epsilon'''
    # print("func_call?", p[1])
    pass


# ID ( EXPRESION* ) ;


def p_func_call(p):
    '''func_call    : ID '(' func_call_1 ')' ';' '''
    pass


def p_func_call_1(p):
    '''func_call_1  : expression func_call_2
                    | epsilon '''
    pass


def p_func_call_2(p):
    '''func_call_2  : ',' expression func_call_2
                    | epsilon '''
    pass


# ( EXP | LLAMADA ) ( ( '>' | '<' | '==' | '<>' ) ( EXP | LLAMADA ) )?
def p_expression(p):
    ''' expression      : exp expression_1 '''
    # print("Expression ", p[1], p[2])
    pass


def p_expression_1(p):
    '''expression_1     : comparison_ops exp
                        | epsilon'''
    pass


def p_comparison_ops(p):
    '''comparison_ops   : '<' 
                        | '>' 
                        | DIFF 
                        | EQUAL '''
    pass


# TERMINO ( ( '+' | '-' ) TERMINO )*
def p_exp(p):
    '''exp      : termino exp_1 '''
    # print("Exp", p[1])
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
    # print("Termino", p[1])
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
    # if (p[2]):
    #     print("Factor", p[2])
    pass


def p_factor_1(p):
    '''factor_1     : '+' 
                    | '-' 
                    | epsilon '''
    pass


def p_bloque(p):
    '''bloque   : bloque_1'''
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

# EJEMPLO PARA PROBAR SEGÚN LA VARIABLE DATA

data = '''
program donpato;
var float:numero[0][0], mat[1], wat, dude;
    int: data, custom, suma;
    char: a;
    string: hi;
    
function void hello(int time, float day) 
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
	if (numeroPi < hi) then {
		numeroPi = 3.14159;
	}
    else
    {
		print("Coronavirus will destroy math");
	}
    if (3 > 2) then {
        numero = 5.5;
    }
}
'''

# data = '''
# program donpato;
# var float:numero;
# main() {
#     numeroPi = 3.1;
# 	if (numeroPi < hi) {
# 		numeroPi = 3.14159;
# 	}
#     else
#     {
# 		print("Coronavirus will destroy math");
# 	}
# }
# '''


logging.basicConfig(
        level=logging.DEBUG,
        filemode="w",
        filename="parselog.txt")

if (parser.parse(data, tracking=True, debug=logging.getLogger()) == 'COMPILA'):
    print("Sintaxis aceptada")
else:
    print("error de sintaxis")

for k, v in function_table.table.items():
    print(v.__str__())