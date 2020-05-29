import sys

from typing import List

from .v_memory import Memory
import os


class VirtualMachine:
    __memory: Memory
    __index_counter: int
    __quads: List[List[str]]

    def __init__(self, file_path):
        self.__memory = Memory()
        self.__index_counter = 0
        self.__quads = []
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
                for line in file:
                    if line == stop_string:
                        break
                    else:
                        values = line.strip("\r\n").split(',')
                        if len(values) < 2:
                            print(f"Error, malformed pair for constant variables")
                        self.__memory.allocate_var(values[0], values[1])
                for line in file:
                    quad = line.strip("\r\n").split(',')
                    if len(quad) < 4:
                        print("Error, malformed quad", quad)
                    else:
                        self.__quads.append(quad)
        else:
            print(f"File {filename} was not found")

    def load_quad(self, operation: str, dir1: str, dir2: str, dir3: str):
        # print(operation, dir1, dir2, dir3, sep=",")
        if operation == "SUM":
            var1 = self.__memory.get_var(dir1)
            var2 = self.__memory.get_var(dir2)
            self.__memory.assign_var(dir3, int(var1) + int(var2))
        elif operation == "SUB":
            var1 = self.__memory.get_var(dir1)
            var2 = self.__memory.get_var(dir2)
            self.__memory.assign_var(dir3, int(var1) - int(var2))
        elif operation == "DIV":
            var1 = self.__memory.get_var(dir1)
            var2 = self.__memory.get_var(dir2)
            self.__memory.assign_var(dir3, int(var1) / int(var2))
        elif operation == "MULT":
            var1 = self.__memory.get_var(dir1)
            var2 = self.__memory.get_var(dir2)
            self.__memory.assign_var(dir3, int(var1) * int(var2))
        elif operation == "ASG":
            var1 = self.__memory.get_var(dir1)
            self.__memory.assign_var(dir3, var1)
        elif operation == "GOTO":
            # self.__index_counter = int(dir3)
            return int(dir3)
        elif operation == "GOTOV":
            var1 = self.__memory.get_var(dir1)
            if var1:
                # self.__index_counter = int(dir3)
                return int(dir3)
        elif operation == "GOTOF":
            var1 = self.__memory.get_var(dir1)
            if not var1:
                # self.__index_counter = int(dir3)
                return int(dir3)
        elif operation == "LT":
            var1 = self.__memory.get_var(dir1)
            var2 = self.__memory.get_var(dir2)
            self.__memory.assign_var(dir3, int(var1) < int(var2))
        elif operation == "GT":
            var1 = self.__memory.get_var(dir1)
            var2 = self.__memory.get_var(dir2)
            self.__memory.assign_var(dir3, var1 > var2)
        elif operation == "EQ":
            var1 = self.__memory.get_var(dir1)
            var2 = self.__memory.get_var(dir2)
            self.__memory.assign_var(dir3, var1 == var2)
        elif operation == "NEQ":
            var1 = self.__memory.get_var(dir1)
            var2 = self.__memory.get_var(dir2)
            self.__memory.assign_var(dir3, var1 != var2)
        elif operation == "LAND":  # LOGIC AND
            var1 = self.__memory.get_var(dir1)
            var2 = self.__memory.get_var(dir2)
            self.__memory.assign_var(dir3, var1 and var2)
        elif operation == "LOR":  # LOGIC OR
            var1 = self.__memory.get_var(dir1)
            var2 = self.__memory.get_var(dir2)
            self.__memory.assign_var(dir3, var1 or var2)
        elif operation == "GOSUB":  # GOSUB
            pass
        elif operation == "ERA":  # ERA
            pass
        elif operation == "PARAM":  # PARAM
            pass
        elif operation == "ENDFUNC":  # END FUNC
            pass
        elif operation == "WRITE":  # WRITE
            var1 = self.__memory.get_var(dir3)
            print(var1)
        elif operation == "READ":  # READ
            pass
        elif operation == "LOAD":  # LOAD
            pass
        elif operation == "FS":  # FILE SEARCH
            pass
        elif operation == "LINES":  # LINES
            pass
        elif operation == "COLS":  # COLS
            pass
        return self.__index_counter + 1
