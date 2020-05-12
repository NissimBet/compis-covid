from typing import List

from CuboSemantico import CuboSemantico
from Stack import Stack
from Quadruple import Quadruple


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

    def __init__(self):
        self.function = Stack()
        self.var_type = ''
        self.quadruples = []
        self.jumpStack = Stack()
        self.operands = Stack()
        self.operations = Stack()
        self.types = Stack()
        self.semantic_cube = CuboSemantico()

    @property
    def quad_counter(self):
        return len(self.quadruples) - 1

    def set_type(self, var_type: str):
        self.var_type = var_type

    def set_function(self, name: str):
        self.function.push(name)

    def create_quad(self, operation: Quadruple.OperationType, mem_location_1: str, mem_location_2, mem_result: str):
        self.quadruples.append(Quadruple(operation, mem_location_1, mem_location_2, mem_result))
        return self.quad_counter

    def fill_quad(self):
        jump_index = self.jumpStack.pop()
        quad_index = self.quad_counter
        try:
            self.quadruples[jump_index].result = quad_index
        except IndexError:
            print(f"Error accediendo indice {jump_index} de la lista de cuadruplos")

    def __str__(self):
        return "({}, {})".format(self.function, self.var_type)


class AVAIL:
    def __init__(self) -> None:
        self.counter = 0

    def get_next(self):
        self.counter = self.counter + 1
        return f"tempvar-{self.counter - 1}"
