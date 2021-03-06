dataTypes = [
    # data types
    'int',  # 0
    'float',  # 1
    'string',  # 2
    'char',  # 3
    #'void',  # 4
    'dataFrame',  # 5
    'bool',  # 6
]

operators = [
    '+', '-', '*', '/', '=', '<', '>', "<>", "==", "&&", "||"
]


# allowedOps = {
#     '+' : [{"float", "int"}, {"float"}, {"int"}],
#     '-' : [{"float", "int"}, {"float"}, {"int"}],
#     '*' : [{"float", "int"}, {"float"}, {"int"}],
#     '/' : [{"float", "int"}, {"float"}, {"int"}],
#     '=' : [{"float", "int"}, {"float"}, {"int"}, {"string"}, {"char"}, {"dataFrame"}, {"bool"}],
#     '<' : [{"float", "int"}, {"float"}, {"int"}],
#     '>' : [{"float", "int"}, {"float"}, {"int"}],
#     "<>": [{"float", "int"}, {"float"}, {"int"}, {"string"}, {"char"}, {"dataFrame"}, {"bool"}],
#     "==": [{"float", "int"}, {"float"}, {"int"}, {"string"}, {"char"}, {"dataFrame"}, {"bool"}],
# }

allowedOps = {
    '+' : [
        ({"float", "int"}, "float"),
        ({"float"}, "float"),
        ({"int"}, "int")
    ],
    '-' : [
        ({"float", "int"}, "float"),
        ({"float"}, "float"),
        ({"int"}, "int")
    ],
    '*' : [
        ({"float", "int"}, "float"),
        ({"float"}, "float"),
        ({"int"}, "int")
    ],
    '/' : [
        ({"float", "int"}, "float"),
        ({"float"}, "float"),
        ({"int"}, "int")

    ],
    '=' : [
        ({"float", "int"}, "float"),
        ({"float"}, "float"),
        ({"int"}, "int"),
        ({"string"}, "string"),
        ({"char"}, "char"),
        ({"dataFrame"}, "dataFrame"),
        ({"bool"}, "bool")
    ],
    '<' : [
        ({"float", "int"}, "bool"),
        ({"float"}, "bool"),
        ({"int"}, "bool")
    ],
    '>' : [
        ({"float", "int"}, "bool"),
        ({"float"}, "bool"),
        ({"int"}, "bool")
    ],
    "<>": [
        ({"float", "int"}, "bool"),
        ({"float"}, "bool"),
        ({"int"}, "bool"),
        ({"string"}, "bool"),
        ({"char"}, "bool"),
        ({"dataFrame"}, "bool"),
        ({"bool"}, "bool")
    ],
    "==": [
        ({"float", "int"}, "bool"),
        ({"float"}, "bool"),
        ({"int"}, "bool"),
        ({"string"}, "bool"),
        ({"char"}, "bool"),
        ({"dataFrame"}, "bool"),
        ({"bool"}, "bool")
    ],
    "&&": [
        ({"bool"}, "bool")
    ],
    "||": [
        ({"bool"}, "bool")
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
