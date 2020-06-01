from typing import Final, Generic, TypeVar, List

T = TypeVar("T")


class Stack(Generic[T]):
    def __init__(self):
        self.__data: List[T] = []
        self.false_bottom: Final = "$"

    @property
    def is_empty(self) -> bool:
        return len(self.__data) == 0

    def push(self, data):
        self.__data.append(data)

    def pop(self) -> T:
        if len(self.__data) > 0:
            return self.__data.pop()
        else:
            return None

    def add_separator(self) -> None:
        self.push(self.false_bottom)

    def remove_separator(self) -> None:
        if self.top() == self.false_bottom:
            self.pop()

    @property
    def is_bottom(self) -> bool:
        return self.top() == self.false_bottom

    def top(self) -> T:
        if self.is_empty:
            return None
        return self.__data[-1]

    def __str__(self):
        return f'Stack [{[item for item in self.__data]}]'
