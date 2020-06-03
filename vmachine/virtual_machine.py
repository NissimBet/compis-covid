import sys
import re
from Stack import Stack
from typing import List, Any, Dict

from .v_memory import Memory
from .v_function import VMFunction
from .v_variables import get_scope, get_type, try_cast, convert_dir

import pandas as pd
from matplotlib import pyplot

import os


class VirtualMachine:
    # program counter
    __index_counter: int
    # lista de cuadruplos cargados del .obj
    __quads: List[List[str]]
    # stack de ejecucion de funciones
    __execution_stack: Stack[VMFunction]
    # tabla de funciones recreada
    __function_table: Dict[str, Dict[str, Any]]

    def __init__(self, file_path):
        # memorias de la maquina virtual
        self.__global_memory = Memory(2000)
        self.__global_temps = Memory(18000)
        self.__constants = Memory(15000)
        self.__execution_stack = Stack[VMFunction]()

        self.__index_counter = 0
        self.__index_stack = Stack[int]()
        self.__quads: List[List[str]] = []

        self.__function_table = {}

        self.__context = None

        self.load_file_contents(file_path)

    def execute_quads(self):
        """
        Funcion que ejecuta los cuadruplos cargados  en memoria
        :return:
        """

        # inicializar las variables de cada funcion
        global_func = self.__function_table.get("global")
        for var, size in global_func.get("num_vars").items():
            self.__global_memory.initialize_var_type(var, size)
        for var, size in global_func.get("num_temps").items():
            self.__global_temps.initialize_var_type(var, size)

        function = self.__function_table.get("main")
        function_context = VMFunction("main")
        for var, size in function.get("num_vars").items():
            function_context.era(var, size, False)
        for var, size in function.get("num_temps").items():
            function_context.era(var, size, True)
        self.__execution_stack.push(function_context)

        # ejecutar los cuadruplos en "orden"
        while self.__index_counter < len(self.__quads):
            current_quad = self.__quads[self.__index_counter]
            self.__index_counter = self.load_quad(
                current_quad[0], current_quad[1], current_quad[2], current_quad[3])

    def load_file_contents(self, filename: str):
        """Carga los contenidos de un archivo obj"""
        if os.path.exists(filename):
            with open(filename, "r") as file:
                stop_string = file.readline()
                # CONST TABLE #
                for line in file:
                    if line == stop_string:
                        break
                    else:
                        # separar los datos y eliminar newlines
                        values = line.strip("\r\n").split(',')
                        if len(values) < 2:
                            print(f"Error, malformed pair for constant variables")
                        else:
                            # convertir la direccion del compilador a una de la VM
                            direction = convert_dir(int(values[0]))
                            self.__constants.push_var(
                                direction, try_cast(direction, values[1]))
                # FUNCTION TABLE
                for line in file:
                    if line == stop_string:
                        break
                    else:
                        # separar los datos para cada funcion (nombre, tipo , cuad_inicio , variables locales, variable temporales)
                        values = re.match(
                            r"(\w*),(\w*),(\w*),(\[.*\]),(\[.*\])", line.strip('\r\n'))
                        func_vars = re.findall(r"\(.*?,.*?\)", values.group(4))
                        temp_vars = re.findall(r"\(.*?,.*?\)", values.group(5))

                        # contar la cantidad de variables por tipo de variable
                        num_vars = {}
                        num_temps = {}
                        for func_var in func_vars:
                            var_type = func_var.split(',')
                            num_vars.setdefault(var_type[0].strip(
                                "()'"), int(var_type[1].strip("()'")))
                        for temp_var in temp_vars:
                            temp_type = temp_var.split(',')
                            num_temps.setdefault(temp_type[0].strip(
                                "()'"), int(temp_type[1].strip("()'")))

                        if len(values.groups()) < 5:
                            print(f"Error, malformed fucntion table data")
                        else:
                            # crear una funcion en la tabla de funciones
                            new_function = {
                                "type": values[2],
                                "dir_start": values[3],
                                "num_vars": num_vars,
                                "num_temps": num_temps
                            }
                            self.__function_table.setdefault(
                                values[1], new_function)
                # QUADS
                for line in file:
                    quad = line.strip("\r\n").split(',')
                    if len(quad) < 4:
                        print("Error, malformed quad", quad)
                    else:
                        self.__quads.append(quad)
        else:
            print(f"File {filename} was not found")

    def get_var(self, var_dir: str):
        """Regresa el valor de una variable segun el contexto actual del VM"""
        try:
            # revisar si es un apuntador
            match = re.match(r"\((.*)\).*", var_dir)
            if match:
                # si es apuntador, conseguir direccion de esa direccion
                direction = self.get_var(match.group(1))
            else:
                direction = int(var_dir)
        except ValueError:
            print(f"Provided Direction is not a number format {var_dir}")
            return
        direction = convert_dir(direction)
        var_scope = get_scope(direction)
        if var_scope == "global":
            if 2000 <= direction < 3000:
                return self.__global_memory.get_var(direction)
            elif 18000 <= direction < 19000:
                return self.__global_temps.get_var(direction)
        elif var_scope == "local":
            return self.__execution_stack.top().get_var(direction)
        elif var_scope == "constant":
            return self.__constants.get_var(direction)

    def assign_var(self, var_dir: str, value: Any):
        """Asigna un valor a una direccino de memoria segun el contexto de la direccion"""
        try:
            # revisar si es un apuntador
            match = re.match(r"\((.*)\).*", var_dir)
            if match:
                # si es buscar la direccion correspondiente
                direction = self.get_var(match.group(1))
            else:
                direction = int(var_dir)
        except ValueError:
            print(
                f"Provided Direction is not a number format {var_dir}, cannot assign {value}")
            return
        direction = convert_dir(direction)
        var_scope = get_scope(direction)
        if var_scope == "global":
            if 1000 <= direction < 2000:
                return self.__global_memory.assign_var(direction, value)
            elif 2000 <= direction < 3000:
                return self.__global_temps.assign_var(direction, value)
        elif var_scope == "local":
            self.__execution_stack.top().assign_var(direction, value)
        elif var_scope == "constant":
            self.__constants.assign_var(direction, value)

    def load_quad(self, operation: str, dir1: str, dir2: str, dir3: str):
        # print(operation, dir1, dir2, dir3, sep=",")
        if operation == "SUM":
            var1 = self.get_var(dir1)
            var2 = self.get_var(dir2)
            self.assign_var(dir3, int(var1) + int(var2))
        elif operation == "SUB":
            var1 = self.get_var(dir1)
            var2 = self.get_var(dir2)
            self.assign_var(dir3, int(var1) - int(var2))
        elif operation == "DIV":
            var1 = self.get_var(dir1)
            var2 = self.get_var(dir2)
            self.assign_var(dir3, int(var1) / int(var2))
        elif operation == "MULT":
            var1 = self.get_var(dir1)
            var2 = self.get_var(dir2)
            self.assign_var(dir3, int(var1) * int(var2))
        elif operation == "ASG":
            var1 = self.get_var(dir1)
            self.assign_var(dir3, var1)
        elif operation == "GOTO":
            return int(dir3)
        elif operation == "GOTOV":
            var1 = self.get_var(dir1)
            if var1:
                return int(dir3)
        elif operation == "GOTOF":
            var1 = self.get_var(dir1)
            if not var1:
                return int(dir3)
        elif operation == "LT":
            var1 = self.get_var(dir1)
            var2 = self.get_var(dir2)
            self.assign_var(dir3, int(var1) < int(var2))
        elif operation == "GT":
            var1 = self.get_var(dir1)
            var2 = self.get_var(dir2)
            self.assign_var(dir3, var1 > var2)
        elif operation == "EQ":
            var1 = self.get_var(dir1)
            var2 = self.get_var(dir2)
            self.assign_var(dir3, var1 == var2)
        elif operation == "NEQ":
            var1 = self.get_var(dir1)
            var2 = self.get_var(dir2)
            self.assign_var(dir3, var1 != var2)
        elif operation == "LAND":  # LOGIC AND
            var1 = self.get_var(dir1)
            var2 = self.get_var(dir2)
            self.assign_var(dir3, var1 and var2)
        elif operation == "LOR":  # LOGIC OR
            var1 = self.get_var(dir1)
            var2 = self.get_var(dir2)
            self.assign_var(dir3, var1 or var2)
        elif operation == "GOSUB":  # GOSUB
            self.__index_stack.push(self.__index_counter)
            self.__execution_stack.push(self.__context)
            return int(dir3)
        elif operation == "ERA":  # ERA
            # buscar la funcion de la tabla
            function = self.__function_table.get(dir3)
            # cambiar el contexto actual
            function_context = VMFunction(dir3)
            # crear variables
            for var, size in function.get("num_vars").items():
                function_context.era(var, size, False)
            for var, size in function.get("num_temps").items():
                function_context.era(var, size, True)
            self.__context = function_context
        elif operation == "PARAM":  # PARAM
            var1 = self.get_var(dir1)
            self.__context.pass_param(int(dir3), var1)
        elif operation == "ENDFUNC":  # END FUNC
            self.__execution_stack.pop()
            return self.__index_stack.pop() + 1
        elif operation == "WRITE":  # WRITE
            var3 = self.get_var(dir3)
            print(var3)
        elif operation == "READ":  # READ
            data = input()
            casted_data = try_cast(int(dir3), data)
            if not casted_data:
                print(f"Error. Could not read from stdin. ")
            else:
                self.assign_var(dir3, data)
        elif operation == "FS":  # FILE SEARCH
            var1 = self.get_var(dir1)
            if os.path.isfile(var1):
                data_frame = pd.read_csv(var1, header=None)
                self.assign_var(dir3, data_frame)
            else:
                print(f"Error. Provided file {var1} does not exist")
                sys.exit(1)
        elif operation == "LINES":  # LINES
            var1 = self.get_var(dir1)
            self.assign_var(dir3, len(var1))
        elif operation == "COLS":  # COLS
            var1 = self.get_var(dir1)
            self.assign_var(dir3, len(var1.columns))
        elif operation == "VER":
            var1 = self.get_var(dir1)
            var3 = self.get_var(dir3)
            if var1 >= var3:
                print(f"Error, index out of bounds")
                sys.exit(1)
        elif operation == "MEAN":
            var1 = self.get_var(dir1)
            var2 = self.get_var(dir2)
            if 0 <= var2 < len(var1.columns):
                mean_val = var1[var2].mean()
                self.assign_var(dir3, mean_val)
            else:
                print(f"Error. Index out of range")
        elif operation == "MODE":
            var1 = self.get_var(dir1)
            var2 = self.get_var(dir2)
            if 0 <= var2 < len(var1.columns):
                mode_val = var1.mode().iat[0, var2]
                self.assign_var(dir3, mode_val)
            else:
                print(f"Error. Index out of range")
        elif operation == "VAR":
            var1 = self.get_var(dir1)
            var2 = self.get_var(dir2)
            if 0 <= var2 < len(var1.columns):
                variance = var1[var2].var()
                self.assign_var(dir3, variance)
            else:
                print(f"Error. Index out of range")
        elif operation == "BAR":
            var1 = self.get_var(dir1)
            var2 = self.get_var(dir2)
            if 0 <= var2 < len(var1.columns):
                var1[var2].plot.bar(rot=0)
                pyplot.show()
            else:
                print(f"Error. Index out of range")
        elif operation == "COV":
            var1 = self.get_var(dir1)
            var2 = self.get_var(dir2)
            if 0 <= var2 < len(var1.columns):
                cov_res = var1.cov()[var2][var2]
                self.assign_var(dir3, cov_res)
            else:
                print(f"Error. Index out of range")
        elif operation == "SCAT":
            var1 = self.get_var(dir1)
            var2 = self.get_var(dir2)
            var3 = self.get_var(dir3)
            if 0 <= var2 < len(var1.columns) and 0 <= var3 < len(var1.columns):
                pyplot.scatter(var1[var2], var1[var3])
                # var1.plot.scatter(x=var2, y=var3)
                pyplot.show()
            else:
                print(f"Error. Index out of range")
        return self.__index_counter + 1
