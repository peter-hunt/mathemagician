"""
Path management for mathemagician.
"""

from pathlib import Path

from .myjson import dump, load, JSONDecodeError

__all__ = [
    'MAIN_DIR', 'PROFILES_DIR', 'DATA_DIR', 'SETTINGS_JSON', 'path_init',
    'has_data', 'read_data', 'load_data',
    'has_file', 'read_file', 'load_file', 'write_file', 'dump_file',
]

MAIN_DIR = Path.home() / 'mathemagician'
PROFILES_DIR = MAIN_DIR / 'profiles'
DATA_DIR = Path(__file__).parent / 'data'
SETTINGS_JSON = MAIN_DIR / 'settings.json'


def path_init():
    """Initialize the mathemagician path."""
    if not DATA_DIR.exists():
        raise RuntimeError('data path does not exist')
    if not MAIN_DIR.exists():
        MAIN_DIR.mkdir()
    if not PROFILES_DIR.exists():
        PROFILES_DIR.mkdir()
    if not SETTINGS_JSON.exists():
        SETTINGS_JSON.touch()
        with (DATA_DIR / 'default_settings.json').open() as file:
            default_settings = load(file)
        with SETTINGS_JSON.open('w') as file:
            dump(default_settings, file)

def has_data(*path: str) -> bool:
    """Check if data exists in the data directory."""
    return DATA_DIR.joinpath(*path).exists()


def read_data(*path: str) -> str:
    """Read data from the data directory."""
    with DATA_DIR.joinpath(*path).open() as file:
        return file.read()


def load_data(*path: str) -> dict:
    """Load data from the data directory."""
    try:
        with DATA_DIR.joinpath(*path).open() as file:
            return load(file)
    except JSONDecodeError:
        print(f'Error loading data from {DATA_DIR.joinpath(*path)}')
        return


def has_file(*path: str) -> bool:
    """Check if a file exists in the main directory."""
    return MAIN_DIR.joinpath(*path).exists()


def read_file(*path: str) -> str:
    """Read data from the main directory."""
    with MAIN_DIR.joinpath(*path).open() as file:
        return file.read()


def load_file(*path: str) -> dict:
    """Load data from the main directory."""
    try:
        with MAIN_DIR.joinpath(*path).open() as file:
            return load(file)
    except JSONDecodeError:
        print(f'Error loading data from {MAIN_DIR.joinpath(*path)}')
        return


def write_file(content: str, *path: str):
    """Write data to the main directory."""
    with MAIN_DIR.joinpath(*path).open('w') as file:
        file.write(content)


def dump_file(data: dict, *path: str):
    """Dump data to the main directory."""
    with MAIN_DIR.joinpath(*path).open('w') as file:
        dump(data, file)
