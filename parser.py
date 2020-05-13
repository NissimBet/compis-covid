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
from CuboSemantico import CuboSemantico
from Quadruple import Quadruple
from lexer import tokens, literals

from Stack import Stack
from Queue import Queue
from DataUtils import ParsingContext
from Variable import Variable, VariableTable
from Function import FunctionTable
from AVAIL import avail

function_table = FunctionTable()
global_context = ParsingContext()

global_context.set_function("global")
function_table.declare_function('global', 'void')


def p_goto_main(p):
    """goto_main    :"""
    quad_index = global_context.create_quad(Quadruple.OperationType.GOTO, "", "", "")
    global_context.jumpStack.push(quad_index)


# program id ; VARS? function* main
def p_programa(p):
    """programa     : PROGRAM ID ';' programa_1 main"""
    p[0] = "COMPILA"
    pass


def p_programa_1(p):
    """programa_1   : vars goto_main programa_2
                    | goto_main programa_2 """
    # print("Programa ", p[1])
    pass


def p_programa_2(p):
    """programa_2   : function programa_2
                    | epsilon"""
    pass


# var (tipo : lista_id ;)+
def p_vars(p):
    """vars         : VAR vars_1 """
    pass


def p_set_var_type(p):
    """set_var_type : """
    # TODO push el tipo de variable a stack
    global_context.set_type(p[-1])


def p_vars_1(p):
    """vars_1       : tipo set_var_type ':' lista_id ';' vars_2 """
    # print("vars_1", p[1], p[4], p[6])
    pass


def p_vars_1_error(p):
    """vars_1       : tipo set_var_type ':' lista_id error ';' vars_2 """
    print("Error de sintaxis en la declaración de variables. Línea ", p.lineno(5), ", Posición", p.lexpos(5))


def p_vars_2(p):
    """vars_2       : vars_1
                    | epsilon """
    pass


def p_declare_var(p):
    """declare_var  : """
    # TODO tomar prestado el tipo de variable ultimo en el scope
    # TODO tomar prestado el nombre de la ultima funcion en el scope
    if not function_table.declare_variable(global_context.function.top(),
                                           Variable(global_context.var_type, p[-1][0], p[-1][1])):
        print(
                f'Error de Sintaxis en la declaracion de variables. Linea {p.lineno(-1)}. \
                Variable "{p[-1][0]}" ya esta declarada en este contexto')


# lista_id : id (, id)*
def p_lista_id(p):
    """lista_id     : id_completo declare_var lista_id_1"""
    if p[2] is not None:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = [p[1]]
    pass


def p_lista_id_1(p):
    """lista_id_1   : ',' id_completo declare_var lista_id_1
                    | epsilon"""
    if len(p) > 2:
        if p[3] is not None:
            p[0] = [p[2]] + p[3]
        else:
            p[0] = [p[2]]
    pass


# id dimension?
def p_id_completo(p):
    """id_completo      : ID id_completo_1"""
    # print("Id Completo",p[1], p[2])
    p[0] = p[1], p[2]
    pass


def p_id_completo_1(p):
    """id_completo_1    : dimension
                        | epsilon"""
    # print("Id_completo_1 ", p[1])
    p[0] = p[1]
    pass


def p_id_completo_1_error(p):
    """id_completo_1    : error """
    print("Syntax error while declaring variable dimensions.")
    pass


# TODO debe ser num_var entera
# [ num_var ] {0, 2}
def p_dimension(p):
    """dimension    : '[' num_var ']' dimension_1 """
    # print("dimension", p[1:4])
    p[0] = (p[2], p[4])


def p_dimension_1(p):
    """dimension_1  : '[' num_var ']'
                    | epsilon """
    # print("dimension x2", p[1:4])
    if len(p) > 2:
        p[0] = p[2]


def p_tipo(p):
    """tipo : INT
            | FLOAT
            | STRING
            | CHAR
            | BOOL
            | DATAFRAME"""
    p[0] = p[1]


def p_declare_func(p):
    """declare_func : """
    # TODO tomar prestado el tipo de la ultima funcion en el scope
    if not function_table.declare_function(func_name=p[-1], return_type=global_context.var_type):
        print(f'Error de Sintaxis en declacion de funciones. Linea {p.lineno(-1)}. Funcion "{p[-1]}" ya esta declarada')
    else:
        # TODO agregar la funcion al scope
        global_context.set_function(p[-1])


# function return_type ID ( parameters? ) vars? { bloque? }
def p_function(p):
    """function     : FUNCTION return_type ID declare_func '(' function_1 ')' function_2 '{' bloque '}' """
    # print("Function", p[3])
    # TODO quitar la funcion del scope
    global_context.function.pop()


def p_function_1(p):
    """function_1   : parameters
                    | epsilon """
    pass


def p_function_2(p):
    """function_2   : vars
                    | epsilon """
    pass


def p_return_type(p):
    """return_type  : tipo
                    | VOID """
    p[0] = p[1]
    # TODO poner el tipo de retorno de la funcion
    global_context.set_type(p[1])


# TIPO 'id' (',' TIPO 'id')*
def p_parameters(p):
    """parameters       : tipo ID parameters_1
                        | epsilon"""
    if len(p) > 2:
        # TODO tomar prestado el nombre de la funcion ultima en el contexto
        if not function_table.add_parameter(global_context.function.top(), Variable(p[1], p[2])):
            print(
                    f"Error de Sintaxis. Linea {p.lineno(2)}. No se pudo declarar el parametro {p[2]}. Ya esta declarado en el scope")


def p_parameters_1(p):
    """parameters_1     : ',' tipo ID parameters_1
                        | epsilon"""
    if len(p) > 2:
        # TODO tomar prestado el nombre de la funcion ultima en el contexto
        if not function_table.add_parameter(global_context.function.top(), Variable(p[2], p[3])):
            print(
                    f"Error de Sintaxis. Linea {p.lineno(3)}. No se pudo declarar el parametro {p[3]}. Ya esta declarado en el scope")


def p_statement(p):
    """statement    : condition
                    | statement_1 ';' """
    pass


def p_statement_1(p):
    """statement_1  : assignment
                    | func_call
                    | return
                    | read
                    | write
                    | load
                    | loop"""


def p_check_variable(p):
    """check_variable   : """
    # TODO tomar prestado el nombre de la funcion ultima en el contexto
    if not function_table.is_variable_declared(global_context.function.top(), p[-1][0]):
        print(f'Error de Sintaxis. Error de asignacion en linea {p.lineno(-1)}. Variable no declarada {p[-1][0]}')


# ID_COMPLETO '=' EXPRESsION
def p_assignment(p):
    """assignment   : id_completo check_variable '=' logic_comp """
    assigned = function_table.get_variable(global_context.function.top(),p[1][0])
    operand_type = global_context.types.pop()
    operand_name = global_context.operands.pop()
    global_context.create_quad(Quadruple.OperationType.ASSIGN, operand_name, "", assigned.name)
    print(f"Assign to {p[1][0]}, {p[4]}")


def p_assignment_error(p):
    """assignment   : id_completo check_variable '=' error """
    print(f"Error de Sintaxis. Linea {p.lineno(4)}. Asignacion incompleta")
    pass


# return ( EXP )
def p_return(p):
    """return   : RETURN '(' exp ')' """
    # TODO tomar prestado el nombre de la funcion ultima en el contexto
    print(f"Retorno de funcion {global_context.function.top()}, tipo {p[3]}")
    pass


# read ( LISTA_ID )
def p_read(p):
    """read     : READ '(' lista_id ')' """
    pass


# write '(' ( EXPRESION | string_var )+ ')'
def p_write(p):
    """write    :  WRITE '(' write_1 write_2 ')' """
    pass


def p_write_1(p):
    """write_1  : logic_comp
                | string_var """
    pass


def p_write_2(p):
    """write_2  : ',' write_1 write_2
                | epsilon """
    pass


# load ( id , ruta_acceso , num_var , num_var )
def p_load(p):
    """load     : LOAD '(' ID ',' string_var ',' string_var ',' num_var ')' """
    pass


def p_declare_main(p):
    """declare_main : """
    # TODO declarar main
    global_context.set_function('main')
    function_table.declare_function('main', 'void')
    global_context.fill_quad()


def p_main(p):
    """main     : MAIN declare_main '(' ')' main_1 '{' bloque '}'  """
    pass


def p_main_1(p):
    """main_1   : vars
                | epsilon """
    pass


def p_logic_comp_check(p):
    """logic_comp_check : """
    print(f'Resultado de expresion es {p[-1]}. Lineno {p.lineno(-1)}')


# if ( EXPRESION ) then { bloque? } ( else { bloque? } )?
def p_condition(p):
    """condition    : IF '(' logic_comp logic_comp_check ')' THEN '{' condition_1 '}' condition_2 """
    # global_context.create_quad(Quadruple.OperationType.GOTO_FALSE, '/', '/', 'LINE')
    # print(p[3])
    pass


def p_condition_1(p):
    """condition_1  : bloque
                    | epsilon """
    pass


def p_condition_2(p):
    """condition_2  : ELSE '{' condition_1 '}'
                    | epsilon"""
    pass


def p_loop(p):
    """loop     : conditional_loop
                | no_condition_loop """
    pass


# while ( EXPRESION ) do { bloque? }
def p_conditional_loop(p):
    """conditional_loop     : WHILE '(' logic_comp ')' DO '{' conditional_loop_1 '}' """
    # global_context.create_quad(Quadruple.OperationType.GOTO_FALSE, '/', '/', 'LINE')
    pass


def p_conditional_loop_1(p):
    """conditional_loop_1   : bloque
                            | epsilon """
    pass


# desde ID_COMPLETO = EXP to EXP hacer { ESTATUTO* }
def p_no_condition_loop(p):
    """no_condition_loop    : FROM id_completo '=' exp TO exp DO '{' no_condition_loop_1 '}'  """
    pass


def p_no_condition_loop_1(p):
    """no_condition_loop_1  : bloque
                            | epsilon """
    pass


def p_num_var(p):
    """ num_var     : ID
                    | CTE_I
                    | CTE_F """
    # print("num var", p[1])
    p[0] = p[1]


def p_string_var(p):
    """ string_var  : ID
                    | CTE_STRING """
    p[0] = p[1]


def p_var(p):
    """var      : ID var_1"""
    p[0] = p[1]
    # print("id?", p[1])


def p_var_1(p):
    """var_1    : '(' func_call_1 ')'
                | dimension
                | epsilon"""
    # print("VAR", p[1])


def p_var_cte(p):
    """var_cte      : CTE_I
                    | CTE_F
                    | CTE_STRING
                    | CTE_CHAR
                    | var_bool """
    print("Var_Cte", p.lineno(1), p[1])
    p[0] = p[1]


def p_var_bool(p):
    """var_bool     : TRUE
                    | FALSE"""
    p[0] = p[1]


# ID ( EXPRESION* ) ;
def p_stat_methods(p):
    """stat_methods : stat_methods_1 '(' func_call_1 ')'
    """
    p[0] = p[1]


def p_stat_methods_1(p):
    """stat_methods_1   : MEAN
                        | MODE
                        | VARIANCE
                        | NORMAL
                        | GAMMA
                        | GRAPH
                        | NORMAL_GRAPH
                        | COV
                        | SCATTER
    """
    print('Stats Method:', p[1])
    p[0] = p[1]


def p_func_call(p):
    """func_call    : ID '(' func_call_1 ')'
                    | stat_methods """
    p[0] = p[1]


def p_func_call_1(p):
    """func_call_1  : logic_comp func_call_2
                    | epsilon """
    pass


def p_func_call_2(p):
    """func_call_2  : ',' logic_comp func_call_2
                    | epsilon """
    pass


def p_logic_comp_cuad(p):
    """logic_comp_cuad  : """
    global_context.create_operation_quad(["&", "||"])


def p_logic_comp(p):
    """logic_comp       : expression logic_comp_cuad logic_comp_1"""
    p[0] = p[1]


def p_logic_comp_1(p):
    """logic_comp_1     : logic_comp_ops expression logic_comp_cuad logic_comp_1
                        | epsilon"""
    pass


def p_logic_comp_ops(p):
    """logic_comp_ops   : '&'
                        | OR"""
    p[0] = p[1]
    global_context.operations.push(p[1])
    pass


# ( EXP ) ( ( '>' | '<' | '==' | '<>' ) ( EXP ) )?
def p_expression(p):
    """ expression      : exp expression_1 """
    if p[2]:
        # TODO hacer la comparacion
        p[0] = p[2][1]
        global_context.create_operation_quad([">", "<", "<>", "=="])
    else:
        p[0] = p[1]


def p_expression_1(p):
    """expression_1     : comparison_ops exp
                        | epsilon"""
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = (p[1], p[2])


def p_comparison_ops(p):
    """comparison_ops   : '<'
                        | '>'
                        | DIFF
                        | EQUAL """
    global_context.operations.push(p[1])
    p[0] = p[1]


def p_exp_cuad(p):
    """exp_cuad   : """
    global_context.create_operation_quad(["+", "-"])


# TERMINO ( ( '+' | '-' ) TERMINO )*
def p_exp(p):
    """exp      : termino exp_cuad exp_1 """
    if p[2]:
        p[0] = p[1]
    else:
        # TODO hacer multiplicacion
        p[0] = p[1]


def p_exp1(p):
    """exp_1    : exp_2 termino exp_cuad exp_1
                | epsilon"""
    if len(p) > 2:
        # TODO hacer multiplicacion o division
        p[0] = p[2]
    else:
        p[0] = None


def p_exp_2(p):
    """exp_2    : '+'
                | '-' """
    p[0] = p[1]
    global_context.operations.push(p[1])


def p_termino_vp(p):
    """termino_vp    : """
    global_context.create_operation_quad(["*", "/"])


# FACTOR ( ( '*' | '/' ) FACTOR )*
def p_termino(p):
    """termino      : factor termino_vp termino_1 """
    # print("Termino", p[1])
    if p[2]:
        p[0] = p[1]
    else:
        p[0] = p[1]


def p_termino_1(p):
    """termino_1    : termino_2 factor termino_vp termino_1
                    | epsilon """
    if len(p) > 2:
        p[0] = p[2]
    else:
        p[0] = None


def p_termino_2(p):
    """termino_2    : '*'
                    | '/' """
    p[0] = p[1]
    global_context.operations.push(p[1])


def p_remove_false_bottom(p):
    """remove_false_bottom  : """
    global_context.operations.remove_separator()


def p_add_false_bottom(p):
    """add_false_bottom     : """
    global_context.operations.add_separator()


def p_factor(p):
    """factor       : '(' add_false_bottom logic_comp remove_false_bottom ')'
                    | factor_1 factor_2"""
    if len(p) == 3:
        if p[1] == '+':
            p[0] = p[2]
        elif p[1] == '-':
            global_context.operands.push(p[2])
            global_context.types.push(function_table.get_variable(global_context.function.top(), p[2]).type)
            global_context.operations.push("=")
            global_context.operations.push("*")
            global_context.operands.push('-1')
            global_context.types.push("int")
            global_context.create_operation_quad(['*'])
            global_context.create_operation_quad(['='])
            # p[0] = -p[2]
        p[0] = p[2]
    else:
        p[0] = p[3]


def p_factor_1(p):
    """factor_1     : '+'
                    | '-'
                    | epsilon """
    p[0] = p[1]


def p_factor_var_check(p):
    """factor_var_check : """
    if not function_table.is_variable_declared(global_context.function.top(), p[-1]):
        print(f'Error de sintaxis. Variable {p[-1]} no declarada en linea {p.lineno(-1)}')
    else:
        variable = function_table.get_variable(global_context.function.top(), p[-1])
        global_context.types.push(variable.type)
        global_context.operands.push(variable.name)


def p_factor_2(p):
    """factor_2     : var_cte
                    | var factor_var_check"""
    p[0] = p[1]


def p_bloque(p):
    """bloque   : statement bloque
                | epsilon"""
    pass


def p_epsilon(p):
    """epsilon :"""
    pass


# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")
    print(p)
    pass


# Build the parser
parser = yacc.yacc(start="programa")

# EJEMPLO PARA PROBAR SEGÚN LA VARIABLE DATA

# data = '''
# program donpato;
# var float:numero[0][0], mat[1], wat, dude;
#     int: data, custom, suma;
#     char: a;
#     string: hi;
#     bool: ahora;
#
# function void hello(int time, float day)
#     var string: hello, world, hi;
#     {
#         return (hello + world);
#     }
# function void there()
#     var string: hello, world;
#     {
#         return (hello + world);
#     }
#
# main() var int: numeroPi; {
#     numeroPi = 3.1;
# 	if (numeroPi < hi) then {
# 		numeroPi = 3.14159;
# 	}
#     else
#     {
# 		print("Coronavirus will destroy math");
# 	}
#     if (3 > 2) then {
#         numero = 5.5;
#         numeroPi = "12312";
#         numero = true;
#     }
#     else {
#         scatter(numeroPi);
#         numeroPi = 12 + there();
#     }
# }
# '''

data = """
program test;
var int: a ,b;
bool: t, f;
main () var int: x, c, d; {
    a = d + -c;
    x = (a + c) * d / d;
    if (b > a) then {
        t = f & f;
    }
}
"""

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

if parser.parse(data, tracking=True, debug=logging.getLogger()) == 'COMPILA':
    print("Sintaxis aceptada")
else:
    print("error de sintaxis")

for k, v in function_table.table.items():
    print(v.__str__())

print(global_context.types)
print(global_context.operands)
print(global_context.operations)

# quads display
for quad in global_context.quadruples:
    print(quad)
