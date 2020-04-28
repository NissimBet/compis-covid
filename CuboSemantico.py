dataTypes = [
    # data types
    'int',  # 0
    'float',  # 1
    'string',  # 2
    'char',  # 3
    'void',  # 4
    'dataFrame',  # 5
    'bool',  # 6
]

operators = [
    '+', '-', '*', '/', '=', '<', '>', "<>", "=="
]
#
# allowedOps = {
#     "int": {
#         "int": True,
#         "float": True,
#         'string': False,
#         'char': False,
#         'void': False,
#         'dataFrame': False,
#     }
# }


allowedOps = {
    '+' : [{"float", "int"}, {"float"}, {"int"}],
    '-' : [{"float", "int"}, {"float"}, {"int"}],
    '*' : [{"float", "int"}, {"float"}, {"int"}],
    '/' : [{"float", "int"}, {"float"}, {"int"}],
    '=' : [{"float", "int"}, {"float"}, {"int"}, {"string"}, {"char"}, {"dataFrame"}, {"bool"}],
    '<' : [{"float", "int"}, {"float"}, {"int"}],
    '>' : [{"float", "int"}, {"float"}, {"int"}],
    "<>": [{"float", "int"}, {"float"}, {"int"}, {"string"}, {"char"}, {"dataFrame"}, {"bool"}],
    "==": [{"float", "int"}, {"float"}, {"int"}, {"string"}, {"char"}, {"dataFrame"}, {"bool"}],
}


# '+'
# '-'
# '*'
# '/'
# '='
# '<'
# '>'
# "<>"
# "=="


class CuboSemantico:
    def __init__(self):
        self.cubo = {}
        # self.cubo = [
        #     {type1: {type2: {ops: {type1, type2} in allowedOps[ops]}}} for type1 in dataTypes for type2 in dataTypes
        #     for ops
        #     in operators]
        for type1 in dataTypes:
            self.cubo[type1] = {}
            for type2 in dataTypes:
                self.cubo[type1][type2] = {}
                for op in operators:
                    self.cubo[type1][type2][op] = {type1, type2} in allowedOps[op]

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