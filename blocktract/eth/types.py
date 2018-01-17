from ..lang.bytes import (
        Bytes,
    )
from ..lang.integers import (
        Num,
    )

class Address(Bytes):

    def _storable(self, value):
        # Literals can only be integers of length 20 bytes or less
        if isinstance(value, int) and super.storable(value):
            return value.bit_length() <= 2**20
        return False

    def __repr__(self):
        return "{}(0x{:02x})".format(self._type, self.value)

    @property
    def balance(self):
        pass
    
    @property
    def codesize(self):# -> Num:
        pass

class Timedelta(Num):
    pass

class Timestamp(Num):
    pass

eth_types = {}
eth_types['address'] = Address
eth_types['timedelta'] = Timedelta
eth_types['timestamp'] = Timestamp
