import ast
import operator

from .ast import AST

class BinOp(AST):
    pass

class BoolOp(AST):
    pass

class LtE(AST):
    pass

class Compare(AST):
    pass

class And(AST):
    pass

class Add(AST):
    pass


# Python magic to get all classes in this module
import sys
import inspect
classes = dict(inspect.getmembers(sys.modules[__name__], inspect.isclass))
