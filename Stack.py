from typing import Final


class Stack(object):
    def __init__(self):
        self.__data = []
        self.false_bottom: Final = "$"

    @property
    def is_empty(self):
        return len(self.__data) == 0

    def push(self, data):
        self.__data.append(data)

    def pop(self):
        if len(self.__data) > 0:
            return self.__data.pop()
        else:
            return None

    def add_separator(self):
        self.push(self.false_bottom)

    def remove_separator(self):
        self.pop()

    @property
    def is_bottom(self):
        return self.top() == self.false_bottom

    def top(self):
        if self.is_empty:
            return None
        return self.__data[-1]

    def __str__(self):
        return f'Stack [{[item for item in self.__data]}]'
