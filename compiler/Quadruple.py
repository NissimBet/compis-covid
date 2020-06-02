from enum import Enum, unique
from typing import Union

# mapeo de los operadores simples a su nombre en el enum
operator_names = {
    '+': "SUM",
    '-': "SUB",
    '*': "MULT",
    '/': "DIV",
    '=': "ASG",
    '<': "LT",
    '>': "GT",
    "<>": "NEQ",
    "==": "EQ",
    "&&": "LAND",
    "||": "LOR",
}


class Quadruple:
    @unique
    class OperationType(Enum):
        # operaciones simples
        ADD = "SUM"
        SUBTRACT = "SUB"
        DIVIDE = "DIV"
        MULTIPLY = "MULT"
        ASSIGN = "ASG"
        # comparacion entera
        LESS_THAN = "LT"
        GREATER_THAN = "GT"
        EQUALS = "EQ"
        NOT_EQUAL = "NEQ"
        # comparacion logica
        LOGIC_AND = "LAND"
        LOGIC_OR = "LOR"
        # saltos de posicion
        GOTO = "GOTO"
        GOTO_TRUE = "GOTOV"
        GOTO_FALSE = "GOTOF"
        # manejo de funciones
        GO_SUB = "GOSUB"
        ERA = "ERA"
        PARAMETER = "PARAM"
        END_FUNC = "ENDFUNC"
        # input / output
        WRITE = "WRITE"
        READ = "READ"
        LOAD = "LOAD"
        FILE_SEARCH = "FS"
        LINES = "LINES"
        COLS = "COLS"
        # fin de programa
        END_PROG = "END"
        # revision de indice en arreglo
        VER = "VER"
        # metodos estadisticos
        MEAN = "MEAN"

    @staticmethod
    def get_operator_name(name: str):
        """Regresa el nombre del operador"""
        if name in operator_names:
            return operator_names[name]
        return None

    def __init__(self, operation: Union[OperationType, str], first_direction: str, second_direction: str, result: str):
        self.operation = operation.name if type(operation) is self.OperationType else operation
        self.first_direction = first_direction
        self.second_direction = second_direction
        self.result = result

    def __str__(self):
        return f'Quadruple ({self.operation}, {self.first_direction}, {self.second_direction}, {self.result})'
