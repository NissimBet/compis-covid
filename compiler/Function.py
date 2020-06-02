from typing import Dict, List

from .Variable import Variable, VariableTable


class Function(object):
    name: str                           # Nombre de la funcion
    return_type: str                    # tipo de retorno de la funcion
    return_dir: int                     # direccion donde retornar
    parameters: List[Variable]          # parametros de la funcion
    variables: VariableTable            # tabla de variables de la funcion
    quad_number: int                    # cuadruplo de inicio de la funcion
    temps: Dict[str, int]               # cantidad de temporales en terminos de cantidad de variables por tipo
    vars: Dict[str, int]                # cantidad de no temporales en terminos de cantidad de variables por tipo

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
        self.return_dir = -1
        self.temps = {}
        self.vars = {}

    def add_variable(self, var: Variable) -> bool:
        """declara una variable a la funcion. Regresa si se tuvo exito al declararla"""
        if var in self.parameters or self.variables.is_variable_defined(var.name):
            return False
        return self.variables.declare_variable(var)

    def add_parameter(self, var: Variable) -> bool:
        """Agrega una variable a los parametros de la funcion. Regresa si se agrego con exito"""
        if var in self.parameters or self.variables.is_variable_defined(var.name):
            return False
        self.parameters.append(var)
        return self.variables.declare_variable(var)

    def count_vars(self) -> None:
        """Cuenta la cantidad de variables en la funcion. Genera el diccionario de vars"""
        var_vals = list(self.variables.table.values())
        var_org: Dict[str, int] = {var.type: 0 for var in var_vals}
        for var in var_vals:
            var_org[var.type] += var.size
        self.vars = var_org

    def __str__(self):
        return f"{self.return_type} Function {self.name}({[pname.name for pname in self.parameters]}) vars: {[(v.name, v.dimesions) for k, v in self.variables.table.items()]} "


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
        """Agrega una funcion a la tabla de funciones. Regresa si se pudo declarar la funcion"""
        if func_name not in self.__table:
            self.__table[func_name] = Function(name=func_name,
                                               return_type=return_type,
                                               quad_number=quad_num)
            return True
        return False

    def add_parameter(self, func_name: str, param: Variable) -> bool:
        """Agrega un parametro a la funcion. Regresa si se pudo agregar el parametro"""
        if func_name in self.__table:
            # Agregar el parametro si la variable esta declarada, pero es global o si no esta declarada
            if self.is_variable_declared(func_name, param.name) and self.is_global(param.name) or \
                    not self.is_variable_declared(func_name, param.name):
                return self.__table[func_name].add_parameter(param)
        return False

    def declare_variable(self, func_name: str, var: Variable) -> bool:
        """Le declara una variable a la funcion. Regresa si se pudo declarar la variable"""
        if not self.is_variable_declared(func_name, var.name):
            return self.__table[func_name].add_variable(var)
        return False

    def is_variable_declared(self, func_name: str, var_name: str) -> bool:
        """Regresa si la variable ya esta declarada en la funcion dada"""
        if func_name in self.__table:
            if self.__table[func_name].variables.is_variable_defined(var_name):
                return True
            if 'global' in self.__table and self.__table['global'].variables.is_variable_defined(var_name):
                return True
        return False

    def get_variable(self, func_name: str, var_name: str) -> Variable:
        """Busca y Regresa una variable de la funcion. Regresa None si no se encuentra la variable"""
        if func_name in self.__table:
            if self.__table[func_name].variables.is_variable_defined(var_name):
                return self.__table[func_name].variables.get_variable(var_name)
            if 'global' in self.__table and self.__table['global'].variables.is_variable_defined(var_name):
                return self.__table['global'].variables.get_variable(var_name)
        else:
            return None

    def get_dimensions(self, func_name: str, var_name: str) -> List[int]:
        """Regresa las dimensiones de una variable dentro de una funcion"""
        if func_name in self.__table:
            if self.__table[func_name].variables.is_variable_defined(var_name):
                return self.__table[func_name].variables.get_dimensions(var_name)
            if 'global' in self.__table and self.__table['global'].variables.is_variable_defined(var_name):
                return self.__table['global'].variables.get_dimensions(var_name)
        return []

    def is_global(self, var_name: str) -> bool:
        """regresa si la funcion esta declarada globalmente"""
        return "global" in self.__table and self.__table["global"].variables.is_variable_defined(var_name)

    def function(self, func_name: str) -> Function:
        """Regresa una funcion de la tabla"""
        return self.__table.get(func_name, None)

    def erase_var_table(self, func_name: str) -> None:
        """Borra la tabla de variables de una funcion, calculando el tamano de la funcion al mismo tiempo"""
        self.__table.get(func_name, None).count_vars()
        self.__table.get(func_name, None).variables.table.clear()
