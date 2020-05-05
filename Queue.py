from typing import List


class Queue:
    def __init__(self):
        self.__data = []

    @property
    def is_empty(self):
        return len(self.__data) == 0

    def empty(self):
        self.__data.clear()

    def push(self, data):
        self.__data.insert(0, data)

    def pop(self):
        if len(self.__data) > 0:
            return self.__data.pop(0)
        else:
            return None

    def top(self):
        if self.is_empty:
            return None
        return self.__data[0]

    def __str__(self):
        return f'Queue [{[item for item in self.__data.__reversed__()]}]'
