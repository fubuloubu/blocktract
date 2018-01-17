from .bytes import Bytes

# Basic Integer Type
# NOTE: DO NOT USE DIRECTLY
class Integer(Bytes):

    @property
    def signed(self) -> bool:
        if not hasattr(self, '_signed'):
            raise NotImplementedError("Cannot determine signed or unsigned!")
        return self._signed
    
    # Range of integer
    @property
    def range(self) -> (int, int):
        int_signed = int(self.signed)
        min_val = -int_signed*2**(self.bits-int_signed)
        max_val = 2**(self.bits-int_signed)
        return (min_val, max_val)

    def _storable(self, value) -> bool:
        if isinstance(value, int):
            min_val, max_val = self.range
            return min_val <= value < max_val
        return False # Can't store non-integers

class Num(Integer):
    _signed = True
    _bits = 128 # bits

class Num256(Integer):
    _signed = False
    _bits = 256 # bits
