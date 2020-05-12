from enum import Enum, unique


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

    def __init__(self, operation: OperationType, first_direction: str, second_direction: str, result: str):
        self.operation = operation
        self.first_direction = first_direction
        self.second_direction = second_direction
        self.result = result

    def __str__(self):
        return f'Quadruple ({self.operation}, {self.first_direction}, {self.second_direction}, {self.result})'
