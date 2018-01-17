# Base class of all types
class Type:
    def __init__(self, value=None):
        self.value = value

    def __repr__(self):
        return "{}({})".format(self._type, self.value)
    
    @property
    def _type(self):
        raise NotImplementedError("Type Not Implemented '{}'".format(self))

# All 32-byte types inherit from this one
class BaseType(Type):
    @property
    def _type(self):
        return type(self).__name__.lower()

# All types that can be globals inherit from this one
class GlobalType(Type):
    pass

# All types that can be arguments or return types inherit from this one
class ArgType(Type):
    pass

class Address(BaseType, GlobalType, ArgType):
    pass

global_types={}
global_types['address'] = Address

arg_types={}
arg_types['address'] = Address
