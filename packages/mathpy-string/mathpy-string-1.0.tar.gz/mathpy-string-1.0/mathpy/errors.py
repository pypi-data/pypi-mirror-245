class MathPySyntaxError(SyntaxError):
    def __init__(self, expected_char, error_token=None, *, default_message_format: bool = True):
        if default_message_format:
            if error_token is None:
                super().__init__(f'Incomplete syntax (missing {expected_char})')
            else:
                line, column = error_token.get_position()
                super().__init__(
                    f'Expected {expected_char !r}. Got {error_token.get_value() !r} instead (line {line}, column {column})')
        else:
            super().__init__(expected_char)


class MathPyIndexError(IndexError):
    pass


class MathPyIllegalCharError(SyntaxError):
    pass


class MathPyTypeError(TypeError):
    pass


class MathPyValueError(ValueError):
    pass


class MathPyNameError(NameError):
    pass


class MathPyAttributeError(AttributeError):
    pass


class MathPyZeroDivisionError(ZeroDivisionError):
    pass
