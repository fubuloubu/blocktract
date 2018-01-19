from .ast import vyBinOp, vyBoolOp


# Convieience class to stop recursion
# Needs to be first so it's not overriden
class Leaf:
    def __new__(self, *args):
        return self

# Comparision Operators
class vyEq(Leaf, vyBinOp):
    pass


class vyNeq(Leaf, vyBinOp):
    pass


class vyGtE(Leaf, vyBinOp):
    pass


class vyLtE(Leaf, vyBinOp):
    pass


class vyLt(Leaf, vyBinOp):
    pass


class vyGt(Leaf, vyBinOp):
    pass


# Math operators
class vyAdd(Leaf, vyBinOp):
    pass


class vyAnd(Leaf, vyBoolOp):
    pass


# Python magic to get all classes in this module
from .utils import module_classes
classes = module_classes(__name__)
