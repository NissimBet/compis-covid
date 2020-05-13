class AVAIL:
    counter = 0

    def __init__(self) -> None:
        # self.counter = 0
        pass

    def get_next(self):
        self.counter = self.counter + 1
        return f"tempvar-{self.counter - 1}"


avail = AVAIL()
