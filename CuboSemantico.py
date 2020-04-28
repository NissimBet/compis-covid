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
    '<' : [{"float", "int"}],
    '>' : [{"float", "int"}],
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
