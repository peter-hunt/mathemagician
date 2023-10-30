"""
Data type class, used to create data types with load and dump functions.

Example:
>>> class Point(DataType):
...     variables = [
...         Variable('x', int),
...         Variable('y', int),
...     ]
...
...     def __init__(self, *args, **kwargs):
...         super().__init__(*args, **kwargs)
...
...     def __repr__(self):
...         return f'Point({self.x}, {self.y})'
...
...     def __add__(self, other):
...         return Point(self.x + other.x, self.y + other.y)
...
...     def __sub__(self, other):
...         return Point(self.x - other.x, self.y - other.y)
...
>>> p1 = Point(1, 2)
>>> p2 = Point(3, 4)
>>> p1 + p2
Point(4, 6)
>>> p1 - p2
Point(-2, -2)
>>> p1.dump()
{'x': 1, 'y': 2}
>>> p3 = Point.load(p1.dump())
>>> p3
Point(1, 2)
"""

from types import FunctionType

from .util import print_warning, is_type

__all__ = ['DataType', 'Variable']


class Variable:
    """
    Variable class, used to store information about a variable.
    Used in the DataType class.
    """
    name: str
    typecheck: type
    default_getter: FunctionType
    use_keyword: bool
    load: FunctionType
    dump: FunctionType
    is_valid: FunctionType

    def __init__(self, name: str, typecheck: type,
                 default_getter: FunctionType | None = None, use_keyword: bool = False,
                 load_func: FunctionType | None = None, dump_func: FunctionType | None = None,
                 is_valid_func: FunctionType = None):
        self.name = name
        self.typecheck = typecheck
        self.default_getter = default_getter
        self.use_keyword = use_keyword
        if load_func is not None:
            self.load = load_func
        if dump_func is not None:
            self.dump = dump_func
        if is_valid_func is not None:
            self.is_valid = is_valid_func

    def load(self, value):
        return value

    def dump(self, value):
        return value

    def is_valid(self, obj):
        return is_type(obj, self.typecheck)


class DataType:
    """
    Data type class, used to create data types with load and dump functions.
    """
    variables: list[Variable] = []

    def __init__(self, *args, **kwargs):
        use_default = False
        use_keyword = False
        index = 0
        used_variables = {*()}
        while index < len(args):
            variable = self.variables[index]
            if variable.name in used_variables:
                raise TypeError(f'Duplicate argument: {variable.name}')
            if use_default and variable.default_getter is None:
                raise ValueError(f'Default value must be last: {variable.name}')
            if use_keyword and (not variable.use_keyword or variable.default_getter is None):
                raise ValueError(f'Keyword argument must be last and have a default value: {variable.name}')
            if variable.default_getter is not None:
                use_default = True
            if variable.use_keyword:
                use_keyword = True
            if isinstance(args[index], variable.typecheck):
                setattr(self, variable.name, args[index])
                used_variables.add(variable.name)
            else:
                raise TypeError(f'Invalid value for {variable.name}: {args[index]}')
            index += 1
        for key, value in kwargs.items():
            variable = next((variable for variable in self.variables
                             if variable.name == key), None)
            if variable is None:
                raise TypeError(f'Invalid keyword argument: {key}')
            if variable.name in used_variables:
                raise TypeError(f'Duplicate keyword argument: {variable.name}')
            if isinstance(value, variable.typecheck):
                setattr(self, variable.name, value)
                used_variables.add(variable.name)
            else:
                raise TypeError(f'Invalid value for {variable.name}: {value}')
        for variable in self.variables:
            if variable.name not in used_variables:
                if variable.default_getter is None:
                    raise TypeError(f'Missing argument: {variable.name}')
                setattr(self, variable.name, variable.default_getter())

    @classmethod
    def _load(cls, data):
        """Underlying load function."""
        missing_variables = False
        for variable in cls.variables:
            if variable.name not in data and variable.default_getter is None:
                print_warning(f'Missing variable for loading'
                              f' {cls.__name__}: {variable.name}')
                missing_variables = True
        if not missing_variables:
            return cls(**{variable.name: variable.load(data[variable.name])
                          for variable in cls.variables})

    @classmethod
    def load(cls, data):
        """Default load function."""
        return cls._load(data)

    def _dump(self):
        """Underlying dump function."""
        return {variable.name: variable.dump(getattr(self, variable.name))
                for variable in self.variables}

    def dump(self):
        """Default dump function."""
        return self._dump()

    @classmethod
    def _is_valid(cls, data):
        """Underlying is_valid function."""
        for variable in cls.variables:
            if variable.name in data:
                if not variable.is_valid(data[variable.name]):
                    return False
            elif variable.default_getter is None:
                return False
        return True

    @classmethod
    def is_valid(cls, data):
        """Check if the data is valid."""
        return cls._is_valid(data)

    def __repr__(self) -> str:
        """Return the representation of the object."""
        return f"{self.__class__.__name__}({', '.join(f'{variable.name}={getattr(self, variable.name)!r}' for variable in self.variables)})"
