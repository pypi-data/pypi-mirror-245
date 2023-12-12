class Token:
    def __init__(self, value: any, tt_type: str, line: int = None, index: int = None):
        self.value = value
        self.tt_type = tt_type

        self.line = line
        self.index = index

    def get_value(self) -> any:
        return self.value

    def get_position(self) -> tuple[int, int]:
        return self.line + 1, self.index  # starts at 1 and not 0

    def __repr__(self) -> str:
        return f'Token({self.value !r}, {self.tt_type !r})'
