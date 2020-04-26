# NO TENGO NI IDEA SI DEBERIAMOS HACERLO ASI
# HAZ DE CUENTA QUE ES UN SUPER EARLY DRAFT
from Stack import Stack


class ParsingContext(object):
    function: Stack
    var_type: str

    def __init__(self):
        self.function = Stack()
        self.var_type = ''

    def set_type(self, var_type: str):
        self.var_type = var_type

    def set_function(self, name: str):
        self.function.push(name)

    def __str__(self):
        return "({}, {})".format(self.function, self.var_type)
