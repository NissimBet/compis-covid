from typing import Tuple, Dict, List


class Dimension:
    upper_bound: int
    r: int
    m: int

    def __init__(self, u_bound: int):
        self.upper_bound = u_bound

    def __str__(self):
        return f"{self.upper_bound}, {self.m}"


class Variable(object):
    type: str
    name: str
    value: any
    dimensions: List[Dimension]
    size: int
    direction: int

    def __init__(self, variable_type: str, name: str, dimensions: List[int] = [], var_direction: int = -1):
        self.type = variable_type
        self.name = name
        self.direction = var_direction
        self.init_dimensions(dimensions)

    def init_dimensions(self, bounds: List[int]):
        if not bounds or len(bounds) == 0:
            self.dimensions = []
            self.size = 1
            return

        r = 1
        offset = 0
        dimensions: List[Dimension] = []
        for index in range(len(bounds)):
            r = r * (bounds[index])
            dimension = Dimension(bounds[index])
            dimension.r = r
            dimensions.append(dimension)

        self.size = r
        dimensions[-1].m = r

        for index in range(len(bounds)):
            m = dimensions[index - 1].m // (bounds[index])
            dimensions[index].m = m

        dimensions[-1].m = - offset

        self.dimensions = dimensions

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
    
    def get_dimensions(self, name: str):
        length = len(self.table[name].dimensions)
        if length == 1:
            return [self.table[name].dimensions[0].upper_bound]
        elif length == 2:
            return [self.table[name].dimensions[0].upper_bound, self.table[name].dimensions[1].upper_bound]
        else:
            return None

    def set_direction(self, var_name: str, direction: int):
        if var_name in self.table:
            self.table[var_name].direction = direction
