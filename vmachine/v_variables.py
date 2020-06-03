from typing import Any

categs = [("global", "non_temp", 2000, 1000), ("global", "temp", 18000, 1000),
          ("local", "non_temp", 3000, 1000), ("local", "temp", 8000, 1000),
          ("constant", "value", 15000, 1000)]

data_types = [("int", 0, 100), ("float", 100, 100),
              ("char", 200, 100), ("string", 300, 100),
              ("bool", 400, 100), ("dataFrame", 500, 100),
              ("pointer", 600, 100)]

compiler_categs = [("global", "non_temp", 1000, 1000), ("global", "temp", 2000, 1000),
                   ("local", "non_temp", 5000, 1000), ("local", "temp", 6000, 1000),
                   ("constant", "value", 10000, 1000)]

compiler_data_types = [("int", 0, 100), ("float", 100, 100),
                       ("char", 200, 100), ("string", 300, 100),
                       ("bool", 400, 100), ("dataFrame", 500, 100),
                       ("pointer", 600, 100)]


def convert_dir(mem_direction: int):
    for categ_idx, categ in enumerate(compiler_categs):
        if categ[2] <= mem_direction < categ[2] + categ[3]:
            direction = mem_direction - categ[2]
            for type_idx, d_type in enumerate(compiler_data_types):
                if d_type[1] <= direction < d_type[1] + d_type[2]:
                    return mem_direction - compiler_categs[categ_idx][2] - compiler_data_types[type_idx][1] + \
                           categs[categ_idx][2] + data_types[type_idx][1]


def get_scope(mem_direction: int):
    for categ in categs:
        if categ[2] <= mem_direction < categ[2] + categ[3]:
            return categ[0]


def get_type(mem_direction: int):
    for categ in categs:
        if categ[2] <= mem_direction < categ[2] + categ[3]:
            direction = mem_direction - categ[2]
            for d_type in data_types:
                if d_type[1] <= direction < d_type[1] + d_type[2]:
                    return d_type[0]


def try_cast(mem_direction: int, mem_value: Any):
    val_type = get_type(mem_direction)
    try:
        if val_type == "int":
            return int(mem_value)
        elif val_type == "float":
            return float(mem_value)
        elif val_type == "string":
            return str(mem_value)
        elif val_type == "bool":
            return bool(mem_value)
        elif val_type == "char":
            return str(mem_value)[0]
        elif val_type == "dataFrame":
            return mem_value
        elif val_type == "pointer":
            return mem_value
    except ValueError:
        print(f"Error Casting value {mem_value} to {val_type}")
    return None
