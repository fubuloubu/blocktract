from ..lang.bytes import (
        Bytes,
    )
from ..lang.integers import (
        Num,
    )

class address:#(Bytes):

    def __repr__(self):
        return "{}(0x{:20x})".format(self._type, self.value)

    @property
    def balance(self):
        pass
    
    @property
    def codesize(self):# -> Num:
        pass

class timedelta(Num):
    pass

class timestamp(Num):
    pass

eth_types = {}
eth_types['address'] = address
eth_types['timedelta'] = timedelta
eth_types['timestamp'] = timestamp
