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

    def init_dimensions(self, bounds: List[int]) -> None:
        """
        Funcion que realiza la inicializacion de las dimensiones de la variable

        :param bounds: la lista de los limites superiores para cada dimension
        :return: None
        """
        if not bounds or len(bounds) == 0:
            self.dimensions = []
            self.size = 1
            return

        r = 1
        offset = 0
        dimensions: List[Dimension] = []
        # para cada limite superior, realizar el calculo de la R y crear una dimension para agregar sobre la variable
        for index in range(len(bounds)):
            r = r * (bounds[index] + 1)
            dimension = Dimension(bounds[index])
            dimension.r = r
            dimensions.append(dimension)

        # el tamano total de la variable es la r final / m0
        self.size = r
        # asignar el m0 al ultimo valor
        dimensions[-1].m = r

        # segunda pasada para calcular el tamano de cada dimension
        for index in range(len(bounds)):
            m = dimensions[index - 1].m // (bounds[index] + 1)
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
        """Declarar una variable en la tabla. Regresa si se la declaracion es exitosa"""
        if var.name not in self.table:
            self.table[var.name] = var
            return True
        return False

    def is_variable_defined(self, name: str) -> bool:
        """Regresa si la variable ya esta definida"""
        return name in self.table

    def get_variable(self, name: str) -> Variable:
        """Regresa una variable de la tabla o None si no se encontro"""
        return self.table.get(name, None)
    
    def get_dimensions(self, name: str) -> List[int]:
        """Regresa la lista de dimensiones"""
        if name in self.table:
            return [dim.upper_bound for dim in self.table.get(name).dimensions]
        return []

    def set_direction(self, var_name: str, direction: int) -> None:
        """asigna la direccion virtual de una variable"""
        if var_name in self.table:
            self.table[var_name].direction = direction
