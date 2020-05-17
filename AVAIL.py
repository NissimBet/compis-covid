from typing import Union, Dict, Any


class AVAIL:
    counter = 0
    types: Dict[str, Dict[str, Dict[str, Dict[str, Any]]]] = {
        "global": {
            "non_temp": {},
            "temp": {},
        },
        "local": {
            "non_temp": {},
            "temp": {}
        },
        "constant": {
            "variable": {}
        }
    }
    dir_to_var: Dict[str, str]
    dir_to_const: Dict[str, Dict[str, str]]
    const_to_dir: Dict[str, str]

    def __init__(self) -> None:
        # self.counter = 0
        self.data_types = [("int" ,100), ("float" ,100), ("char" ,100), ("string" ,100), ("bool" ,100), ("dataFrame" ,100)]
        self.types["global"]["non_temp"] = {self.data_types[x][0]: { "min": 1000 + x * self.data_types[x][1], "max": 1000 + (x + 1) * self.data_types[x][1], "counter": 0} for x in range(len(self.data_types))}
        self.types["global"]["temp"] = {self.data_types[x][0]: { "min": 2000 + x * self.data_types[x][1], "max": 2000 + x * self.data_types[x][1], "counter": 0} for x in range(len(self.data_types))}
        self.types["local"]["non_temp"] = {self.data_types[x][0]: { "min": 5000 + x * self.data_types[x][1], "max": 5000 + x * self.data_types[x][1], "counter": 0} for x in range(len(self.data_types))}
        self.types["local"]["temp"] = {self.data_types[x][0]: { "min": 6000 + x * self.data_types[x][1], "max": 6000 + x * self.data_types[x][1], "counter": 0} for x in range(len(self.data_types))}
        self.types["constant"]["value"] = {self.data_types[x][0]: { "min": 10000 + x * self.data_types[x][1], "max": 10000 + x * self.data_types[x][1], "counter": 0} for x in range(len(self.data_types))}
        self.dir_to_var = {}
        self.const_to_dir = {}
        self.dir_to_const = {}

    def get_next(self):
        self.counter = self.counter + 1
        return f"tempvar-{self.counter - 1}"

    def get_next_global(self, var_type: str, is_temp: bool, var_name: str = ""):
        if var_type in [x[0] for x in self.data_types]:
            if is_temp:
                count = self.types.get("global").get("temp").get(var_type)["counter"]
                minimum = self.types.get("global").get("temp").get(var_type)["min"]
                self.types.get("global").get("temp").get(var_type)["counter"] += 1
                return minimum + count
            else:
                count = self.types.get("global").get("non_temp").get(var_type)["counter"]
                minimum = self.types.get("global").get("non_temp").get(var_type)["min"]
                self.types.get("global").get("non_temp").get(var_type)["counter"] += 1

                self.dir_to_var[str(minimum + count)] = var_name
                return minimum + count
        else:
            print(f"ERROR. variable type {var_type} not recognized")

    def get_next_local(self, var_type: str, is_temp: bool, var_name: str = ""):
        if var_type in [x[0] for x in self.data_types]:
            if is_temp:
                count = self.types.get("local").get("temp").get(var_type)["counter"]
                minimum = self.types.get("local").get("temp").get(var_type)["min"]
                self.types.get("local").get("temp").get(var_type)["counter"] += 1
                return minimum + count
            else:
                count = self.types.get("local").get("non_temp").get(var_type)["counter"]
                minimum = self.types.get("local").get("non_temp").get(var_type)["min"]
                self.types.get("local").get("non_temp").get(var_type)["counter"] += 1

                self.dir_to_var[str(count + minimum)] = var_name
                return count + minimum
        else:
            print(f"ERROR. variable type {var_type} not recognized")

    def reset_locals(self):
        def reset(var_type: str):
            for val_dir in self.types.get("local").get(var_type):
                counter = self.types.get("local").get(var_type).get(val_dir)["counter"]
                minim = self.types.get("local").get(var_type).get(val_dir)["min"]
                maxim = self.types.get("local").get(var_type).get(val_dir)["max"]
                for index in range(minim, counter):
                    self.dir_to_var.pop(str(minim + index))
                self.types.get("local").get(var_type).get(val_dir)["counter"] = 0
        reset("non_temp")
        reset("temp")

    def set_const_var(self, const_type: str, const_val: Any):
        if const_type in [x[0] for x in self.data_types]:
            if const_val not in self.const_to_dir:
                const_dir = self.get_next_const(const_type, const_val)
                self.const_to_dir[const_val] = const_dir
                return const_dir
            else:
                return self.const_to_dir[const_val]
        else:
            print("ERROR. Const datatype not accepted")

    def get_next_const(self, var_type: str, value: Any):
        if var_type in [x[0] for x in self.data_types]:
            if value not in self.const_to_dir:
                count = self.types.get("constant").get("value").get(var_type)["counter"]
                minimum = self.types.get("constant").get("value").get(var_type)["min"]
                self.types.get("constant").get("value").get(var_type)["counter"] += 1
                self.dir_to_const[str(count + minimum)] = {}
                self.dir_to_const[str(count + minimum)]["value"] = value
                self.dir_to_const[str(count + minimum)]["type"] = var_type
                return count + minimum
            else:
                return self.const_to_dir[value]
        else:
            print("ERROR. variable type not recognized")

    def get_const_type(self, mem_dir: int):
        return self.dir_to_const[str(mem_dir)]['type']


avail = AVAIL()
