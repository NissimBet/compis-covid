from typing import Union, Dict, Any


class AVAIL:
    counter = 0
    # Estructura base de las variables
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
            "value": {}     # Este nivel es solo para tener consistencia con los niveles jerarquicos
                            # y que el typing no tenga problemas
        }
    }
    # los mapas de las direcciones a las variables es para tener una forma rapida
    # de accesar y revisar la existencia de las variables sin hacer comparaciones a costa del uso de memoria
    # mapeo de direccion a variable
    dir_to_var: Dict[str, str]
    # mapeo de direccion a valor constante
    dir_to_const: Dict[str, Dict[str, str]]
    # mapeo de valor constante a direccion
    const_to_dir: Dict[str, str]

    def __init__(self) -> None:
        # las categorias en que las variables se dividen y la direccion base
        categs = [("global", "non_temp", 1000), ("global", "temp", 2000),
                  ("local", "non_temp", 5000), ("local", "temp", 6000),
                  ("constant", "value", 10000)]
        # los tipos de datos existentes y sus tamanos
        self.data_types = [("int", 100), ("float", 100),
                           ("char", 100), ("string", 100),
                           ("bool", 100), ("dataFrame", 100),
                           ("pointer", 100)]
        # llenar los datos iniciales de la estructura del AVAIL
        # iterar por las categorias y los tipos y inicializar direcciones base, contador y tamano de la variable actual
        for category in categs:
            self.types[category[0]][category[1]] = {
                self.data_types[x][0]:
                    {
                        "min": category[2] + x * self.data_types[x][1],
                        "max": category[2] + (x + 1) * self.data_types[x][1] - 1,
                        "counter": 0,
                        "size": 1
                    } for x in range(len(self.data_types))
            }
        self.dir_to_var = {}
        self.const_to_dir = {}
        self.dir_to_const = {}

    def set_size(self, var_type: str, size: int, is_global: bool) -> None:
        """
        Funcion que asigna el tamano de la variable actual, para usar en el calculo de la proxima variable

        :param var_type: el tipo de la variable que se quiere agrandar
        :param size: el tamano a asignar a la variable
        :param is_global: si la variable es global o local
        :return: None
        """
        if is_global:
            self.types["global"]["non_temp"][var_type]["size"] = size
        else:
            self.types["local"]["non_temp"][var_type]["size"] = size

    def get_next_global(self, var_type: str, is_temp: bool, var_name: str = ""):
        """
        Funcion que regresa la direccion virtual proxima para el tipo de dato en el contexto global

        :param var_type: tipo de dato que se desea asignar
        :param is_temp: si es un dato de tipo temporal
        :param var_name: el nombre de la variable, se usa como llave para las variables temporales
        :return: la direccion virtual proxima para el tipo de variable global
        """
        if var_type in [x[0] for x in self.data_types]:
            if is_temp:
                count = self.types.get("global").get("temp").get(var_type).get("counter")
                minimum = self.types.get("global").get("temp").get(var_type).get("min")
                self.types.get("global").get("temp").get(var_type)["counter"] += 1
                # base + cantidad de variables asignada
                return minimum + count
            else:
                count = self.types.get("global").get("non_temp").get(var_type).get("counter")
                minimum = self.types.get("global").get("non_temp").get(var_type).get("min")
                size = self.types.get("global").get("non_temp").get(var_type).get("size")
                # variables no temporales pueden ser dimensionadas, se debe tomar en cuenta el tamano de la anterior
                self.types.get("global").get("non_temp").get(var_type)["counter"] += size
                # la variable proxima esta en base + contador + tamano del anterior - 1 (se inicia en 0)
                self.dir_to_var[str(minimum + count + size - 1)] = var_name
                return minimum + count + size - 1
        else:
            print(f"ERROR. variable type {var_type} not recognized")

    def get_next_local(self, var_type: str, is_temp: bool, var_name: str = ""):
        """
        Funcion que regresa la direccion virtual proxima para el tipo de dato en el contexto global

        :param var_type: tipo de dato que se desea asignar
        :param is_temp: si es un dato de tipo temporal
        :param var_name: el nombre de la variable, se usa como llave para las variables temporales
        :return: la direccion virtual proxima para el tipo de variable local
        """
        if var_type in [x[0] for x in self.data_types]:
            if is_temp:
                count = self.types.get("local").get("temp").get(var_type)["counter"]
                minimum = self.types.get("local").get("temp").get(var_type)["min"]
                self.types.get("local").get("temp").get(var_type)["counter"] += 1
                return minimum + count
            else:
                count = self.types.get("local").get("non_temp").get(var_type)["counter"]
                minimum = self.types.get("local").get("non_temp").get(var_type)["min"]
                size = self.types.get("local").get("non_temp").get(var_type).get("size")
                # variables no temporales pueden ser dimensionadas, se debe tomar en cuenta el tamano de la anterior
                self.types.get("local").get("non_temp").get(var_type)["counter"] += size
                # la variable proxima esta en base + contador + tamano del anterior - 1 (se inicia en 0)
                self.dir_to_var[str(count + minimum + size - 1)] = var_name
                return count + minimum + size - 1
        else:
            print(f"ERROR. variable type {var_type} not recognized")

    def reset_global(self):
        """
                Funcion que reinicia los contadores para las variables locales

                :return: la cantidad de variables temporales que se eliminaron para cada tipo
                """

        # Esta funcion realiza el reseteo para las variables temporales o no temporales
        def reset(var_scope: str):
            # Generar el diccionario de las variables y sus cantidades
            variables = {v_key: v_val.get("counter") for v_key, v_val in self.types.get("global").get(var_scope).items()
                         if v_val.get("counter") > 0}
            # iterar sobre los tipos de variables, reiniciando el contador y eliminando del mapa anterior la variable
            for val_dir in self.types.get("global").get(var_scope):
                counter = self.types.get("global").get(var_scope).get(val_dir)["counter"]
                minim = self.types.get("global").get(var_scope).get(val_dir)["min"]
                maxim = self.types.get("global").get(var_scope).get(val_dir)["max"]
                # para las variables declaradas, eliminarla del diccionario de variables
                for index in range(minim, minim + counter):
                    self.dir_to_var.pop(str(index), None)
                # reiniciar el contador
                self.types.get("global").get(var_scope).get(val_dir)["counter"] = 0
            return variables

        reset("non_temp")
        return reset("temp")

    def reset_locals(self):
        """
        Funcion que reinicia los contadores para las variables locales

        :return: la cantidad de variables temporales que se eliminaron para cada tipo
        """

        # Esta funcion realiza el reseteo para las variables temporales o no temporales
        def reset(var_scope: str):
            # Generar el diccionario de las variables y sus cantidades
            variables = {v_key: v_val.get("counter") for v_key, v_val in self.types.get("local").get(var_scope).items()
                         if v_val.get("counter") > 0}
            # iterar sobre los tipos de variables, reiniciando el contador y eliminando del mapa anterior la variable
            for val_dir in self.types.get("local").get(var_scope):
                counter = self.types.get("local").get(var_scope).get(val_dir)["counter"]
                minim = self.types.get("local").get(var_scope).get(val_dir)["min"]
                maxim = self.types.get("local").get(var_scope).get(val_dir)["max"]
                # para las variables declaradas, eliminarla del diccionario de variables
                for index in range(minim, minim + counter):
                    self.dir_to_var.pop(str(index), None)
                # reiniciar el contador
                self.types.get("local").get(var_scope).get(val_dir)["counter"] = 0
            return variables

        reset("non_temp")
        return reset("temp")

    def get_next_const(self, var_type: str, value: Any):
        """
        Funcion que genera una direccion virtual para una constante

        :param var_type: el tipo de variable a generar
        :param value: el valor de la variable constante
        :return: regresa la direccion de una constante
        """
        if var_type in [x[0] for x in self.data_types]:
            if str(value) not in self.const_to_dir:
                count = self.types.get("constant").get("value").get(var_type)["counter"]
                minimum = self.types.get("constant").get("value").get(var_type)["min"]
                self.types.get("constant").get("value").get(var_type)["counter"] += 1
                # inicializa el diccionario de la constante para almacenar el tipo y valor
                self.dir_to_const[str(count + minimum)] = {}
                self.dir_to_const[str(count + minimum)]["value"] = value
                self.dir_to_const[str(count + minimum)]["type"] = var_type
                self.const_to_dir[str(value)] = count + minimum
                return count + minimum
            else:
                return self.const_to_dir[str(value)]
        else:
            print("ERROR. variable type not recognized")

    def get_const_type(self, mem_dir: int):
        """Funcion que regresa el tipo de la variable en una direccion virtual"""
        return self.dir_to_const[str(mem_dir)]['type']

    def get_val_from_dir(self, var_dir: int):
        """regresa el valor de una variable en una direccion, ya sea constante o variable"""
        if str(var_dir) in self.dir_to_const:
            return self.dir_to_const[str(var_dir)]["value"]
        elif str(var_dir) in self.dir_to_var:
            return self.dir_to_var[str(var_dir)]


avail = AVAIL()
