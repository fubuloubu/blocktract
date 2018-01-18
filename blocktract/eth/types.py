from ..types import Type


class address(Type):

    @property
    def balance(self):
        pass
    
    @property
    def codesize(self):# -> Num:
        pass

class timedelta(Type):
    pass

class timestamp(Type):
    pass

from ..utils import module_classes
eth_types = module_classes(__name__)
