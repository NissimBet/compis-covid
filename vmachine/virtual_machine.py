import sys
import re
from Stack import Stack
from typing import List, Any, Dict

from .v_memory import Memory
from .v_function import VMFunction
from .v_variables import get_scope, get_type, try_cast

import os


class VirtualMachine:
    __index_counter: int
    __quads: List[List[str]]
    __execution_stack: Stack[VMFunction]
    __function_table: Dict[str, Dict[str, Any]]

    def __init__(self, file_path):
        self.__global_memory = Memory(1000)
        self.__constants = Memory(10000)
        self.__execution_stack = Stack[VMFunction]()

        self.__index_counter = 0
        self.__index_stack = Stack[int]()
        self.__quads: List[List[str]] = []

        self.__function_table = {}

        self.load_file_contents(file_path)

    def execute_quads(self):
        while self.__index_counter < len(self.__quads):
            current_quad = self.__quads[self.__index_counter]
            # print("counter ", self.__index_counter, len(self.__quads))
            # print("QUAD", current_quad)
            self.__index_counter = self.load_quad(current_quad[0], current_quad[1], current_quad[2], current_quad[3])

    def load_file_contents(self, filename: str):
        if os.path.exists(filename):
            with open(filename, "r") as file:
                stop_string = file.readline()
                # CONST TABLE
                for line in file:
                    if line == stop_string:
                        break
                    else:
                        values = line.strip("\r\n").split(',')
                        if len(values) < 2:
                            print(f"Error, malformed pair for constant variables")
                        else:
                            self.__constants.push_var(int(values[0]), try_cast(int(values[0]), values[1]))
                # FUNCTION TABLE
                for line in file:
                    if line == stop_string:
                        break
                    else:
                        values = re.match(r"(\w*),(\w*),(\w*),(\[.*\]),(\[.*\])", line.strip('\r\n'))
                        func_vars = re.findall(r"\(.*?,.*?\)", values.group(4))
                        temp_vars = re.findall(r"\(.*?,.*?\)", values.group(5))
                        # print(values.groups())
                        # print(func_vars)
                        # print(temp_vars)
                        num_vars = {}
                        num_temps = {}
                        for func_var in func_vars:
                            var_type = func_var.split(',')
                            num_vars.setdefault(var_type[0].strip("()'"), int(var_type[1].strip("()'")))
                        for temp_var in temp_vars:
                            temp_type = temp_var.split(',')
                            num_temps.setdefault(temp_type[0].strip("()'"), int(temp_type[1].strip("()'")))

                        if len(values.groups()) < 5:
                            print(f"Error, malformed fucntion table data")
                        else:
                            new_function = {
                                "type": values[2],
                                "dir_start": values[3],
                                "num_vars": num_vars,
                                "num_temps": num_temps
                            }
                            self.__function_table.setdefault(values[1], new_function)
                # QUADS
                for line in file:
                    quad = line.strip("\r\n").split(',')
                    if len(quad) < 4:
                        print("Error, malformed quad", quad)
                    else:
                        self.__quads.append(quad)
                # print(f"Found Constants {[c for c in self.__constants.get_vars()]}")
                # print(f"Found Functions {[f for f in self.__function_table.keys()]}")
        else:
            print(f"File {filename} was not found")

    def get_var(self, var_dir: str):
        try:
            direction = int(var_dir)
        except ValueError:
            print(f"Provided Direction is not a number format {var_dir}")
            return
        var_scope = get_scope(direction)
        if var_scope == "global":
            return self.__global_memory.get_var(direction)
        elif var_scope == "local":
            return self.__execution_stack.top().get_var(direction)
        elif var_scope == "constant":
            return self.__constants.get_var(direction)

    def assign_var(self, var_dir: str, value: Any):
        try:
            direction = int(var_dir)
        except ValueError:
            print(f"Provided Direction is not a number format {var_dir}, cannot assign {value}")
            return
        var_scope = get_scope(direction)
        if var_scope == "global":
            # self.__global_memory.assign_var(direction, try_cast(direction, value))
            self.__global_memory.assign_var(direction, value)
        elif var_scope == "local":
            # self.__execution_stack.top().assign_var(direction, try_cast(direction, value))
            self.__execution_stack.top().assign_var(direction, value)
        elif var_scope == "constant":
            # return self.__constants.assign_var(direction, try_cast(direction, value))
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
            # self.__index_counter = int(dir3)
            return int(dir3)
        elif operation == "GOTOV":
            var1 = self.get_var(dir1)
            if var1:
                # self.__index_counter = int(dir3)
                return int(dir3)
        elif operation == "GOTOF":
            var1 = self.get_var(dir1)
            if not var1:
                # self.__index_counter = int(dir3)
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
            return int(dir3)
        elif operation == "ERA":  # ERA
            function = self.__function_table.get(dir3)
            function_context = VMFunction(dir3)
            for var, size in function.get("num_vars").items():
                function_context.era(var, size, False)
            for var, size in function.get("num_temps").items():
                function_context.era(var, size, True)
            self.__execution_stack.push(function_context)
        elif operation == "PARAM":  # PARAM
            current_context = self.__execution_stack.pop()
            var1 = self.get_var(dir1)
            current_context.pass_param(int(dir3), var1)
            self.__execution_stack.push(current_context)
        elif operation == "ENDFUNC":  # END FUNC
            self.__execution_stack.pop()
            return self.__index_stack.pop() + 1
        elif operation == "WRITE":  # WRITE
            var3 = self.get_var(dir3)
            print(var3)
        elif operation == "READ":  # READ
            data = input()
            self.assign_var(dir3, data)
        elif operation == "LOAD":  # LOAD
            pass
        elif operation == "FS":  # FILE SEARCH
            pass
        elif operation == "LINES":  # LINES
            pass
        elif operation == "COLS":  # COLS
            pass
        return self.__index_counter + 1
