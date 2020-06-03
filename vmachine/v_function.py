from typing import Any
from .v_memory import Memory


class VMFunction:
    def __init__(self, name: str = ""):
        self.name = name
        self.__local_memory = Memory(3000)
        self.__temp_memory = Memory(8000)

    def get_var(self, var_direction: int):
        """
        Funcion que regresa el valor de una variable en memoria de la funcion

        :param var_direction: direccion de la memoria
        :return: El valor en la direccion
        """
        if 3000 <= var_direction < 8000:
            return self.__local_memory.get_var(var_direction)
        elif 8000 <= var_direction < 9000:
            return self.__temp_memory.get_var(var_direction)

    def assign_var(self, var_direction: int, value: Any):
        """
        Funcio que asigna un valor a una direccion

        :param var_direction: la direccion donde asignar el valor
        :param value: el valor que asignar
        :return: None
        """
        if 3000 <= var_direction < 8000:
            return self.__local_memory.assign_var(var_direction, value)
        elif 8000 <= var_direction < 9000:
            return self.__temp_memory.assign_var(var_direction, value)

    def era(self, var_type: str, size: int,  is_temp: bool):
        """
        Funcion que genera el tamano para una variable de la funcion

        :param var_type: tipo de variable que (allocate)
        :param size: cantidad de direcciones que generar
        :param is_temp: si es una variable temporal o no
        :return:
        """
        if is_temp:
            self.__temp_memory.initialize_var_type(var_type, size)
        else:
            self.__local_memory.initialize_var_type(var_type, size)

    def pass_param(self, param_dir: int, param_value: Any):
        """pasar un valor de parametro a su direccion local"""
        self.__local_memory.assign_var(param_dir, param_value)

    def get_vars(self):
        """regresa las variables locales"""
        return self.__local_memory.get_vars(), self.__temp_memory.get_vars()
