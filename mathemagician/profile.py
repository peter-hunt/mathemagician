"""
Profile module.

This module contains the Profile class and ProfileInstance class.
The Profile class is a data type that stores information about a profile.
The ProfileInstance class is a class that represents a profile instance.
"""

from numbers import Number

from .cliengine import CliEngine
from .datatype import DataType, Variable
from .items import Item, Empty
from .myjson import dump
from .path import PROFILES_DIR
from .util import (
    interrupt_safe,
    print_text, print_prompt, print_command, print_title,
    print_success, print_error, print_warning, print_info,
    clear, clear_color,
)

__all__ = ['Profile', 'ProfileInstance']


class Profile(DataType):
    """
    Profile data type, used to store profile data.
    """
    variables = [
        Variable('name', str),
        Variable('last_update', Number, lambda: 0),
        Variable('inventory_size', int, lambda: 16),
        Variable(
            'inventory', list, lambda: [Empty() for i in range(16)], False,
            lambda value: [Item.load(item) for item in value],
            lambda value: [item.dump() for item in value],
            lambda value: all(Item.is_valid(item) for item in value),
        ),
    ]

    def save(self):
        """Save the profile."""
        with open(PROFILES_DIR / f'{self.name}.json', 'w') as file:
            dump(self.dump(), file)


class ProfileInstance:
    """
    Profile instance class, used to run a profile.
    """
    engine = CliEngine()
    add_command = engine.add_command
    parse = engine.parse
    commands = engine.commands
    documentation = engine.documentation

    def __init__(self, profile: str):
        self.profile = profile
        self.name = profile.name

    def save(self):
        """Save the profile."""
        self.profile.save()

    @interrupt_safe
    def run(self):
        """Run the profile."""
        print_info(f'Playing on profile: {self.name}')
        self.running = True
        while self.running:
            print_prompt('>> ', end='')
            print_command('', end='')
            command = input()
            clear_color()
            self.parse(self, command)


@ProfileInstance.add_command('exit', 'quit')
def quit_profile(self):
    """Save and exit the profile to the main menu."""
    self.save()
    print_success('Profile saved.')
    self.running = False

@ProfileInstance.add_command('forceexit', 'forcequit')
def forcequit_profile(self):
    """Exit the profile without saving."""
    self.running = False

@ProfileInstance.add_command('help')
def print_help(self):
    """Print the help message."""
    print_info('Available commands:')
    for command in self.commands:
        print_info('- ', end='')
        print_command(command)
        print_info(f'    {self.documentation[command]}')

@ProfileInstance.add_command('clear', 'cls')
def clear_screen(self):
    """Clear the screen."""
    clear()

@ProfileInstance.add_command('save')
def save_profile(self):
    """Save the profile."""
    self.save()
    print_success('Profile saved.')
