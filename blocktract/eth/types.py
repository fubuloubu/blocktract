from ..types import uint256


class address(uint256):
    compiled_type = 'address'

    @property
    def balance(self):
        pass
    
    @property
    def codesize(self):# -> Num:
        pass

class timedelta(uint256):
    pass

class timestamp(uint256):
    pass

from ..utils import module_classes
classes = module_classes(__name__)
