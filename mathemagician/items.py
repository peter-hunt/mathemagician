"""
Item data type, used to store item data.
"""

from .datatype import DataType, Variable

__all__ = ['Item', 'Empty']


class Empty:
    """
    Empty item data type, used as a placeholder for inventory space.
    """


class Item(DataType):
    """
    Item data type, used to store item data.

    Variables:
        name: str
            The name of the item.
    """
    variables = [
        Variable('name', str, lambda: 'ItemName'),
    ]

    @classmethod
    def load(cls, data):
        if data is None:
            return Empty()
        return cls._load(data)

    def dump(self):
        if isinstance(self, Empty):
            return None
        return self._dump()

    @classmethod
    def is_valid(self, data):
        if data is None:
            return True
        return self._is_valid(data)


class Empty(Item):
    """
    Empty item data type, used as a placeholder for inventory space.
    """
    variables = []
