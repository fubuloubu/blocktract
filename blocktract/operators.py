import ast
import operator

from .ast import AST


class Operator(AST):
    def __init__(self, node: ast.AST, parent: AST):
        self._parent = parent
        self._fields = ()


class Eq(Operator):
    pass


class Neq(Operator):
    pass


class GtE(Operator):
    pass


class LtE(Operator):
    pass


class Lt(Operator):
    pass


class Gt(Operator):
    pass


class BinOp(AST):
    pass

class BoolOp(AST):
    pass

class LtE(Operator):
    pass

class And(AST):
    pass

class Add(AST):
    pass


# Python magic to get all classes in this module
import sys
import inspect
classes = dict(inspect.getmembers(sys.modules[__name__], inspect.isclass))
