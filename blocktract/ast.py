import ast

from .types import Type
from .context import Context


# Base class of all Vyper AST Types
class AST:
    def __init__(self, node: ast.AST, parent=None):
        raise NotImplementedError("Class '{}' is not implemented!".format(type(self).__name__))

    @property
    def context(self):
        if hasattr(self, '_context'):
            return self._context
        if hasattr(self, '_parent'):
            return self._parent.context
        raise ValueError("I have no context!")


class Module(AST):
    # Starts Context
    def __init__(self, node: ast.AST, parent: AST=None):
        self._parent = parent
        self._fields = ('name','state','methods')
        self._context = parent.context if parent else Context()
        self.name = 'self' #else Module in Module?
        self.context.new_scope(self.name)
        # Parse State schema first
        while len(node.body) > 0:
            n = node.body.pop()
            if isinstance(n, ast.AnnAssign):
                self.context.new(Variable(n))
            else:
                break
        # Then parse methods
        self.methods = []
        while len(node.body) > 0:
            n = node.body.pop()
            if isinstance(n, ast.AnnAssign):
                raise ValueError("State definitions must come before any methods!")
            elif isinstance(n, ast.FunctionDef):
                method_added = True
                self.methods.append(Method(n, self))
            else:
                raise NotImplementedError("Class '{}' not implemented for 'Module'!".format(n))

    @property
    def state(self):
        return self.context.get_scope(self.name)


class Variable(AST):
    def __init__(self, node: ast.AST):
        # Doesn't require parent or context, is leaf node of AST
        self._fields = ('name','type','value')
        self.name = node.target.id
        self.type = node.annotation.id #TODO Load type using lookup from types.py
        self.value = None #TODO Validate value before storing, instead of storing in type


class Method(AST):
    # Changes Context
    def __init__(self, node: ast.AST, parent: AST):
        self._parent = parent
        self._fields = ('name','args','body','decorators')
        self.name = node.name
        self.context.new_scope(scope=self.name)
        for n in node.args.args:
            self.context.new(Variable(n))
        self.body = [transform(n, parent=self) for n in node.body]
        self.decorators = [n.id for n in node.decorator_list]

    @property
    def args(self) -> list:
        return self.context.scope(self.name)


class If(AST):
    # Changes Context
    pass


class For(AST):
    # Changes Context
    pass


class Attribute(AST):
    # This is variable reference, so return the variable instead
    def __new__(self, node: ast.AST, parent: AST):
        if isinstance(node, ast.Name):
            return parent.context.get(node.id)
        if isinstance(node, ast.Attribute):
            return parent.context.get(node.attr, scope=node.value.id)
        raise ValueError("Can't use '{}' here!".format(node))


# Helper to determine if node represents statement(s) or a variable reference
def parse_statement(node: ast.AST, parent: AST) -> AST:
        if isinstance(node.value, ast.AST):
            return transform(node.value, parent=parent)
        else:
            return Attribute(node, parent)


class Assign(AST):
    def __init__(self, node: ast.AST, parent: AST):
        self._parent = parent
        self._fields = ('var', 'stmt')

        # To avoid self-referential first assignment,
        # we parse variable after parsing statement
        self.stmt = parse_statement(node, parent)
        var = Variable(node.targets[0])
        if not self.context.has(var.name):
            # Variable not previously defined, so add it
            self.context.add(var)
        self.var = self.context.get(var.name)


class Return(AST):
    def __init__(self, node: ast.AST, parent: AST):
        self._parent = parent
        self._fields = ('returns')
        self.returns =  parse_statement(node, parent)


# Python magic to get all classes in this module
import sys
import inspect
from .operators import classes as operators
classes = dict(inspect.getmembers(sys.modules[__name__], inspect.isclass))
classes.update(operators)


# Transform Python AST Node to Vyper AST Node automagically
def transform(node: ast.AST, parent: AST=None) -> AST:
    class_name = type(node).__name__
    if class_name in ['Load', 'Store']:
        return None
    if class_name not in classes.keys():
        raise NotImplementedError("Class '{}' is not implemented!".format(class_name))
    return classes[class_name](node, parent)
