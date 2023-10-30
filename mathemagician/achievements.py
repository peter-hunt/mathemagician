"""
Achievements module, used to store acheivement data.
"""

from .datatype import DataType, Variable

__all__ = ['Acheivement']


class Acheivement(DataType):
    """
    Acheivement data type, used to store acheivement data.

    Variables:
        name: str
            The name of the acheivement.
        timestamp: int
            The timestamp of the acheivement.
    """
    variables = [
        Variable('name', str, lambda: 'AcheivementName'),
        Variable('timestamp', int, lambda: 0),
    ]
