from typing import Dict, List

from Variable import Variable, VariableTable


class Function(object):
    name: str
    return_type: str
    parameters: List[Variable]
    variables: VariableTable
    quad_number: int
    temps_used: int

    def __init__(self, name: str,
                 return_type: str,
                 parameters: List = None,
                 quad_number: int = 0):
        if parameters is None:
            parameters = []
        self.name = name
        self.return_type = return_type
        self.parameters = parameters
        self.variables = VariableTable()
        self.quad_number = quad_number
        self.temps = {}
        self.vars = {}

    def add_variable(self, var: Variable) -> bool:
        if var in self.parameters or self.variables.is_variable_defined(var.name):
            return False
        return self.variables.declare_variable(var)

    def add_parameter(self, var: Variable) -> bool:
        if var in self.parameters or self.variables.is_variable_defined(var.name):
            # print(f'Error, variable {var.name} is already declared in scope')
            return False
        self.parameters.append(var)
        self.variables.declare_variable(var)
        return True

    def count_vars(self):
        var_vals = list(self.variables.table.values())
        var_org: Dict[str, int] = {var.type: 0 for var in var_vals}
        for var in var_vals:
            var_org[var.type] += 1
        self.vars = var_org

    def __str__(self):
        return f"{self.return_type} Function {self.name}({[pname.name for pname in self.parameters]}) vars: {[(v.name, v.dimesions) for k, v in self.variables.table.items()]} "


# TODO Crear los cuadruplos para cada una de las funciones y definir los parametros
class FunctionTable(object):
    def __init__(self):
        self.__table: Dict[str, Function] = {
            # "mean": Function("mean", "float"),
            # "mode": Function("mode", "float"),
            # "variance": Function("variance", "float"),
            # "normal": Function("normal", "float"),
            # "gamma": Function("gamma", "float"),
            # "graph": Function("graph", "float"),
            # "normal_graph": Function("normal_graph", "float"),
            # "cov": Function("cov", "float"),
            # "scatter": Function("scatter", "float"),
        }

    @property
    def table(self):
        return self.__table

    def declare_function(self, func_name: str, return_type: any, quad_num: int = 0) -> bool:
        if func_name not in self.__table:
            self.__table[func_name] = Function(name=func_name,
                                               return_type=return_type,
                                               quad_number=quad_num)
            # print("Declared Function", func_name)
            return True
        return False

    def add_parameter(self, func_name: str, param: Variable) -> bool:
        if func_name in self.__table:
            if self.is_variable_declared(func_name, param.name) and self.is_global(param.name) or \
                    not self.is_variable_declared(func_name, param.name):
                return self.__table[func_name].add_parameter(param)
            else:
                return False
        return False

    def declare_variable(self, func_name: str, var: Variable) -> bool:
        if not self.is_variable_declared(func_name, var.name):
            return self.__table[func_name].add_variable(var)
            # print(f"Added Variable {var} to {func_name}")
        return False

    def is_variable_declared(self, func_name: str, var_name: str) -> bool:
        if func_name in self.__table:
            if self.__table[func_name].variables.is_variable_defined(var_name):
                # print(f"Error, variable {var_name} declared on function {func_name}")
                return True
            if 'global' in self.__table and self.__table['global'].variables.is_variable_defined(var_name):
                # print(f"Error, variable {var_name} declared on function {func_name}")
                return True
        return False

    def get_variable(self, func_name: str, var_name: str) -> Variable:
        if func_name in self.__table:
            if self.__table[func_name].variables.is_variable_defined(var_name):
                return self.__table[func_name].variables.get_variable(var_name)
            if 'global' in self.__table and self.__table['global'].variables.is_variable_defined(var_name):
                return self.__table['global'].variables.get_variable(var_name)
        else:
            return None

    def get_dimensions(self, func_name: str, var_name: str):
        if func_name in self.__table:
            if self.__table[func_name].variables.is_variable_defined(var_name):
                return self.__table[func_name].variables.get_dimensions(var_name)
            if 'global' in self.__table and self.__table['global'].variables.is_variable_defined(var_name):
                return self.__table['global'].variables.get_dimensions(var_name)
        else:
            return None

    def is_global(self, var_name: str):
        return self.__table["global"].variables.is_variable_defined(var_name)

    def is_temp(self, func_name: str, var_name: str):
        return func_name in self.__table and self.__table.get(func_name).variables.is_variable_defined(var_name)

    def function(self, func_name: str):
        return self.__table.get(func_name, None)

    def erase_var_table(self, func_name: str):
        self.__table.get(func_name, None).count_vars()
        self.__table.get(func_name, None).variables.table.clear()
