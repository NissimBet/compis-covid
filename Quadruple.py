from enum import Enum, unique, auto


class Quadruple:
    @unique
    class OperationType(Enum):
        ADD = auto()
        SUBTRACT = auto()
        DIVIDE = auto()
        MULTIPLY = auto()

    def __init__(self, operation: OperationType, first_direction: str, second_direction: str, result: str):
        self.operation = operation
        self.first_direction = first_direction
        self.second_direction = second_direction
        self.result = result

    def __str__(self):
        return f'Quadruple ({self.operation}, {self.first_direction}, {self.second_direction}, {self.result})'
