from ..types import (
        BaseType,
    )

# Stores less than 32 bytes
class Bytes(BaseType):
    def _parse_type(self):
        if self.value:
            assert self._storable(self.value), \
                    "Value '{}' exceeds capacity for type '{}'".\
                    format(self.value, repr(self))
        else:
            self.value = 0

    @property
    def bits(self) -> int:
        if not hasattr(self, '_bits'):
            raise NotImplementedError("Cannot determine number of bits!")
        assert self._bits in 8*[1, 2, 4, 8, 16, 32], "Size is not appropiate!"
        return self._bits

    @property
    def bytes(self) -> int:
        return self.bits/8

    def _storable(self, value) -> bool:
        if isinstance(value, bytes):
            # hex() converts to nibbles (a nibble is 4 bits)
            return 4*len(value.hex()) <= self.bits 
        if isinstance(value, int):
            if value < 0:
                return False
            return value.bit_length() <= self.bits
        raise ValueError("Cannot store literal '{}'".format(type(value).__class__))

class Bytes32(Bytes):
    _bits = 256 # Maximimum number of bits

class BytesArray:
    pass

class String:
    pass

class Bool(Bytes):
    _bits = 8 # Minimum number of bits (1 byte)

    def _storable(self, value):
        return isinstance(value, bool)
