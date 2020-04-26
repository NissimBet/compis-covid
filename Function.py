from typing import Dict, List

from Variable import Variable, VariableTable


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

    def add_variable(self, var: Variable) -> bool:
        if self.variables.declare_variable(var):
            return True

        return False

    def set_parameters(self, parameters: List[Variable]) -> bool:
        for parameter in parameters:
            status = self.add_parameter(parameter)
            if not status:
                print(f'Error, variable {parameter.name} is already declared in scope')
                return False
        return True

    def add_parameter(self, var: Variable) -> bool:
        if var in self.parameters or self.variables.is_variable_defined(var.name):
            print(f'Error, variable {var.name} is already declared in scope')
            return False
        self.parameters.append(var)
        self.variables.declare_variable(var)
        return False

    def __str__(self):
        return f"{self.return_type} Function {self.name}({[pname.name for pname in self.parameters]}) vars: {[(v.name, v.dimesions) for k, v in self.variables.table.items()]} "


class FunctionTable(object):
    def __init__(self):
        self.__table: Dict[str, Function] = {}

    @property
    def table(self):
        return self.__table

    def declare_function(self, func_name: str, return_type: any) -> bool:
        if func_name not in self.__table:
            self.__table[func_name] = Function(name=func_name,
                                               return_type=return_type,
                                               parameters=[])
            # print("Declared Function", func_name)
            return True
        return False

    def set_parameters(self, func_name: str, parameters: List[Variable]) -> bool:
        if func_name in self.__table:
            self.__table[func_name].set_parameters(parameters)
            return True
        return False

    def add_parameter(self, func_name: str, param: Variable) -> bool:
        if func_name in self.__table:
            self.__table[func_name].add_parameter(param)
            return True
        return False

    def declare_variable(self, func_name: str, var: Variable) -> bool:
        if not self.is_variable_declared(func_name, var.name):
            self.__table[func_name].add_variable(var)
            # print(f"Added Variable {var} to {func_name}")
            return True
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
