from ..lang.decimal import Decimal
from ..lang.label import MultiLabel

ETHER_LABELS = {
    'wei':          1,
    'kwei':         1e3,
    'ada':          1e3,
    'femtoether':   1e3,
    'mwei':         1e6,
    'babbage':      1e6,
    'picoether':    1e6,
    'gwei':         1e9,
    'shannon':      1e9,
    'nanoether':    1e9,
    'nano':         1e9,
    'szabo':        1e12,
    'microether':   1e12,
    'micro':        1e12,
    'finney':       1e15,
    'milliether':   1e15,
    'milli':        1e15,
    'ether':        1e18,
    'kether':       1e21,
    'grand':        1e21,
    'einstein':     1e21,
    'mether':       1e24,
    'gether':       1e27,
    'tether':       1e30
}

class Ether(Decimal, MultiLabel):
    def __init__(value=None, label="wei"):
        super(Decimal).__init__(value=value)
        super(MultiLabel).__init__(conversion_list=ETHER_LABELS, label=label, truncate=True)
