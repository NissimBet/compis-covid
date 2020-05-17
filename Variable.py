from typing import Tuple, Dict


class Variable(object):
    type: str
    name: str
    value: any
    dimesions: Tuple[int, int]
    direction: int

    def __init__(self, variable_type: str, name: str, dimensions: Tuple[int, int] = [None, None], var_direction: int = -1):
        self.type = variable_type
        self.name = name
        self.dimesions = dimensions
        self.direction = var_direction

    def __str__(self):
        return f'({self.name}, {self.type})'


class VariableTable(object):
    table: Dict[str, Variable]

    def __init__(self):
        self.table = {}

    def declare_variable(self, var: Variable) -> bool:
        if var.name not in self.table:
            self.table[var.name] = var
            return True
        return False

    def is_variable_defined(self, name: str) -> bool:
        return name in self.table

    def get_variable(self, name: str) -> Variable:
        return self.table.get(name)

    def set_direction(self, var_name: str, direction: int):
        if var_name in self.table:
            self.table[var_name].direction = direction

