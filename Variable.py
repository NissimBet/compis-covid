from typing import Tuple, Dict


class Variable(object):
    type: str
    name: str
    value: any
    dimesions: Tuple[int, int]

    def __init__(self, variable_type: str, name: str, dimensions: Tuple[int, int] = [None, None]):
        self.type = variable_type
        self.name = name
        self.dimesions = dimensions

    def __str__(self):
        return f'({self.name}, {self.type})'


class VariableTable(object):
    table: Dict[str, Variable]

    def __init__(self):
        self.table = {}

    def declare_variable(self, var: Variable):
        if var.name not in self.table:
            self.table[var.name] = var
            return True
        return False

    def is_variable_defined(self, name: str):
        return name in self.table




