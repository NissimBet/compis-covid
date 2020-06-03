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
from .lexer import tokens, literals
from .Quadruple import Quadruple

from .DataUtils import ParsingContext
from .Variable import Variable

from compiler.AVAIL import avail

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
    global_context.end_function(False)
    global_context.create_quad(Quadruple.OperationType.END_PROG, "", "", "")


def p_programa_1(_):
    """programa_1   : vars goto_main programa_2
                    | goto_main programa_2 """


def p_programa_2(_):
    """programa_2   : function programa_2
                    | epsilon"""


# var (tipo : lista_id ;)+
def p_vars(_):
    """vars         : VAR vars_1 """


def p_set_var_type(p):
    """set_var_type : """
    global_context.set_type(p[-1])


def p_vars_1(_):
    """vars_1       : tipo set_var_type ':' lista_id ';' vars_2 """


def p_vars_1_error(p):
    """vars_1       : tipo set_var_type ':' lista_id error ';' vars_2 """
    print("Error de sintaxis en la declaración de variables. Línea ",
          p.lineno(5), ", Posición", p.lexpos(5))


def p_vars_2(_):
    """vars_2       : vars_1
                    | epsilon """


def p_declare_var(p):
    """declare_var  : """
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
    """id_completo      : ID push_dim_var id_completo_1"""
    p[0] = p[1], p[2]


def p_push_dim_var(p):
    """push_dim_var     : """
    var = global_context.get_variable(p[-1])
    global_context.types.push(var.type)
    global_context.operands.push(var.direction)


def p_id_completo_1(p):
    """id_completo_1    :  dimension
                        | epsilon"""
    p[0] = p[1]


def p_id_completo_1_error(_):
    """id_completo_1    : error """
    print("Syntax error while declaring variable dimensions.")


def p_verif_dim(_):
    """verif_dim : """
    direc = global_context.operands.pop()
    direc_type = global_context.types.pop()
    var = global_context.get_variable(avail.get_val_from_dir(direc))

    if len(var.dimensions) == 0:
        print(f"Error. variable {var.name} no tiene dimensiones.")

    dim = 1
    global_context.dimensions.push((var.name, dim))
    global_context.operations.add_separator()


def p_crear_quad_ver(_):
    """crear_quad_ver   :"""
    global_context.create_first_dim_access_quads()


# [ num_var ] {0, 2}
def p_dimension(p):
    """dimension    : '[' verif_dim logic_comp crear_quad_ver  ']' dimension_1 """
    global_context.create_dimension_final_quads()
    global_context.operations.remove_separator()
    p[0] = (p[2], p[5])


def p_handle_matrix(_):
    """handle_matrix    : """
    global_context.create_second_dim_access_quads()


def p_dimension_1(p):
    """dimension_1  : '[' logic_comp handle_matrix ']'
                    | epsilon """
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
    global_context.jumpStack.add_separator()
    if not global_context.declare_function(p[-1], None):
        print(
            f'Error de Sintaxis en declacion de funciones. Linea {p.lineno(-1)}. Funcion "{p[-1]}" ya esta declarada')


# function return_type ID ( parameters? ) vars? { bloque? }
def p_function(_):
    """function     : FUNCTION return_type ID declare_func '(' function_1 ')' function_2 '{' bloque '}' """
    while i := global_context.return_pos.pop():
        global_context.fill_quad(i)
    global_context.jumpStack.remove_separator()
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
                    | std_methods
                    | func_call
                    | return
                    | read
                    | write
                    | load"""


def p_check_variable(p):
    """check_variable   : """
    if not global_context.is_variable_declared(p[-1][0]):
        print(
            f'Error de Sintaxis. Error de asignacion en linea {p.lineno(-1)}. Variable no declarada {p[-1][0]}')


# ID_COMPLETO '=' EXPRESSION
def p_assignment(p):
    """assignment   : id_completo check_variable '=' logic_comp """
    operand_type = global_context.types.pop()
    operand_name = global_context.operands.pop()

    # if global_context.operands.top() is not None:
    assigned = global_context.operands.pop()
    assigned_type = global_context.types.pop()
    # else:
    #     assigned = global_context.get_variable(p[1][0]).direction
    #     assigned_type = global_context.get_variable(p[1][0]).type

    global_context.create_quad(
            Quadruple.OperationType.ASSIGN,
            f"({operand_name})" if operand_type == "pointer" else operand_name,
            "",
            f"({assigned})" if assigned_type == "pointer" else assigned)
    # print(f"Assign to {p[1][0]}, {p[4]}")


def p_assignment_error(p):
    """assignment   : id_completo check_variable '=' error """
    print(f"Error de Sintaxis. Linea {p.lineno(4)}. Asignacion incompleta")


# return ( EXP )
def p_return(p):
    """return   : RETURN '(' logic_comp ')' """
    function = global_context.get_function()
    exp_type = global_context.types.pop()
    exp_val = global_context.operands.pop()
    global_context.create_quad(Quadruple.OperationType.ASSIGN, exp_val, "", str(function.return_dir))
    global_context.create_quad(Quadruple.OperationType.GOTO, "", "", "")
    global_context.return_pos.push(global_context.quad_counter)
    if exp_type != function.return_type:
        print(
            f"Error, wrong return type. Expecting {function.return_type} on function {function.name}")


def p_set_func(p):
    """set_func     :"""
    global_context.operations.add_separator()
    global_context.func_calls.push(p[-1])


def p_check_read_param(p):
    """check_read_param  : """
    var = global_context.get_variable(p[-1][0])
    if var:
        global_context.create_quad(
            Quadruple.OperationType.READ, "", "", var.direction)
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

    global_context.create_quad(Quadruple.OperationType.WRITE,
                               "",
                               "",
                               f"({var_name})" if var_type == "pointer" else var_name)


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
        # print('nombres', num_lines_var_name, num_vars_var_name)
        var = global_context.get_variable(var_name)
        num_lines = global_context.get_variable(num_lines_var_name)
        num_vars = global_context.get_variable(num_vars_var_name)

        if var and num_lines and num_vars:
            if var.type == "dataFrame":
                if num_lines.type == "int" and num_vars.type == "int":
                    global_context.create_quad(
                        Quadruple.OperationType.FILE_SEARCH, path, "", str(var.direction))
                    global_context.create_quad(
                        Quadruple.OperationType.LINES, str(var.direction), "", str(num_lines.direction))
                    global_context.create_quad(
                        Quadruple.OperationType.COLS, str(var.direction), "", str(num_vars.direction))
                else:
                    if num_lines.type == "int":
                        print(
                            f"ERROR in line {p.lineno(7)}. Expected int, got {num_lines.type}")
                    if num_vars.type == "int":
                        print(
                            f"ERROR in line {p.lineno(9)}. Expected int, got {num_vars.type}")
            else:
                print(
                    f"ERROR in line {p.lineno(3)}. Expected type dataFrame, got {var.type}")
        else:
            if not var:
                print(
                    f"ERROR in line {p.lineno(3)}. Variable not declared {p[3]}")
            if not num_lines:
                print(
                    f"ERROR in line {p.lineno(7)}. Variable not declared {p[7]}")
            if not num_vars:
                print(
                    f"ERROR in line {p.lineno(9)}. Variable not declared {p[9]}")
    except IndexError:
        print(f"ERROR in line {p.lineno(0)}. Too little variables provided")


def p_declare_main(_):
    """declare_main : """
    global_context.declare_function('main', 'void')
    global_context.fill_quad()


def p_main(_):
    """main     : MAIN declare_main '(' ')' main_1 '{' bloque '}'  """
    global_context.end_function(False)


def p_main_1(_):
    """main_1   : vars
                | epsilon """
    pass


def p_logic_comp_check(p):
    """logic_comp_check : """
    if not global_context.types.top() == "bool":
        print(
            f"Type Error. Se esperaba un valor booleano en linea {p.lineno(-1)}")
    else:
        operand = global_context.operands.pop()
        operand_type = global_context.types.pop()
        global_context.create_quad(
            Quadruple.OperationType.GOTO_FALSE, operand, "", "")
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
        print(
            f"Type Error. Se esperaba un valor booleano en linea {p.lineno(-1)}")
    else:
        operand = global_context.operands.pop()
        operand_type = global_context.types.pop()
        global_context.create_quad(
            Quadruple.OperationType.GOTO_FALSE, operand, "", "")
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
        print(
            f"Syntax Error. Variable {p[-1][0]} not declared in line {p.lineno(-1)}")


def p_for_assign(_):
    """for_assign   : """
    operand_type = global_context.types.pop()
    operand_name = global_context.operands.pop()
    assigned_type = global_context.types.top()
    assigned = global_context.operands.top()
    # assigned = global_context.get_variable(p[1][0])
    # print(assigned, operand_name)
    global_context.create_quad(
        Quadruple.OperationType.ASSIGN, operand_name, "", assigned)


def p_for_compare(_):
    """for_compare  : """
    global_context.create_jump()
    # print(global_context.operands, global_context.operations)
    right_operand = global_context.operands.pop()
    right_type = global_context.types.pop()

    left_operand = global_context.operands.pop()
    left_type = global_context.types.pop()

    operator = "<"
    resultant_type = global_context.semantic_cube.cubo[left_type][right_type][operator]
    if resultant_type:
        result = avail.get_next_local(resultant_type, True, "")

        global_context.create_quad(Quadruple.get_operator_name(
            operator), left_operand, right_operand, result)
        global_context.operands.push(result)
        global_context.types.push(resultant_type)

        # print(global_context.operands, global_context.operations)
        global_context.create_quad(
            Quadruple.OperationType.GOTO_FALSE, result, "", "")
        global_context.create_jump()

        global_context.operands.push(left_operand)
        global_context.types.push(left_type)
        global_context.operands.add_separator()
        global_context.types.add_separator()
    else:
        print(f"Error de sintaxis. Type Error")
    # global_context.operations.push("<")
    # global_context.create_operation_quad(["<"])
    # operand = global_context.operands.pop()
    # op_type = global_context.types.pop()


# desde ID_COMPLETO = EXP to EXP hacer { ESTATUTO* }
def p_no_condition_loop(_):
    """no_condition_loop    : FROM id_completo for_check_id '=' exp for_assign TO exp for_compare DO '{' no_condition_loop_1 '}'  """
    global_context.operands.remove_separator()
    global_context.types.remove_separator()
    operand = global_context.operands.pop()
    operand_type = global_context.types.pop()

    one = avail.get_next_const("int", 1)
    global_context.create_quad(
        Quadruple.OperationType.ADD, operand, one, operand)
    end = global_context.jumpStack.pop()
    start = global_context.jumpStack.pop()
    # print("End of for loop", global_context.operands)
    global_context.create_quad(Quadruple.OperationType.GOTO, "", "", start + 1)
    global_context.fill_quad(end)


def p_no_condition_loop_1(_):
    """no_condition_loop_1  : bloque
                            | epsilon """


# def p_num_var(p):
#     """ num_var     : ID
#                     | CTE_I
#                     | CTE_F """
#     # print("num var", p[1])
#     p[0] = p[1]


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
    """std_methods  : mean_func
                    | mode_func
                    | variance_func
                    | GAMMA
                    | graph_func
                    | NORMAL_GRAPH
                    | cov_func
                    | scatter_func
    """
    p[0] = p[1]


def p_mean_func(p):
    """mean_func    : MEAN '(' ID ',' logic_comp ',' ID ')' """
    frame_var = global_context.get_variable(p[3])
    index_var = global_context.operands.pop()
    index_type = global_context.types.pop()
    res_var = global_context.get_variable(p[7])

    if frame_var.type != "dataFrame":
        print(f"Type Error. Expected dataFrame, got {frame_var.type}")
    if index_type != "int":
        print(f"Error. Expected integer, got {index_type}")
    if res_var.type != "float":
        print(f"Error. Expected float, got {res_var.type}")

    global_context.create_quad(Quadruple.OperationType.MEAN,
                               str(frame_var.direction),
                               str(index_var),
                               str(res_var.direction))


def p_mode_func(p):
    """mode_func    : MODE '(' ID ',' logic_comp ',' ID ')' """
    frame_var = global_context.get_variable(p[3])
    index_var = global_context.operands.pop()
    index_type = global_context.types.pop()
    res_var = global_context.get_variable(p[7])

    if frame_var.type != "dataFrame":
        print(f"Type Error. Expected dataFrame, got {frame_var.type}")
    if index_type != "int":
        print(f"Error. Expected integer, got {index_type}")
    if res_var.type != "float":
        print(f"Error. Expected float, got {res_var.type}")

    global_context.create_quad(Quadruple.OperationType.MODE,
                               str(frame_var.direction),
                               str(index_var),
                               str(res_var.direction))


def p_variance_func(p):
    """variance_func    : VARIANCE '(' ID ',' logic_comp ',' ID ')' """
    frame_var = global_context.get_variable(p[3])
    index_var = global_context.operands.pop()
    index_type = global_context.types.pop()
    res_var = global_context.get_variable(p[7])

    if frame_var.type != "dataFrame":
        print(f"Type Error. Expected dataFrame, got {frame_var.type}")
    if index_type != "int":
        print(f"Error. Expected integer, got {index_type}")
    if res_var.type != "float":
        print(f"Error. Expected float, got {res_var.type}")

    global_context.create_quad(Quadruple.OperationType.VARIANCE,
                               str(frame_var.direction),
                               str(index_var),
                               str(res_var.direction))


def p_graph_func(p):
    """graph_func    : GRAPH '(' ID ',' logic_comp ')' """
    frame_var = global_context.get_variable(p[3])
    index_var = global_context.operands.pop()
    index_type = global_context.types.pop()

    if frame_var.type != "dataFrame":
        print(f"Type Error. Expected dataFrame, got {frame_var.type}")
    if index_type != "int":
        print(f"Error. Expected integer, got {index_var.type}")

    global_context.create_quad(Quadruple.OperationType.BAR,
                               str(frame_var.direction),
                               str(index_var),
                               "")


def p_scatter_func(p):
    """scatter_func  : SCATTER '(' ID ',' logic_comp ',' logic_comp ')' """
    frame_var = global_context.get_variable(p[3])

    y_index_var = global_context.operands.pop()
    y_index_type = global_context.types.pop()

    x_index_var = global_context.operands.pop()
    x_index_type = global_context.types.pop()

    if frame_var.type != "dataFrame":
        print(f"Type Error. Expected dataFrame, got {frame_var.type}")
    if x_index_type != "int":
        print(f"Error. Expected integer, got {x_index_type}")
    if y_index_type != "int":
        print(f"Error. Expected integer, got {y_index_type}")

    global_context.create_quad(Quadruple.OperationType.SCATTER,
                               str(frame_var.direction),
                               str(x_index_var),
                               str(y_index_var))


def p_cov_func(p):
    """cov_func    : COV '(' ID ',' logic_comp ',' ID ')' """
    frame_var = global_context.get_variable(p[3])
    index_var = global_context.operands.pop()
    index_type = global_context.types.pop()
    res_var = global_context.get_variable(p[7])

    if frame_var.type != "dataFrame":
        print(f"Type Error. Expected dataFrame, got {frame_var.type}")
    if index_type != "int":
        print(f"Error. Expected integer, got {index_var.type}")
    if res_var.type != "float":
        print(f"Type Error. Expected dataFrame, got {frame_var.type}")

    global_context.create_quad(Quadruple.OperationType.COV,
                               str(frame_var.direction),
                               str(index_var),
                               str(res_var.direction))


def p_called_func(p):
    """called_func  : """
    f_name = p[-1]
    if f_name in global_context.function_table.table:
        global_context.operations.add_separator()
        global_context.func_calls.push(f_name)
        global_context.param_counter.push(0)
        function_size = global_context.function_table.function(f_name).vars

        global_context.create_quad(Quadruple.OperationType.ERA, "", "", f_name)
    else:
        print(
            f"Syntax Error, function not defined {f_name} in line {p.lineno(-1)}")


def p_end_func_call(p):
    """end_func_call    :"""
    f_name = global_context.func_calls.pop()
    f_params = global_context.param_counter.pop()
    global_context.operations.remove_separator()

    global_context.create_quad(Quadruple.OperationType.GO_SUB, "", "",
                               global_context.function_table.function(f_name).quad_number)

    function = global_context.function_table.function(f_name)
    if function and function.return_type != "void":
        temp = avail.get_next_local(function.return_type, True, function.name)
        global_context.create_quad(Quadruple.OperationType.ASSIGN, str(function.return_dir), "", temp)
        global_context.operands.push(temp)
        global_context.types.push(function.return_type)

    if len(global_context.function_table.function(f_name).parameters) != f_params:
        print(
                f"Syntax Error. Function {f_name} missing parameters, expected {len(global_context.function_table.function(f_name).parameters)}, got {f_params}")


def p_func_call(p):
    """func_call    : ID called_func '(' func_call_1 ')' end_func_call """
    p[0] = p[1]


def p_check_param(p):
    """check_param : """
    function_name = global_context.func_calls.top()
    function = global_context.function_table.function(function_name)
    if global_context.param_counter.top() < len(function.parameters):
        vtype = global_context.types.pop()
        var = global_context.operands.pop()
        if vtype == function.parameters[global_context.param_counter.top()].type:
            param_counter = global_context.param_counter.top()
            param_dir = function.parameters[param_counter].direction
            # print(function.parameters[param_counter].direction)
            global_context.create_quad(
                Quadruple.OperationType.PARAMETER, var, "", param_dir)
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
    func = global_context.function_table.function(p[-1])
    if not var and not func:
        print(
            f'Error de sintaxis. Variable {p[-1]} no declarada en linea {p.lineno(-1)}')
    else:
        if var:
            global_context.operands.push(var.direction)
            global_context.types.push(var.type)
        elif func:
            p_called_func(p)


def p_var(_):
    """var      : ID push_id var_1
                | std_methods """


def p_var_1(_):
    """var_1    : '(' func_call_1 ')' end_func_call
                | dimension
                | epsilon"""


def p_bloque(_):
    """bloque   : statement bloque
                | epsilon"""
    while (i := global_context.operands.top()) != global_context.operands.false_bottom and not global_context.operands.is_empty:
        global_context.operands.pop()
    while (i := global_context.types.top()) != global_context.types.false_bottom and not global_context.types.is_empty:
        global_context.types.pop()


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

logging.basicConfig(
    level=logging.DEBUG,
    filemode="w",
    filename="../parselog.txt")
