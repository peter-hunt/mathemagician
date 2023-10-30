"""
Mathemagician game core system.
"""

from .cliengine import CliEngine
from .path import PROFILES_DIR, has_file, load_file
from .profile import Profile, ProfileInstance
from .util import (
    interrupt_safe,
    print_text, print_prompt, print_command, print_title,
    print_success, print_error, print_warning, print_info,
    clear, clear_color,
)

__all__ = ['Game']


class Game:
    """
    Mathemagician game core system.
    """
    engine = CliEngine()
    add_command = engine.add_command
    parse = engine.parse
    commands = engine.commands
    documentation = engine.documentation

    def __init__(self):
        self.num = 1

    @interrupt_safe
    def run(self):
        """Run the game."""
        print_info('Welcome to Mathemagician! Use "help" to get started.')
        self.running = True
        while self.running:
            print_prompt('> ', end='')
            print_command('', end='')
            command = input('')
            clear_color()
            self.parse(self, command)


@Game.add_command('exit', 'quit')
def stop_game(self):
    """Exit the main menu."""
    self.running = False

@Game.add_command('help')
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

@Game.add_command('list')
def list_profiles(self):
    """List all profiles."""
    valid_profiles = []
    for profile in PROFILES_DIR.iterdir():
        if profile.suffix == '.json':
            profile_obj = load_file('profiles', profile.name)
            if profile_obj is None:
                print_warning(f'Invalid JSON file: {profile.stem}')
                continue
            if Profile.is_valid(profile_obj):
                valid_profiles.append((profile_obj['name'], profile.stem))
            else:
                print_warning(f'Invalid profile: {profile.stem}')
    if valid_profiles:
        print_info('Available profiles:')
        for name, filename in valid_profiles:
            print_info(f'- {name} ({filename})')
    else:
        print_info('No profiles found.')

@Game.add_command('new')
def new_profile(self):
    """Create a new profile."""
    print_text('Creating a new profile.')
    print_text('Enter a name for your profile:')
    while True:
        print_prompt('>> ', end='')
        print_command('', end='')
        name = input()
        if not name:
            print_error('Invalid name.')
        elif has_file('profiles', f'{name}.json'):
            print_error('Profile already exists.')
        else:
            break
    profile = Profile(name)
    profile.save()
    print_success(f'Profile created: {name}')

@Game.add_command('enter <profile_name>', 'load <profile_name>',
                  'open <profile_name>', 'run <profile_name>')
def open_profile(self, profile_name: str):
    """Open a profile."""
    if not has_file('profiles', f'{profile_name}.json'):
        print_error('Profile does not exist.')
        return
    profile_obj = load_file('profiles', f'{profile_name}.json')
    if profile_obj is None:
        print_error('Invalid profile.')
        return
    profile_instance = ProfileInstance(Profile.load(profile_obj))
    profile_instance.run()
