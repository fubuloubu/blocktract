
# Base class of all types
class Type:
    _fields = ('compiled_type',)
    def __repr__(self):
        return self.__class__.__name__[2:]

    def __str__(self):
        return self.compiled_type

    def can_store(self, _value):
        #TODO change to NotImplementedError
        return True

    @property
    def size(self):
        raise NotImplementedError("'{}' doesn't implemented size!".format(self))

class BaseType(Type):
    _size = 32

    @property
    def size(self):
        return self._size

class bool(BaseType):
    compiled_type = 'bool'

class uint256(BaseType):
    compiled_type = 'uint256'

from .utils import module_classes
from .eth.types import classes as eth_types
classes = module_classes(__name__)
classes.update(eth_types)

def get_type(typename: str) -> Type:
    if typename not in classes.keys():
        raise NotImplementedError("Type '{}' not implemented!".format(typename))
    return classes[typename]
