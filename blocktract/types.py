
# Base class of all types
class vyType:
    _fields = ('compiled_type')
    def __repr__(self):
        return self.__class__.__name__[2:]

    def __str__(self):
        return self.compiled_type

    def can_store(self, _value):
        #TODO change to NotImplementedError
        return True

class vybool(vyType):
    compiled_type = 'bool'

from .utils import module_classes
from .eth.types import classes as eth_types
classes = module_classes(__name__)
classes.update(eth_types)

def get_type(typename: str) -> vyType:
    typename = 'vy' + typename  # Prefix all the classes so we don't get confused
    if typename not in classes.keys():
        raise NotImplementedError("Type '{}' not implemented!".format(typename))
    return classes[typename]
