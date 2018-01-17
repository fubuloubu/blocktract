# Base class of all types
class Type:
    def __init__(self, name: str, namespace: str=None, value=None):
        # For pretty-printing
        self.name = name
        self.namespace = namespace

        self.value = value
        self._parse_type()

    def __str__(self):
        return "'" + (self.namespace + "." + self.name if self.namespace else self.name) + "'"

    def __repr__(self):
        return "{}({})".format(self._type, self.value)

    def _parse_type(self):
        raise NotImplementedError("parse_type Not Implemented '{}'".format(self))

    def compute_type(self, right):
        if self.return_type is right.return_type:
            return self.return_type
        raise ValueError("Types of {} and {} don't match!".format(left, right))
    
    @property
    def _type(self):
        return type(self).__name__.lower()

    @property
    def return_type(self):
        return self

# All 32-byte types inherit from this one
class BaseType(Type):
    pass


def compute_type(left: Type, right: Type):
    return left.compute_type(right)

from .lang import types as lang_types
from .eth.types import eth_types

# All types that can be globals inherit from this one
class GlobalType(Type):
    pass

global_types={}
global_types.update(lang_types)
global_types.update(eth_types)

# All types that can be arguments or return types inherit from this one
class LocalType(Type):
    pass

local_types={}
local_types.update(lang_types)
del local_types['mapping'] # Mappings can't be a local
local_types.update(eth_types)
