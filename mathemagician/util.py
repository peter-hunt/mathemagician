"""
Utility functions.
"""

from sys import stdout
from types import FunctionType, GenericAlias, UnionType

from .path import DATA_DIR, load_file, load_data

__all__ = [
    'is_type', 'interrupt_safe',
    'print_text', 'print_prompt', 'print_command', 'print_title',
    'print_success', 'print_error', 'print_warning', 'print_info',
    'load_color', 'load_color_scheme',
    'COLOR_SCHEME',
    'clear', 'clear_color',
]


def is_type(obj: object, checktype: type) -> bool:
    """Check if an object is of a certain type."""
    if isinstance(checktype, type | UnionType):
        return isinstance(obj, checktype)
    elif checktype is any:
        return True
    elif isinstance(checktype, GenericAlias):
        if not is_type(obj, checktype.__origin__):
            return False
        if checktype.__origin__ is tuple:
            if len(checktype.__args__) == 2 and checktype.__args__[1] is ...:
                for _obj in obj:
                    if not is_type(_obj, checktype.__args__[0]):
                        return False
                return True
            if ... in checktype.__args__:
                raise TypeError('Invalid type: Ellipsis must be the last type in a'
                                ' two argument tuple.')
            if len(checktype.__args__) != len(obj):
                return False
            for _obj, _checktype in zip(obj, checktype.__args__):
                if not is_type(_obj, _checktype):
                    return False
            return True
        elif checktype.__origin__ is list:
            if len(checktype.__args__) != 1:
                raise TypeError('Invalid type: List must have one argument.')
            for _obj in obj:
                if not is_type(_obj, checktype.__args__[0]):
                    return False
            return True
        elif checktype.__origin__ is set:
            if len(checktype.__args__) != 1:
                raise TypeError('Invalid type: Set must have one argument.')
            for _obj in obj:
                if not is_type(_obj, checktype.__args__[0]):
                    return False
            return True
        elif checktype.__origin__ is dict:
            if len(checktype.__args__) != 2:
                raise TypeError('Invalid type: Dict must have two arguments.')
            for key, value in obj.items():
                if not is_type(key, checktype.__args__[0]):
                    return False
                if not is_type(value, checktype.__args__[1]):
                    return False
            return True
        else:
            raise TypeError(f'Invalid type: {checktype}')
    else:
        raise TypeError(f'Invalid type: {checktype}')


def interrupt_safe(func: FunctionType) -> FunctionType:
    """Decorator to catch keyboard interrupts."""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyboardInterrupt:
            print('Keyboard interrupt.')
    return wrapper


def load_color(color: str) -> tuple[int, int, int]:
    """Load a color as RGB values from a string."""
    if color.startswith('#'):
        color = color[1:]
    if len(color) == 3:
        color = ''.join(char * 2 for char in color)
    if len(color) != 6:
        raise ValueError('Invalid color.')
    return tuple(int(color[i:i + 2], 16) for i in range(0, 6, 2))


COLOR_SCHEME = {}
print_text = print
print_prompt = print
print_command = print
print_title = print
print_success = print
print_error = print
print_warning = print
print_info = print


def generate_printer(name: str, color: str):
    def printer(*args, sep=' ', end='\n', file=None, flush=False) -> None:
        """Print text."""
        if file is None:
            file = stdout
        file.write(color + sep.join(f'{arg}' for arg in args) + end)
        if flush:
            file.flush()
    printer.__name__ = name
    return printer


def load_color_scheme(color_scheme: str):
    """Load a color scheme."""
    global COLOR_SCHEME, \
        print_text, print_prompt, print_command, print_title, \
        print_success, print_error, print_warning, print_info
    if not (DATA_DIR / 'color_schemes' / f'{color_scheme}.json').exists():
        print_warning(f'Color scheme {color_scheme} does not exist.')
        return
    COLOR_SCHEME = load_data('color_schemes', f'{color_scheme}.json')
    text_color = load_color(COLOR_SCHEME['text'])
    text_format = f'\x1b[38;2;{text_color[0]};{text_color[1]};{text_color[2]}m'
    print_text = generate_printer('print_text', text_format)
    prompt_color = load_color(COLOR_SCHEME['prompt'])
    prompt_format = f'\x1b[38;2;{prompt_color[0]};{prompt_color[1]};{prompt_color[2]}m'
    print_prompt = generate_printer('print_prompt', prompt_format)
    command_color = load_color(COLOR_SCHEME['command'])
    command_format = f'\x1b[38;2;{command_color[0]};{command_color[1]};{command_color[2]}m'
    print_command = generate_printer('print_command', command_format)
    title_color = load_color(COLOR_SCHEME['title'])
    title_format = f'\x1b[38;2;{title_color[0]};{title_color[1]};{title_color[2]}m'
    print_title = generate_printer('print_title', title_format)
    success_color = load_color(COLOR_SCHEME['success'])
    success_format = f'\x1b[38;2;{success_color[0]};{success_color[1]};{success_color[2]}m'
    print_success = generate_printer('print_success', success_format)
    error_color = load_color(COLOR_SCHEME['error'])
    error_format = f'\x1b[38;2;{error_color[0]};{error_color[1]};{error_color[2]}m'
    print_error = generate_printer('print_error', error_format)
    warning_color = load_color(COLOR_SCHEME['warning'])
    warning_format = f'\x1b[38;2;{warning_color[0]};{warning_color[1]};{warning_color[2]}m'
    print_warning = generate_printer('print_warning', warning_format)
    info_color = load_color(COLOR_SCHEME['info'])
    info_format = f'\x1b[38;2;{info_color[0]};{info_color[1]};{info_color[2]}m'
    print_info = generate_printer('print_info', info_format)


def clear():
    """Clear the screen."""
    print('\x1b[2J\x1b[H', end='')


def clear_color():
    """Clear the color."""
    print('\x1b[0m', end='')


settings = load_file('settings.json')
color_scheme = settings['color_scheme']
if not (DATA_DIR / 'color_schemes' / f'{color_scheme}.json').exists():
    color_scheme = 'vanilla'
load_color_scheme(color_scheme)

