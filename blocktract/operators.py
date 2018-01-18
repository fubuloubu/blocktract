from .ast import BinOp


# Comparision Operators
class Eq(BinOp):
    pass


class Neq(BinOp):
    pass


class GtE(BinOp):
    pass


class LtE(BinOp):
    pass


class Lt(BinOp):
    pass


class Gt(BinOp):
    pass


# Math Operators Meta-class
class MathOp(BinOp):
    pass


class Add(MathOp):
    pass


# Boolean Operators Meta-class
class BoolOp(BinOp):
    pass


class And(BoolOp):
    pass


# Python magic to get all classes in this module
import sys
import inspect
classes = dict(inspect.getmembers(sys.modules[__name__], inspect.isclass))
