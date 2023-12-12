from .lexer import MathPyLexer as _MathPyLexer
from .parser import MathPyParser as _MathPyParser
from .interpreter import MathPyInterpreter as _MathPyInterpreter
from .common import update_program_start_time as _update_program_start_time


def _start_message() -> str:
    from datetime import datetime
    from .common import module_version

    _month_lookup = {
        "01": "Jan",
        "02": "Feb",
        "03": "Mar",
        "04": "Apr",
        "05": "May",
        "06": "Jun",
        "07": "Jul",
        "08": "Aug",
        "09": "Sep",
        "10": "Oct",
        "11": "Nov",
        "12": "Dec",
    }

    date = datetime.now()
    month = _month_lookup.get(f"{date:%m}")

    return f'MathPy {module_version} ({month} {date:%d %Y, %H:%M:%S})\nPlease check documentation for help.'


def run_file(file: open) -> None:
    file_contents = file.read()
    _update_program_start_time()  # update program runtime counter

    mp_lexer = _MathPyLexer(file_contents)
    tokens = mp_lexer.tokenize()

    mp_parser = _MathPyParser(tokens)
    ast = mp_parser.parse()

    mp_interpreter = _MathPyInterpreter()
    mp_interpreter.interpret(ast)


def run_shell() -> None:
    from .types import MathPyNull

    mp_interpreter = _MathPyInterpreter()

    print(_start_message())

    while True:
        try:
            mp_lexer = _MathPyLexer(input('>>> ') + ";")
        except KeyboardInterrupt:
            return

        tokens = mp_lexer.tokenize()

        mp_parser = _MathPyParser(tokens)
        ast = mp_parser.parse_shell()

        output = mp_interpreter.interpret(ast)

        if output is not None and not isinstance(output, MathPyNull):
            print(output)
