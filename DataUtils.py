# NO TENGO NI IDEA SI DEBERIAMOS HACERLO ASI
# HAZ DE CUENTA QUE ES UN SUPER EARLY DRAFT
from typing import Dict, List, Tuple


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


class Function(object):
    name: str
    return_type: str
    parameters: List[Variable]
    variables: VariableTable

    def __init__(self, name: str,
                 return_type: str,
                 parameters: List[Variable]):
        self.name = name
        self.return_type = return_type
        self.parameters = parameters
        self.variables = VariableTable()

    def add_variable(self, var: Variable):
        if self.variables.declare_variable(var):
            return True
        print(f"Error, variable {var.name} declared on function {self.name}")
        return False

    def set_parameters(self, parameters: List[Variable]):
        self.parameters = parameters

    def add_parameter(self, var: Variable):
        self.parameters.append(var)

    def __str__(self):
        return f"{self.return_type} Function {self.name}({[pname.name for pname in self.parameters]}) vars: {[(v.name, v.dimesions) for k, v in self.variables.table.items()]} "


class FunctionTable(object):
    def __init__(self):
        self.table: Dict[str, Function] = {}

    def declare_function(self, func_name: str, return_type: any) -> bool:
        if func_name not in self.table:
            self.table[func_name] = Function(name=func_name,
                                             return_type=return_type,
                                             parameters=[])
            print("Declared Function", func_name)
            return True
        return False

    def set_parameters(self, func_name: str, parameters: List[Variable]):
        if func_name in self.table:
            self.table[func_name].set_parameters(parameters)
            return True
        return False

    def add_parameter(self, func_name: str, param: Variable):
        if func_name in self.table:
            self.table[func_name].add_parameter(param)
            return True
        return False

    def declare_variable(self, func_name: str, var: Variable) -> bool:
        if not self.table[func_name].variables.is_variable_defined(var.name):
            self.table[func_name].add_variable(var)
            print("Added ", var)
            return True
        return False


class ParsingContext(object):
    function: str
    var_type: str

    def __init__(self):
        self.function = ''
        self.var_type = ''

    def set_type(self, var_type: str):
        self.var_type = var_type

    def set_function(self, name: str):
        self.function = name

    def __str__(self):
        return "({}, {})".format(self.function, self.var_type)
