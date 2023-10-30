"""
A command engine for a command line interface.

Usage:
>>> from .cliengine import CliEngine
>>>
>>> class Game:
...     engine = CliEngine()
...     add_command = engine.add_command
...     parse = engine.parse
...
...     def __init__(self):
...         self.num = 1
...
...     def run(self):
...         self.running = True
...         while self.running:
...             command = input('> ')
...             self.parse(self, command)
...
>>> @Game.add_command('exit')
...     def stop(self):
...         self.running = False
...
>>> @Game.add_command('print')
...     def print_num(self):
...         print(self.num)
...
>>> @Game.add_command('set <num:int>')
...     def set_num(self, num: int):
...         self.num = num
...
>>> game = Game()
>>> game.run()
> print
1
> set 2
> print
2
> exit
"""

from re import fullmatch
from types import FunctionType

from .util import print_warning

__all__ = ['parse_value', 'CliEngine']


def parse_value(value: str, arg_type: str) -> any:
    """
    Parse a string and return the value if it matches the type.
    Return None if the string does not match the type.
    Raise a ValueError if the type is invalid.

    Valid types:
    - str
    - bool
    - int
    - float
    - number (int or float)

    >>> parse_value('hello', 'str')
    'hello'
    >>> parse_value('true', 'bool')
    True
    >>> parse_value('1', 'int')
    1
    >>> parse_value('1.0', 'float')
    1.0
    >>> parse_value('1', 'number')
    1
    >>> parse_value('1.0', 'number')
    1.0
    >>> parse_value('1.0', 'invalid')
    Traceback (most recent call last):
        ...
    ValueError: Invalid argument type: invalid
    >>> parse_value('1.0', 'int')
    >>> parse_value('1', 'float')
    """
    try:
        match arg_type:
            case 'str':
                return value
            case 'bool':
                return {'true': True, 'false': False}.get(value.lower(), None)
            case 'int':
                return int(value)
            case 'float':
                return float(value)
            case 'number':
                return float(value) if '.' in value else int(value)
    except ValueError:
        return
    raise ValueError(f'Invalid argument type: {arg_type}')


class CliEngine:
    """
    A command engine for a command line interface.
    """
    def __init__(self) -> None:
        """Initialize the command engine."""
        self.commands: dict[str, FunctionType] = {}
        self.documentation: dict[str, str] = {}

    def add_command(self, *commands) -> None:
        """Decorator to add a command to the subclass."""
        def decorator(func: FunctionType) -> FunctionType:
            for command in commands:
                self.commands[command] = func
                self.documentation[command] = func.__doc__ or ''
            return func
        return decorator

    def parse(self, instance: any, string: str) -> None:
        """Parse a string and execute the corresponding command."""
        # Check if the string is empty
        if string == '':
            return
        # Check if the string is a comment
        if string.strip().startswith('#'):
            return
        # Check if the string is a command
        for command in self.commands:
            kwargs = self._parse(command, string)
            if kwargs is not None:
                self.commands[command](instance, **kwargs)
                break
        else:
            print_warning('Unknown command. Use "help" for a list of commands.')

    @staticmethod
    def _parse(format_: str, string: str) -> None | tuple[any]:
        """Parse a string and return the arguments if the format matches."""
        # Split the format and string into words
        format_words = format_.split()
        string_words = string.split()

        # Check that the number of words match
        if len(format_words) > len(string_words):
            return

        # Check that each word matches the format
        args = {}
        string_words.extend([None] * (len(format_words) - len(string_words)))
        for format_word, string_word in zip(format_words, string_words):
            # Check for argument
            if fullmatch(r'<\w+(:\w+)?>|\[\w+(:\w+)?\]', format_word):
                if format_word.startswith('[') and string_word is None:
                    continue

                word = format_word[1:-1]
                if (colon_count := word.count(':')) > 1:
                    print_warning(f'Invalid argument format: {format_word}'
                                  f' in command {format_}')
                    return

                arg_name, arg_type = word.split(':') if colon_count == 1 else (word, 'str')
                if arg_name in args:
                    print_warning(f'Duplicate argument: {arg_name}'
                                  f' in command {format_}')
                    return
                args[arg_name] = parse_value(string_word, arg_type)

            # Check for plain text
            elif format_word != string_word:
                return

        return args
