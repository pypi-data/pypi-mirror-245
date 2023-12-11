from rich.console import Console
from io import StringIO
from importlib import import_module

__all__ = [
    "import_from_string",
    "rich_format",
]


def import_from_string(dot_path: str) -> object:
    module_path, _, name = dot_path.rpartition(".")
    module = import_module(module_path)
    return getattr(module, name)


def rich_format(a: object, max_width: int = 130) -> str:
    # Create a StringIO buffer to capture the output
    buffer = StringIO()

    # Create a console with the buffer as the output file
    console = Console(file=buffer, force_terminal=True, width=max_width)

    # Use the console to print the object
    with console.capture() as capture:
        console.print(a)

    # Get the string from the buffer
    return capture.get()
