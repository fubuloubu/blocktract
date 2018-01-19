from ..types import vyType


class vyaddress(vyType):
    compiled_type = 'address'

    @property
    def balance(self):
        pass
    
    @property
    def codesize(self):# -> Num:
        pass

class vytimedelta(vyType):
    pass

class vytimestamp(vyType):
    pass

from ..utils import module_classes
classes = module_classes(__name__)
