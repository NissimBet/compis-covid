# tipos de datos aceptados
dataTypes = [
    'int',  # 0
    'float',  # 1
    'string',  # 2
    'char',  # 3
    'dataFrame',  # 5
    'bool',  # 6
    'pointer'
]
# operadores validos
operators = [
    '+', '-', '*', '/', '=', '<', '>', "<>", "==", "&&", "||"
]
# operaciones permitidas
# es un mapa de la operacion y los resultados generados segun un set
allowedOps = {
    '+' : [
        ({"float", "int"}, "float"),
        ({"float"}, "float"),
        ({"int"}, "int"),
        ({"pointer"}, "pointer"),
        ({"pointer", "int"}, "int"),
        ({"pointer", "float"}, "float"),
    ],
    '-' : [
        ({"float", "int"}, "float"),
        ({"float"}, "float"),
        ({"int"}, "int"),
        ({"pointer"}, "pointer"),
        ({"pointer", "int"}, "int"),
        ({"pointer", "float"}, "float"),
    ],
    '*' : [
        ({"float", "int"}, "float"),
        ({"float"}, "float"),
        ({"int"}, "int"),
        ({"pointer"}, "pointer"),
        ({"pointer", "int"}, "int"),
        ({"pointer", "float"}, "float"),
    ],
    '/' : [
        ({"float", "int"}, "float"),
        ({"float"}, "float"),
        ({"int"}, "int"),
        ({"pointer"}, "pointer"),
        ({"pointer", "int"}, "int"),
        ({"pointer", "float"}, "float"),
    ],
    '=' : [
        ({"float", "int"}, "float"),
        ({"float"}, "float"),
        ({"int"}, "int"),
        ({"string"}, "string"),
        ({"char"}, "char"),
        ({"dataFrame"}, "dataFrame"),
        ({"bool"}, "bool"),
        ({"pointer"}, "pointer"),
        ({"pointer", "int"}, "int"),
        ({"pointer", "float"}, "float"),
        ({"pointer", "string"}, "string"),
        ({"pointer", "char"}, "char"),
        ({"pointer", "bool"}, "bool")
    ],
    '<' : [
        ({"float", "int"}, "bool"),
        ({"float"}, "bool"),
        ({"int"}, "bool"),
        ({"pointer"}, "bool"),
        ({"pointer", "int"}, "bool"),
        ({"pointer", "float"}, "bool"),
    ],
    '>' : [
        ({"float", "int"}, "bool"),
        ({"float"}, "bool"),
        ({"int"}, "bool"),
        ({"pointer"}, "bool"),
        ({"pointer", "int"}, "bool"),
        ({"pointer", "float"}, "bool"),
    ],
    "<>": [
        ({"float", "int"}, "bool"),
        ({"float"}, "bool"),
        ({"int"}, "bool"),
        ({"string"}, "bool"),
        ({"char"}, "bool"),
        ({"dataFrame"}, "bool"),
        ({"bool"}, "bool"),
        ({"pointer"}, "bool"),
        ({"pointer", "int"}, "bool"),
        ({"pointer", "float"}, "bool"),
        ({"pointer", "string"}, "bool"),
        ({"pointer", "char"}, "bool"),
        ({"pointer", "bool"}, "bool")
    ],
    "==": [
        ({"float", "int"}, "bool"),
        ({"float"}, "bool"),
        ({"int"}, "bool"),
        ({"string"}, "bool"),
        ({"char"}, "bool"),
        ({"dataFrame"}, "bool"),
        ({"bool"}, "bool"),
        ({"pointer"}, "bool"),
        ({"pointer", "int"}, "bool"),
        ({"pointer", "float"}, "bool"),
        ({"pointer", "string"}, "bool"),
        ({"pointer", "char"}, "bool"),
        ({"pointer", "bool"}, "bool")
    ],
    "&&": [
        ({"bool"}, "bool"),
        ({"pointer"}, "bool"),
        ({"pointer", "bool"}, "bool")
    ],
    "||": [
        ({"bool"}, "bool"),
        ({"pointer"}, "bool"),
        ({"pointer", "bool"}, "bool")
    ]
}


class CuboSemantico:
    def __init__(self):
        self.cubo = {}
        for type1 in dataTypes:
            self.cubo[type1] = {}
            for type2 in dataTypes:
                self.cubo[type1][type2] = {}
                for op in operators:
                    try:
                        # indice del valor resultado de la operacion para el operador
                        index = [pair[0] for pair in allowedOps[op]].index({type1, type2})
                        value = allowedOps[op][index][1]
                    except ValueError:
                        value = None
                    self.cubo[type1][type2][op] = value

    def display(self):
        for type1, k1 in self.cubo.items():
            for type2, k2 in k1.items():
                sep1 = "\t\t\t"
                sep2 = "\t\t\t"

                if type1 == "int": sep1 += '\t'
                if type1 == "dataFrame": sep1 = sep1[1:]

                if type2 == "int": sep2 += '\t'
                if type2 == "dataFrame": sep2 = sep2[1:]
                print(f'{type1}{sep1}{type2}{sep2}{k2}')
