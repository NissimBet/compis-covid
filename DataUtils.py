from typing import List, Tuple, Union, Optional

from CuboSemantico import CuboSemantico
from Function import FunctionTable
from Stack import Stack
from Quadruple import Quadruple
from AVAIL import avail
from Variable import Variable


class ParsingContext(object):
    # es de legado, prob hay que cambiarlo
    function: Stack
    var_type: str
    # lista de quadruplos, (no stack por la busqueda)
    quadruples: List[Quadruple]
    # stack de saltos
    jumpStack: Stack

    types: Stack
    operations: Stack
    operands: Stack

    semantic_cube: CuboSemantico()
    function_table: FunctionTable()

    func_calls: Stack
    param_counter: Stack

    def __init__(self):
        self.function = Stack()
        self.var_type = ''
        self.quadruples = []
        self.jumpStack = Stack()
        self.operands = Stack()
        self.operations = Stack()
        self.types = Stack()
        self.semantic_cube = CuboSemantico()
        self.function_table = FunctionTable()
        self.param_counter = Stack()
        self.func_calls = Stack()

    @property
    def quad_counter(self):
        return len(self.quadruples) - 1

    def add_function_parameter(self, var: Variable) -> bool:
        if self.function.top() == "global":
            var.direction = avail.get_next_global(var.type, False, var.name)
        else:
            var.direction = avail.get_next_local(var.type, False, var.name)

        if self.function_table.add_parameter(self.function.top(), var):
            return True
        return False

    def declare_function(self, f_name: str, f_type: Optional[str]) -> bool:
        if f_name not in self.function_table.table:
            quad = self.quad_counter
            self.function_table.declare_function(f_name, f_type if f_type else self.var_type, quad)
            self.set_function(f_name)
            return True
        return False

    def set_type(self, var_type: str):
        self.var_type = var_type

    def set_function(self, name: str):
        self.function.push(name)

    def create_quad(self, operation: Quadruple.OperationType, mem_location_1: str, mem_location_2, mem_result: str):
        self.quadruples.append(Quadruple(operation, mem_location_1, mem_location_2, mem_result))
        return self.quad_counter

    def create_jump(self):
        self.jumpStack.push(self.quad_counter)

    def fill_quad(self, end: int = -1):
        jump_index = end if end != -1 else self.jumpStack.pop()
        quad_index = self.quad_counter
        try:
            self.quadruples[jump_index].result = quad_index + 1
        except IndexError:
            print(f"Error accediendo indice {jump_index} de la lista de cuadruplos")

    def create_operation_quad(self, operations: List[str]):
        if not self.operations.top() in operations:
            return
        right_operand = self.operands.pop()
        right_type = self.types.pop()

        left_operand = self.operands.pop()
        left_type = self.types.pop()

        operator = self.operations.pop()
        resultant_type = self.semantic_cube.cubo[left_type][right_type][operator]
        if resultant_type:
            result = avail.get_next_local(resultant_type, True, "")

            self.create_quad(Quadruple.get_operator_name(operator), left_operand, right_operand, result)
            self.operands.push(result)
            self.types.push(resultant_type)
        else:
            print(f"Error de sintaxis. Type Error")

    def declare_variable(self, var_name: str, dimensions: Tuple[int, int], is_global: bool) -> bool:
        if is_global:
            var_direction = avail.get_next_global(self.var_type, False, var_name)
        else:
            var_direction = avail.get_next_local(self.var_type, False, var_name)

        if not self.function_table.declare_variable(self.function.top(),
                                                    Variable(self.var_type, var_name, dimensions, var_direction)):
            return False
        return True

    def is_variable_declared(self, var_name: str):
        return self.function_table.is_variable_declared(self.function.top(), var_name)

    def get_variable(self, var_name: str):
        return self.function_table.get_variable(self.function.top(), var_name)

    def get_function(self):
        return self.function_table.function(self.function.top())

    def __str__(self):
        return "({}, {})".format(self.function, self.var_type)
