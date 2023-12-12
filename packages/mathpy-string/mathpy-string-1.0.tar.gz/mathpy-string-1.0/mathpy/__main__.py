from .shell_commands import run, shell
from sys import argv

default_command = "shell"

command = argv[1] if len(argv) > 1 else default_command  # argv[0] is current path
arguments = argv[2:]

if command == 'run':
    run(*arguments)

elif command == 'shell':
    shell(*arguments)

else:
    print(f'Unknown command {command !r}')