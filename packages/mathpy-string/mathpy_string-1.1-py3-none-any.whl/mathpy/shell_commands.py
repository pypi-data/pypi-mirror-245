from . import run_file, run_shell
from .common import current_time


def run(path: str, runtime_message: str = "false", *args):
    try:
        file = open(path, 'rt', encoding='utf-8')
    except FileNotFoundError:
        print(f'File {path !r} not found.')
    else:
        run_file(file)
        if runtime_message == "true":
            print(f"\n\nSuccessfully ran {path !r} (Time Elapsed: {current_time()}ms)\n")


def shell(*args) -> None:
    run_shell()
