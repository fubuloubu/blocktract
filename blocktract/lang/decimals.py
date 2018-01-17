from math import log

from .integers import Integer

# Basic Fixed Point Type
# NOTE: DO NOT USE DIRECTLY
class FixedPt(Integer):
    _signed = True

    # Half the bytes are used for storing the integer portion
    # the other half for storing decimal portion
    @property
    def decimal_bytes(self) -> int:
        return super.bytes

    @property
    def bytes(self) -> int:
        return super.bytes + self.decimal_bytes

    @property
    def decimals(self) -> int:
        if not hasattr(self, '_decimals'):
            raise NotImplementedError("Cannot determine signed or unsigned!")
        return self._deicmals

    def _storable(self, value) -> bool:
        if super._storable(value):
            return log(10**self.decimals, 2) < 8*self.decimal_bytes
        return False

class Decimal(FixedPt):
    _bits = 128 # integer storage size
    _decimals = 10 # decimal places
