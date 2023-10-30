from sys import version_info

if version_info < (3, 12):
    raise RuntimeError('mathemagician requires Python 3.12')

from .path import path_init
path_init()

__all__ = []
__modules__ = [
    'achievements', 'cliengine', 'datatype', 'entities', 'game', 'items',
    'path', 'profile', 'util',
]

for module_name in __modules__:
    module = __import__(f'mathemagician.{module_name}', fromlist=['*'])
    __all__.extend(module.__all__)
    for name in module.__all__:
        globals()[name] = module.__dict__[name]
