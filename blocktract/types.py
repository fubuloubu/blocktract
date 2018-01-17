class Type:
    def __init__(self, value=None):
        self.value = value
    
    @property
    def type(self):
        raise NotImplementedError("Type Not Implemented '{}'".format(self))

class GlobalType(Type):
    pass

global_types={}
global_types['address'] = GlobalType

class ArgType(Type):
    pass

arg_types={}
arg_types['address'] = ArgType
