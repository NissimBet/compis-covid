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
        ADD = "SUM"
        SUBTRACT = "SUB"
        DIVIDE = "DIV"
        MULTIPLY = "MULT"
        ASSIGN = "ASG"
        GOTO = "GOTO"
        GOTO_TRUE = "GOTOV"
        GOTO_FALSE = "GOTOF"
        LESS_THAN = "LT"
        GREATER_THAN = "GT"
        EQUALS = "EQ"
        NOT_EQUAL = "NEQ"
        LOGIC_AND = "LAND"
        LOGIC_OR = "LOR"
        GO_SUB = "GOSUB"
        ERA = "ERA"
        PARAMETER = "PARAM"
        END_FUNC = "ENDFUNC"
        WRITE = "WRITE"
        READ = "READ"
        LOAD = "LOAD"
        FILE_SEARCH = "FS"
        LINES = "LINES"
        COLS = "COLS"
        END_PROG = "END"
        VER = "VER"

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
