from typing import Dict, Any, Union, List
from .v_variables import data_types, get_type


class Memory:
    # direccion base de la memoria
    __base_dir: int
    # estructura de memoria
    __memory: Dict[str, Dict[str, Union[int, List[Any]]]]

    def __init__(self, base: int):
        self.__base_dir = base
        self.__memory = {
            d_type[0]: {"base": d_type[1], "values": []} for d_type in data_types
        }

    @property
    def base(self):
        return self.__base_dir

    def get_var_index(self, direction: int, var_type: str = ""):
        if not var_type:
            var_type = get_type(direction)
        return direction - self.__base_dir - self.__memory.get(var_type).get("base")

    def get_var(self, variable_dir: int):
        try:
            var_type = get_type(variable_dir)
            var_index = self.get_var_index(variable_dir, var_type)
            variable = self.__memory.get(var_type).get("values")[var_index]
            if variable is None:
                print(variable, var_index, var_type)
                print(f"Variable not initialized {variable_dir}")
            else:
                return variable
        except IndexError:
            print(f"Error accessing element {variable_dir} in memory")

    def assign_var(self, variable_dir: int, value: Any):
        try:
            var_type = get_type(variable_dir)
            var_index = self.get_var_index(variable_dir, var_type)
            self.__memory.get(var_type).get("values")[var_index] = value
        except IndexError:
            print(f"Error assigning to element {variable_dir} in memory.")

    def push_var(self, variable_dir: int, value: Any):
        try:
            var_type = get_type(variable_dir)
            self.__memory.get(var_type).get("values").append(value)
        except IndexError:
            print(f"Error assigning to element {variable_dir} in memory")

    def initialize_var_type(self, var_type: str, size: int):
        self.__memory.get(var_type)["values"] = [None] * size

    def get_vars(self):
        return self.__memory.values()

    def clear(self):
        self.__memory.clear()
