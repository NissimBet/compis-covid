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
    dir_to_const: Dict[str, Any]

    def __init__(self) -> None:
        # self.counter = 0
        self.data_types = ["int", "float", "char", "string", "bool", "dataFrame"]
        self.types["global"]["non_temp"] = {self.data_types[x]: { "min": 1000 + x * 100, "max": 1000 + (x + 1) * 100 - 1, "counter": 0} for x in range(len(self.data_types))}
        self.types["global"]["temp"] = {self.data_types[x]: { "min": 2000 + x * 100, "max": 2000 + (x + 1) * 100 - 1, "counter": 0} for x in range(len(self.data_types))}
        self.types["local"]["non_temp"] = {self.data_types[x]: { "min": 5000 + x * 100, "max": 5000 + (x + 1) * 100 - 1, "counter": 0} for x in range(len(self.data_types))}
        self.types["local"]["temp"] = {self.data_types[x]: { "min": 6000 + x * 100, "max": 6000 + (x + 1) * 100 - 1, "counter": 0} for x in range(len(self.data_types))}
        self.types["constant"]["value"] = {self.data_types[x]: { "min": 10000 + x * 100, "max": 10000 + (x + 1) * 100 - 1, "counter": 0} for x in range(len(self.data_types))}
        self.dir_to_var = {}
        self.dir_to_const = {}

    def get_next(self):
        self.counter = self.counter + 1
        return f"tempvar-{self.counter - 1}"

    def get_next_global(self, var_type: str, is_temp: bool, var_name: str = ""):
        if var_type in self.data_types:
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
            print("ERROR. variable type not recognized")

    def get_next_local(self, var_type: str, is_temp: bool, var_name: str = ""):
        if var_type in self.data_types:
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
            print("ERROR. variable type not recognized")

    def get_next_const(self, var_type: str, value: Any = ""):
        if var_type in self.data_types:
            count = self.types.get("constant").get("value").get(var_type)["counter"]
            minimum = self.types.get("constant").get("value").get(var_type)["min"]
            self.types.get("constant").get("value").get(var_type)["counter"] += 1
            self.dir_to_const[str(count + min)] = value
            return count + min
        else:
            print("ERROR. variable type not recognized")

    # def get_next_type(self, data_type: str, is_temp: bool, var_type: str):
    #     if data_type in ["global", "local"]:
    #         if is_temp:
    #             if var_type in self.types["temp"]:
    #                 self.types["global"]["temp"][var_type].counter += 1
    #                 if self.types["global"]["temp"][var_type].counter > self.types["global"]["temp"][var_type].max:
    #                     print(f"ERROR. Too many variables set for global {var_type}")
    #                 return self.types["global"]["temp"][var_type].counter
    #             elif var_type in self.types["non_temp"]:
    #                 self.types["global"]["non_temp"][var_type].counter += 1
    #                 if self.types["global"]["non_temp"][var_type].counter > self.types["global"]["non_temp"][var_type].max:
    #                     print(f"ERROR. Too many variables set for local {var_type}")
    #                 return self.types["global"]["non_temp"][var_type].counter
    #             else:
    #                 print(f"ERROR. {var_type} not recognized")
    #     elif data_type == "constant":
    #         self.types["constant"]["value"][var_type].counter += 1
    #         if self.types["constant"]["value"][var_type].counter > self.types["constant"]["value"][var_type].max:
    #             print(f"ERROR. Too many variables set for constant {var_type}")
    #         return self.types["constant"]["value"][var_type].counter
    #     else:
    #         print(f"ERROR. {data_type} not recognized")


avail = AVAIL()
