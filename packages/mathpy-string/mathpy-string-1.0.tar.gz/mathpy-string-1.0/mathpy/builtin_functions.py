from .types import MathPyString, MathPyInt, MathPyFloat, MathPyNull, MathPyBool, MathPyList
from .interpreter import RuntimeResult
from .errors import MathPyTypeError
from random import random


def bind(instance, function, name: str = None):
    name = name if name is not None else function.__name__
    setattr(instance, name, function.__get__(instance, instance.__class__))


def function_wrapper(fnc):
    def function_call(self, *args):
        function_output = fnc(*args)

        return RuntimeResult(return_value=function_output)  # wrap in RuntimeResult

    return function_call


# ----------- Builtin Function Implementations ----------- :
def builtin_function_log(*args):
    values = map(lambda x: x.mathpy_repr(), args)
    print(*values)
    return MathPyNull()


def builtin_function_str(value, *args):
    if args:
        raise MathPyTypeError(f'str() takes 1 argument, {len(args) + 1} given.')

    return MathPyString(str(value))


def builtin_function_int(value, *args):
    if args:
        raise MathPyTypeError(f'int() takes 1 argument, {len(args) + 1} given.')

    return MathPyInt(int(value))


def builtin_function_float(value, *args):
    if args:
        raise MathPyTypeError(f'float() takes 1 argument, {len(args) + 1} given.')

    return MathPyFloat(float(value))


def builtin_function_bool(value, *args):
    if args:
        raise MathPyTypeError(f'bool() takes 1 argument, {len(args) + 1} given.')

    return MathPyBool(bool(value))


def builtin_function_random(*args):
    if args:
        raise MathPyTypeError(f'int() takes no arguments, {len(args)} given.')

    return MathPyFloat(random())


def builtin_function_range(*args):
    if len(args) > 3:
        raise MathPyTypeError(f'range() takes 3 arguments, {len(args)} given.')

    if any(not isinstance(value, MathPyInt) for value in args):
        raise MathPyTypeError(f'range() only takes integer arguments.')

    range_splice = map(lambda x: int(x), args)
    int_range = range(*range_splice)

    return MathPyList(map(lambda x: MathPyInt(x), int_range))


builtins_list = (
    builtin_function_log,
    builtin_function_str, builtin_function_int, builtin_function_bool, builtin_function_float,
    builtin_function_random, builtin_function_range,
)

builtin_functions = {
    fnc.__name__[17:]: function_wrapper(fnc)  # [17:] to remove "builtin_function_"
    for fnc in builtins_list
}
