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
from Quadruple import Quadruple
from lexer import tokens, literals

from DataUtils import ParsingContext
from Variable import Variable

from AVAIL import avail

global_context = ParsingContext()

global_context.set_function("global")
global_context.declare_function('global', 'void')


def p_goto_main(_):
    """goto_main    :"""
    global_context.create_quad(Quadruple.OperationType.GOTO, "", "", "")
    global_context.create_jump()


# program id ; VARS? function* main
def p_programa(p):
    """programa     : PROGRAM ID ';' programa_1 main"""
    p[0] = "COMPILA"
    pass


def p_programa_1(_):
    """programa_1   : vars goto_main programa_2
                    | goto_main programa_2 """


def p_programa_2(_):
    """programa_2   : function programa_2
                    | epsilon"""
    pass


# var (tipo : lista_id ;)+
def p_vars(_):
    """vars         : VAR vars_1 """
    pass


def p_set_var_type(p):
    """set_var_type : """
    # TODO push el tipo de variable a stack
    global_context.set_type(p[-1])


def p_vars_1(_):
    """vars_1       : tipo set_var_type ':' lista_id ';' vars_2 """


def p_vars_1_error(p):
    """vars_1       : tipo set_var_type ':' lista_id error ';' vars_2 """
    print("Error de sintaxis en la declaración de variables. Línea ", p.lineno(5), ", Posición", p.lexpos(5))


def p_vars_2(_):
    """vars_2       : vars_1
                    | epsilon """


def p_declare_var(p):
    """declare_var  : """
    # TODO tomar prestado el tipo de variable ultimo en el scope
    # TODO tomar prestado el nombre de la ultima funcion en el scope
    # print('variable dimension', p[-1][1])
    if not global_context.declare_variable(p[-1][0], p[-1][1], global_context.function.top() == "global"):
        print(
                f'Error de Sintaxis en la declaracion de variables. Linea {p.lineno(-1)}. \
                Variable "{p[-1][0]}" ya esta declarada en este contexto')


# lista_id : id (, id)*
def p_lista_id(p):
    """lista_id     : declare_id declare_var lista_id_1"""
    if p[2] is not None:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = [p[1]]


def p_lista_id_1(p):
    """lista_id_1   : ',' declare_id declare_var lista_id_1
                    | epsilon"""
    if len(p) > 2:
        if p[3] is not None:
            p[0] = [p[2]] + p[3]
        else:
            p[0] = [p[2]]


def p_declare_id(p):
    """declare_id   : ID declare_id_1"""
    p[0] = p[1], p[2]


def p_declare_id_1(p):
    """declare_id_1 : '[' CTE_I ']' declare_id_2
                    | epsilon"""
    if p[1]:
        p[0] = (p[2], p[4])


def p_declare_id_2(p):
    """declare_id_2 : '[' CTE_I ']'
                    | epsilon"""
    if len(p) > 2:
        p[0] = p[2]


# id dimension?
def p_id_completo(p):
    """id_completo      : ID id_completo_1"""
    # print("Id Completo",p[1], p[2])
    p[0] = p[1], p[2]


def p_id_completo_1(p):
    """id_completo_1    : dimension
                        | epsilon"""
    p[0] = p[1]

#  operand = global_context.operands.pop()
#         operand_type = global_context.types.pop()
#         global_context.create_quad(Quadruple.OperationType.GOTO_FALSE, operand, "", "")
    
# usar produccion exp, y verificar los tipos que aparecen

def p_id_completo_1_error(_):
    """id_completo_1    : error """
    print("Syntax error while declaring variable dimensions.")

def p_check_dimension_exists(p):
    """check_dimension_exists   : """
    
    if global_context.get_dimensions(p[-2]) == 0:
        print('Error de sintaxis: Variable no tiene dimensiones:', p[-2])
    else:
        var = global_context.get_variable(p[-2])
        global_context.operands.push(var)

def p_cuadruplo_verificacion(p):
    """cuadruplo_verificacion : """
    # print('pilaoperandos', global_context.operands.top())
    var = global_context.operands.top()
    print('direccion dimension', var.dimensions[0])
    # dimensions = global_context.get_dimensions(var.name)
    # val_accesado = int(avail.get_val_from_dir(p[-1]))
    # print('dir var', var.direction, var)
    # print('direcciones de dims', global_context.get_variable(var.name).dimensions[0].r )
    # if (val_accesado < dimensions[0]):
    #     global_context.dimensions.push(dimensions[0])
    # else:
    #     print('Error de sintaxis: Fuera de límite en acceso')
    
    # print('dimension y num_var', dimensions[0], valdir)
    # if (dimensions[0] < )
    # dim_list = global_context.get_dimensions(var[0])
    # print('dimlist', dim_list)
    # dim_size = dim_list[0]
    # global_context.create_quad(Quadruple.OperationType.VER, var, "", dim_size)


# TODO debe ser num_var entera
# [ num_var ] {0, 2}
def p_dimension(p):
    """dimension    : '[' check_dimension_exists num_var cuadruplo_verificacion ']' dimension_1 """
    p[0] = (p[3], p[6])
    # print('numvar', avail.get_val_from_dir(p[3]),avail.get_val_from_dir(p[6]) )
    
   


def p_dimension_1(p):
    """dimension_1  : '[' num_var ']'
                    | epsilon """
    # print("dimension x2", p[1:4])
    if len(p) > 2:
        p[0] = p[2]
    # print ('This is p4', p[0])


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
    if not global_context.declare_function(p[-1], None):
        print(f'Error de Sintaxis en declacion de funciones. Linea {p.lineno(-1)}. Funcion "{p[-1]}" ya esta declarada')
        # avail.reset_locals()


# function return_type ID ( parameters? ) vars? { bloque? }
def p_function(_):
    """function     : FUNCTION return_type ID declare_func '(' function_1 ')' function_2 '{' bloque '}' """
    global_context.end_function()


def p_function_1(_):
    """function_1   : parameters
                    | epsilon """


def p_function_2(_):
    """function_2   : vars
                    | epsilon """


def p_return_type(p):
    """return_type  : tipo
                    | VOID """
    p[0] = p[1]
    # TODO poner el tipo de retorno de la funcion
    global_context.set_type(p[1])


def p_add_param(p):
    """add_param    : """
    var_type = global_context.var_type
    var_name = p[-1]
    global_context.add_function_parameter(Variable(var_type, var_name, []))


# TIPO 'id' (',' TIPO 'id')*
def p_parameters(_):
    """parameters       : tipo set_var_type ID add_param parameters_1
                        | epsilon"""


def p_parameters_1(_):
    """parameters_1     : ',' tipo set_var_type ID add_param parameters_1
                        | epsilon"""


def p_statement(_):
    """statement    : condition
                    | loop
                    | statement_1 ';' """


def p_statement_1(_):
    """statement_1  : assignment
                    | func_call
                    | return
                    | read
                    | write
                    | load"""


def p_check_variable(p):
    """check_variable   : """
    if not global_context.is_variable_declared(p[-1][0]):
        print(f'Error de Sintaxis. Error de asignacion en linea {p.lineno(-1)}. Variable no declarada {p[-1][0]}')


# ID_COMPLETO '=' EXPRESSION
def p_assignment(p):
    """assignment   : id_completo check_variable '=' logic_comp """
    assigned = global_context.get_variable(p[1][0])
    operand_type = global_context.types.pop()
    operand_name = global_context.operands.pop()
    global_context.create_quad(Quadruple.OperationType.ASSIGN, operand_name, "", assigned.direction)
    # print(f"Assign to {p[1][0]}, {p[4]}")


def p_assignment_error(p):
    """assignment   : id_completo check_variable '=' error """
    print(f"Error de Sintaxis. Linea {p.lineno(4)}. Asignacion incompleta")


# return ( EXP )
def p_return(p):
    """return   : RETURN '(' exp ')' """
    # TODO tomar prestado el nombre de la funcion ultima en el contexto
    print(f"Retorno de funcion {global_context.function.top()}, tipo {p[3]}")
    function = global_context.get_function()
    exp_type = global_context.types.pop()
    exp_val = global_context.operands.pop()
    if exp_type != function.return_type:
        print(f"Error, wrong return type. Expecting {function.return_type} on function {function.name}")


def p_set_func(p):
    """set_func     :"""
    global_context.operations.add_separator()
    global_context.func_calls.push(p[-1])


def p_check_read_param(p):
    """check_read_param  : """
    var = global_context.get_variable(p[-1][0])
    if var:
        global_context.create_quad(Quadruple.OperationType.READ, "", "", var.direction)
    else:
        print(f"Error. Variable {p[-1]} not declared in line {p.lineno(-1)}")


def p_read_param(_):
    """read_param     : id_completo check_read_param read_param_1"""


def p_read_param_1(_):
    """read_param_1    : ',' id_completo check_read_param read_param_1
                         | epsilon"""


# read ( LISTA_ID )
def p_read(p):
    """read     : READ set_func '(' read_param ')' """
    global_context.func_calls.pop()
    global_context.operations.remove_separator()
    p[0] = p[1]


def p_check_write_param(_):
    """check_write_param  : """
    var_name = global_context.operands.pop()
    var_type = global_context.types.pop()

    global_context.create_quad(Quadruple.OperationType.WRITE, "", "", var_name)


def p_write_param(_):
    """write_param     : logic_comp check_write_param write_param_1"""


def p_write_param_1(_):
    """write_param_1    : ',' logic_comp check_write_param write_param_1
                        | epsilon"""


# write '(' ( EXPRESION | string_var )+ ')'
def p_write(_):
    """write    :  WRITE set_func '(' write_param ')' """
    global_context.func_calls.pop()
    global_context.operations.remove_separator()


def p_load(p):
    """load     : LOAD '(' ID ',' string_var ',' ID ',' ID ')' """
    try:
        var_name = p[3]
        path = p[5]

        num_lines_var_name = p[7]
        num_vars_var_name = p[9]

        var = global_context.get_variable(var_name)
        num_lines = global_context.get_variable(num_lines_var_name)
        num_vars = global_context.get_variable(num_vars_var_name)

        if var and num_lines and num_vars:
            if var.type == "dataFrame":
                if num_lines.type == "int" and num_vars.type == "int":
                    global_context.create_quad(Quadruple.OperationType.FILE_SEARCH, path, "", var.direction)
                    global_context.create_quad(Quadruple.OperationType.LINES, var.direction, "", num_lines.direction)
                    global_context.create_quad(Quadruple.OperationType.COLS, var.direction, "", num_vars.direction)
                else:
                    if num_lines.type == "int":
                        print(f"ERROR in line {p.lineno(7)}. Expected int, got {num_lines.type}")
                    if num_vars.type == "int":
                        print(f"ERROR in line {p.lineno(9)}. Expected int, got {num_vars.type}")
            else:
                print(f"ERROR in line {p.lineno(3)}. Expected type dataFrame, got {var.type}")
        else:
            if not var:
                print(f"ERROR in line {p.lineno(3)}. Variable not declared {p[3]}")
            if not num_lines:
                print(f"ERROR in line {p.lineno(7)}. Variable not declared {p[7]}")
            if not num_vars:
                print(f"ERROR in line {p.lineno(9)}. Variable not declared {p[9]}")
    except IndexError:
        print(f"ERROR in line {p.lineno(0)}. Too little variables provided")


def p_declare_main(_):
    """declare_main : """
    global_context.declare_function('main', 'void')
    global_context.fill_quad()


def p_main(_):
    """main     : MAIN declare_main '(' ')' main_1 '{' bloque '}'  """
    pass


def p_main_1(_):
    """main_1   : vars
                | epsilon """
    pass


def p_logic_comp_check(p):
    """logic_comp_check : """
    if not global_context.types.top() == "bool":
        print(f"Type Error. Se esperaba un valor booleano en linea {p.lineno(-1)}")
    else:
        operand = global_context.operands.pop()
        operand_type = global_context.types.pop()
        global_context.create_quad(Quadruple.OperationType.GOTO_FALSE, operand, "", "")
        global_context.create_jump()


# if ( EXPRESION ) then { bloque? } ( else { bloque? } )?
def p_condition(_):
    """condition    : IF '(' logic_comp logic_comp_check ')' THEN '{' condition_1 '}' condition_2 """
    global_context.fill_quad()


def p_condition_1(_):
    """condition_1  : bloque
                    | epsilon """
    pass


def p_go_else(_):
    """go_else      : """
    global_context.create_quad(Quadruple.OperationType.GOTO, "", "", "")
    global_context.fill_quad()
    global_context.create_jump()


def p_condition_2(_):
    """condition_2  : ELSE go_else '{' condition_1 '}'
                    | epsilon"""
    pass


def p_loop(_):
    """loop     : conditional_loop
                | no_condition_loop """
    pass


def p_check_loop(p):
    """check_loop   : """
    if not global_context.types.top() == "bool":
        print(f"Type Error. Se esperaba un valor booleano en linea {p.lineno(-1)}")
    else:
        operand = global_context.operands.pop()
        operand_type = global_context.types.pop()
        global_context.create_quad(Quadruple.OperationType.GOTO_FALSE, operand, "", "")
        global_context.create_jump()


def p_while_return(_):
    """while_return     : """
    global_context.create_jump()


# while ( EXPRESION ) do { bloque? }
def p_conditional_loop(_):
    """conditional_loop     : WHILE '(' while_return logic_comp check_loop ')' DO '{' conditional_loop_1 '}' """
    # global_context.create_quad(Quadruple.OperationType.GOTO_FALSE, '/', '/', 'LINE')
    # quads display
    end = global_context.jumpStack.pop()
    start = global_context.jumpStack.pop()
    global_context.create_quad(Quadruple.OperationType.GOTO, "", "", start + 1)
    global_context.fill_quad(end)


def p_conditional_loop_1(_):
    """conditional_loop_1   : bloque
                            | epsilon """
    pass


def p_for_check_id(p):
    """for_check_id     : """
    if global_context.is_variable_declared(p[-1][0]):
        var = global_context.get_variable(p[-1][0])
        global_context.operands.push(var.direction)
        global_context.types.push(var.type)
    else:
        print(f"Sintax Error. Variable {p[-1][0]} not declared in line {p.lineno(-1)}")


def p_for_assign(_):
    """for_assign   : """
    global_context.operations.push("=")
    global_context.create_operation_quad(["="])


def p_for_compare(_):
    """for_compare  : """
    global_context.create_jump()
    global_context.operations.push("<")
    global_context.create_operation_quad(["<"])
    operand = global_context.operands.pop()
    op_type = global_context.types.pop()
    global_context.create_quad(Quadruple.OperationType.GOTO_FALSE, operand, "", "")
    global_context.create_jump()


# desde ID_COMPLETO = EXP to EXP hacer { ESTATUTO* }
def p_no_condition_loop(_):
    """no_condition_loop    : FROM id_completo for_check_id '=' exp for_assign TO exp for_compare DO '{' no_condition_loop_1 '}'  """
    end = global_context.jumpStack.pop()
    start = global_context.jumpStack.pop()
    global_context.create_quad(Quadruple.OperationType.GOTO, "", "", start + 1)
    global_context.fill_quad(end)


def p_no_condition_loop_1(_):
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


def p_var_cte(p):
    """var_cte      : CTE_I
                    | CTE_F
                    | CTE_STRING
                    | CTE_CHAR
                    | var_bool """
    # print("Var_Cte", p.lineno(1), p[1])
    p[0] = p[1]


def p_var_bool(p):
    """var_bool     : TRUE
                    | FALSE"""
    # print(p[1])
    p[0] = p[1]


# ID ( EXPRESION* ) ;
def p_std_methods(p):
    """std_methods : MEAN
                    | MODE
                    | VARIANCE
                    | NORMAL
                    | GAMMA
                    | GRAPH
                    | NORMAL_GRAPH
                    | COV
                    | SCATTER
                    | ID
    """
    p[0] = p[1]


def p_called_func(p):
    """called_func  : """
    f_name = p[-1]
    if f_name in global_context.function_table.table:
        global_context.operations.add_separator()
        global_context.func_calls.push(f_name)
        global_context.param_counter.push(0)
        function_size = global_context.get_function().count_vars()
        for var_type, var_nums in function_size.items():
            global_context.create_quad(Quadruple.OperationType.ERA, var_type, "", var_nums)
    else:
        print(f"Syntax Error, function not defined {f_name} in line {p.lineno(-1)}")


def p_func_call(p):
    """func_call    : std_methods called_func '(' func_call_1 ')'  """
    try:
        global_context.create_quad(Quadruple.OperationType.GO_SUB, "", "",
                                   global_context.function_table.function(p[1]).quad_number + 1)
    except IndexError:
        print("No se pudo crear el cuadruplo")
    f_name = global_context.func_calls.pop()
    f_params = global_context.param_counter.pop()
    global_context.operations.remove_separator()
    if len(global_context.function_table.function(f_name).parameters) != f_params:
        print(
            f"Syntax Error. Function {f_name} missing parameters, expected {len(global_context.function_table.function(f_name).parameters)}, got {f_params}")
    p[0] = p[1]


def p_check_param(p):
    """check_param : """
    function_name = global_context.func_calls.top()
    function = global_context.function_table.function(function_name)
    if global_context.param_counter.top() < len(function.parameters):
        vtype = global_context.types.pop()
        var = global_context.operands.pop()
        if vtype == function.parameters[global_context.param_counter.top()].type:
            global_context.create_quad(Quadruple.OperationType.PARAMETER, var, "", global_context.param_counter.top())
            print(f"Parametro encontrado {var} en funcion {function.name}")
        else:
            print(
                    f"Type Error on line {p.lineno(-1)}. Expected {function.parameters[global_context.param_counter.top()].type}, got {vtype}")
    else:
        print(f"Error, too many parameters on function {function.name}")
    c = global_context.param_counter.pop()
    c += 1
    global_context.param_counter.push(c)


def p_func_call_1(_):
    """func_call_1  : logic_comp check_param func_call_2
                    | epsilon """


def p_func_call_2(_):
    """func_call_2  : ',' logic_comp check_param func_call_2
                    | epsilon """


def p_logic_comp_cuad(_):
    """logic_comp_cuad  : """
    global_context.create_operation_quad(["&&", "||"])


def p_logic_comp(_):
    """logic_comp       : expression logic_comp_cuad logic_comp_1"""


def p_logic_comp_1(_):
    """logic_comp_1     : logic_comp_ops expression logic_comp_cuad logic_comp_1
                        | epsilon"""
    pass


def p_logic_comp_ops(p):
    """logic_comp_ops   : AND
                        | OR"""
    global_context.operations.push(p[1])


# ( EXP ) ( ( '>' | '<' | '==' | '<>' ) ( EXP ) )?
def p_expression(_):
    """ expression      : exp expression_1 """
    global_context.create_operation_quad([">", "<", "<>", "=="])


def p_expression_1(_):
    """expression_1     : comparison_ops exp
                        | epsilon"""


def p_comparison_ops(p):
    """comparison_ops   : '<'
                        | '>'
                        | DIFF
                        | EQUAL """
    global_context.operations.push(p[1])


def p_exp_cuad(_):
    """exp_cuad   : """
    global_context.create_operation_quad(["+", "-"])


# TERMINO ( ( '+' | '-' ) TERMINO )*
def p_exp(_):
    """exp      : termino exp_cuad exp_1 """


def p_exp1(_):
    """exp_1    : exp_2 termino exp_cuad exp_1
                | epsilon"""


def p_exp_2(p):
    """exp_2    : '+'
                | '-' """
    p[0] = p[1]
    global_context.operations.push(p[1])


def p_termino_vp(_):
    """termino_vp    : """
    global_context.create_operation_quad(["*", "/"])


# FACTOR ( ( '*' | '/' ) FACTOR )*
def p_termino(_):
    """termino      : factor termino_vp termino_1 """


def p_termino_1(_):
    """termino_1    : termino_2 factor termino_vp termino_1
                    | epsilon """


def p_termino_2(p):
    """termino_2    : '*'
                    | '/' """
    p[0] = p[1]
    global_context.operations.push(p[1])


def p_remove_false_bottom(_):
    """remove_false_bottom  : """
    global_context.operations.remove_separator()


def p_add_false_bottom(_):
    """add_false_bottom     : """
    global_context.operations.add_separator()


def p_factor(_):
    """factor       : '(' add_false_bottom logic_comp remove_false_bottom ')'
                    | factor_1 factor_2"""


def p_factor_1(p):
    """factor_1     : '+'
                    | '-'
                    | epsilon """
    p[0] = p[1]


def p_push_const(p):
    """push_const   : """
    operand_type = avail.get_const_type(p[-1])
    global_context.operands.push(p[-1])
    global_context.types.push(operand_type)


def p_factor_2(_):
    """factor_2     : var_cte push_const
                    | var"""


def p_push_id(p):
    """push_id  :   """
    var = global_context.get_variable(p[-1])
    if not var:
        print(f'Error de sintaxis. Variable {p[-1]} no declarada en linea {p.lineno(-1)}')
    global_context.operands.push(var.direction)
    global_context.types.push(var.type)


def p_var(_):
    """var      : ID push_id var_1"""


def p_check_dim(_):
    """check_dim    : """
    # TODO has dims?


def p_check_logic_type(_):
    """check_logic_type :"""
    # TODO revisar el tipo de logic_comp (numerico?)


def p_var_1(_):
    """var_1    : '(' func_call_1 ')'
                | '[' check_dim logic_comp check_logic_type  ']' var_call_dim
                | epsilon"""


def p_var_call_dim(_):
    """var_call_dim : '[' logic_comp ']'
                    | epsilon"""


def p_bloque(_):
    """bloque   : statement bloque
                | epsilon"""
    pass


def p_epsilon(_):
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
var int: a, xyz[20] ,b;
bool: t, f;

function int hello (float x, float y, int re, int be) {
    a = 1;
    b = 2;
    t = true;
    f = false;
}

function void there (int a, int b) {
    a = 1;
    b = a + 10;
}

main ()
var int: x, c, d, y, ren, col, dev[10][2], ted[19];
    float: xx, yy;
    dataFrame: myData, frame;
{
    a = d + c;
    x = (a + c) * d / d;
    if (b > c) then {
        t = f && f;
        t = true;
    } else {
        t = f || f;
    }

 
    load(myData, "miRuta", ren, col);
   

    while (x > c) do {
        t = b + a;
    }

    hello(xx,yy, x + c, c + x);

    from a = a to b do {
        b = x + c;
    }

    ted[10] = 5;

    write(xx, yy, x);

    load(frame, "i", x, y);
    
    return (a);
}
"""
    # dev[2][1] = 10;
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

# data = '''
# program patito;
# var float: x, y, z;
# main() {
#     write(x,y,z);
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

# for k, v in global_context.function_table.table.items():
#     print(v.__str__())

# print(global_context.types)
# print(global_context.operands)
# print(global_context.operations)

# quads display
for quad in range(len(global_context.quadruples)):
    print(quad, global_context.quadruples[quad])

# print(global_context.get_dimensions('d'))

# for func in global_context.function_table.table.values():
#     print(func.name, func.count_vars())

for _, function in global_context.function_table.table.items():
    print(function.name)
    for var in function.variables.table.values():
        print(f"{var.name}, {[dim.upper_bound for dim in var.dimensions]}, {var.size}, {var.direction}")
