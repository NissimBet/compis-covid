from typing import List

from Stack import Stack
from Quadruple import Quadruple


class ParsingContext(object):
    function: Stack
    var_type: str
    quadruples: List[Quadruple]
    quadCounter: int

    def __init__(self):
        self.function = Stack()
        self.var_type = ''
        self.quadruples = []

    @property
    def quad_counter(self):
        return len(self.quadruples)

    def set_type(self, var_type: str):
        self.var_type = var_type

    def set_function(self, name: str):
        self.function.push(name)

    def create_quad(self, operation: Quadruple.OperationType, mem_location_1: str, mem_location_2, mem_result: str):
        self.quadruples.append(Quadruple(operation, mem_location_1, mem_location_2, mem_result))

    def __str__(self):
        return "({}, {})".format(self.function, self.var_type)
