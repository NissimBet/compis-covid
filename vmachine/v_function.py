from typing import Any
from .v_memory import Memory


class VMFunction:
    def __init__(self, name: str = ""):
        self.name = name
        self.__local_memory = Memory(5000)
        self.__temp_memory = Memory(6000)

    def get_var(self, var_direction: int):
        if 5000 <= var_direction < 6000:
            return self.__local_memory.get_var(var_direction)
        elif 6000 <= var_direction < 7000:
            return self.__temp_memory.get_var(var_direction)

    def assign_var(self, var_direction: int, value: Any):
        if 5000 <= var_direction < 6000:
            return self.__local_memory.assign_var(var_direction, value)
        elif 6000 <= var_direction < 7000:
            return self.__temp_memory.assign_var(var_direction, value)

    def era(self, var_type: str, size: int,  is_temp: bool):
        if is_temp:
            self.__temp_memory.initialize_var_type(var_type, size)
        else:
            self.__local_memory.initialize_var_type(var_type, size)

    def pass_param(self, param_dir: int, param_value: Any):
        self.__local_memory.assign_var(param_dir, param_value)

    def get_vars(self):
        return self.__local_memory.get_vars(), self.__temp_memory.get_vars()
