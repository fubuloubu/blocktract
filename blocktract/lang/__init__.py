from .bytes import (
        Bool,
        Bytes32,
        BytesArray,
        String,
    )
from .integers import (
        Num,
        Num256,
    )
from .decimals import (
        Decimal,
    )
from .arrays import (
        FixedArray,
        VariableArray,
    )
from .mappings import (
        Mapping,
    )

types={}
types['bool'] = Bool
types['bytes32'] = Bytes32
types['num'] = Num
types['num256'] = Num256
types['decimal'] = Decimal
types['mapping'] = Mapping
