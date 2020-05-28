from typing import Dict, Any


class Memory:
    __memory: Dict[str, Any]

    def __init__(self):
        self.__memory = {}

    def get_var(self, variable_dir: str):
        return self.__memory[variable_dir]

    def assign_var(self, variable_dir: str, value: Any):
        self.__memory[variable_dir] = value

    def allocate_var(self, variable_dir: str, value: Any):
        try:
            self.__memory[variable_dir] = value
        except KeyError:
            print(f"Error during allocation of variable")
            return False
        return True

    def allocate_function(self, function_dir: str):
        try:
            self.__memory[function_dir] = {
                "parameters": [""],
                "variables": {}
            }
        except KeyError:
            print(f"Error allocating function")
            return False
        return True

    def pass_param(self, function_dir: str, destination_param: str, param_value: str):
        try:
            self.__memory[function_dir]["parameters"][destination_param] = param_value
        except KeyError or IndexError:
            print(f"Error sendinf parameter to function")
            return False
        return True

    def add_function_vars(self, function_dir: str, variables_type: str, size_amount: int):
        try:
            self.__memory[function_dir][variables_type] = size_amount
        except KeyError:
            print("Error adding variables to function")
            return False
        return True

    def remove_function(self, function_dir: str):
        try:
            del self.__memory[function_dir]
        except KeyError:
            print("Error removing function")
            return False
        return True

    def clear(self):
        self.__memory.clear()
