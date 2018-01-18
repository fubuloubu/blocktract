from ..types import vyType


class address(vyType):

    @property
    def balance(self):
        pass
    
    @property
    def codesize(self):# -> Num:
        pass

class timedelta(vyType):
    pass

class timestamp(vyType):
    pass

from ..utils import module_classes
eth_types = module_classes(__name__)
