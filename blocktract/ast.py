import ast

from .debug import debug
from .types import vyType, get_type
from .context import Context


# Base class of all vyper AST Types
class vyAST:
    def __init__(self, node: ast.AST, parent=None):
        raise NotImplementedError("Class '{}' is not implemented!".format(type(self).__name__))

    @property
    def context(self):
        if hasattr(self, '_context'):
            return self._context
        if hasattr(self, '_parent'):
            return self._parent.context
        raise ValueError("I have no context!")


class vyModule(vyAST):
    _fields = ('name','state','methods')
    # Starts Context
    def __init__(self, node: ast.AST, parent: vyAST=None):
        debug(self, "body: " + str(node.body))
        self._parent = parent
        self._context = parent.context if parent else Context()
        self.name = 'self' #else Module in Module?
        self.context.new_scope(self.name)
        # Parse State schema first
        body = node.body
        while len(body) > 0:
            n = body.pop(0)
            debug(self, "state: " + str(n))
            if isinstance(n, ast.AnnAssign):
                self.context.new(vyVariable(n))
            else:
                break
        # Then parse methods
        self.methods = []
        while len(node.body) > 0:
            n = body.pop(0)
            debug(self, "method: " + str(n))
            if isinstance(n, ast.AnnAssign):
                raise ValueError("State definitions must come before any methods!")
            elif isinstance(n, ast.FunctionDef):
                method_added = True
                self.methods.append(vyMethod(n, self))
            else:
                raise NotImplementedError("Feature '{}' not implemented for 'Module'!".format(n))

    @property
    def state(self) -> list:
        return [v for v in self.context.get_scope(self.name).values()]

class vyVariable(vyAST):
    _fields = ('name','type')
    def __init__(self, node: ast.AST):
        # Doesn't require parent or context, is leaf node of AST
        if isinstance(node, ast.arg):
            self.name = node.arg
        elif isinstance(node, ast.AnnAssign):
            self.name = node.target.id
        else:
            raise NotImplementedError("Variable can't parse '{}'!".format(node))

        # Determine type and initialize value
        self.type = get_type(node.annotation.id) #TODO Load type using lookup from types.py


class vyLiteral(vyAST):
    _fields = ('type','value')
    def __init__(self, typename: str, _value=None):
        # Determine type and initialize value
        self.type = get_type(typename)
        self.set_value(_value)

    def set_value(self, value):
        # Validate value before setting it
        if not True:#self.type.can_store(value):
            raise ValueError("Failed to validate type!")
        self._value = value
    
    @property
    def value(self):
        return self._value


class vyMethod(vyAST):
    _fields = ('name','args','body','decorators')
    # Changes Context
    def __init__(self, node: ast.AST, parent: vyAST):
        self._parent = parent
        self.name = node.name
        self.context.new_scope(scope=self.name)
        self._arg_list = []  # Keep order of list
        for n in node.args.args:
            var = vyVariable(n)
            self.context.new(var)
            self._arg_list.append(var.name)
        self.body = [transform(n, parent=self) for n in node.body]
        self.decorators = tuple([n.id for n in node.decorator_list])

    @property
    def args(self) -> list:
        var_list = self.context.get_scope(self.name)
        return [var_list[v] for v in self._arg_list]


class vyIf(vyAST):
    # Changes Context
    pass


class vyFor(vyAST):
    # Changes Context
    pass


class vyAttribute(vyAST):
    # This is variable reference, so return the variable instead
    def __new__(self, node: ast.AST, parent: vyAST):
        if isinstance(node, ast.Name):
            return parent.context.get(node.id)
        if isinstance(node, ast.Attribute):
            return parent.context.get(node.attr, scope=node.value.id)
        raise ValueError("Can't use '{}' here!".format(node))


# Helper to determine if node represents statement(s) or a variable reference
def parse_statement(node: ast.AST, parent: vyAST) -> vyAST:
        if isinstance(node, ast.Attribute) or isinstance(node, ast.Name):
            return vyAttribute(node, parent)
        if hasattr(node, 'value'):
            return transform(node.value, parent=parent)
        return transform(node, parent=parent)


class vyAssign(vyAST):
    _fields = ('var', 'stmt')
    def __init__(self, node: ast.AST, parent: vyAST):
        self._parent = parent

        # Assign can either be:
        # - 'existing = stmt'
        # - 'new: type' which default value
        # - 'new: type = literal'

        # To avoid self-referential first assignment,
        # we parse variable after parsing statement
        if isinstance(node.value, ast.NameConstant):
            self.stmt = vyLiteral(node.value)
        else:
            self.stmt = parse_statement(node.value, parent)

        # Now do the assignment
        if len(node.targets) != 1:
            raise ValueError("Cannot have more than 1 targets for assignment!")
        varname = node.targets[0].attr
        varscope = node.targets[0].value.id
        if not self.context.has(varname, scope=varscope):
            # Variable not previously defined, so add it
            self.context.add(vyVariable(node.targets[0]))
        self.var = self.context.get(varname, scope=varscope)


class vyReturn(vyAST):
    _fields = ('returns',)
    def __init__(self, node: ast.AST, parent: vyAST):
        self._parent = parent
        self.returns =  parse_statement(node, parent)


class vyAssert(vyAST):
    _fields = ('stmt',)
    def __init__(self, node: ast.AST, parent: vyAST):
        self._parent = parent
        self.stmt = transform(node.test, parent=parent)


class vyOperator(vyAST):
    _fields = ('operator',)


# Binary Operator Meta-class
class vyBinOp(vyOperator):
    _fields = ('operator','left','right')
    def __init__(self, node: ast.AST, parent: vyAST):
        self._parent = parent
        self.operator = transform(node.op, parent=parent)
        self.left = parse_statement(node.left, parent)
        self.right = parse_statement(node.right, parent)


class vyBoolOp(vyBinOp):
    def __new__(self, node: ast.AST, parent: vyAST):
        if len(node.values) != 2:
            raise ValueError("Cannot have more than 2 arguments!")
        node.left = node.values[0]
        node.right = node.values[1]
        return vyBinOp(node, parent)

class vyCompare(vyBinOp):
    def __new__(self, node: ast.AST, parent: vyAST):
        self._parent = parent
        if len(node.ops) != 1:
            raise ValueError("Cannot have more than 1 operator!")
        node.op = node.ops[0]
        if len(node.comparators) != 1:
            raise ValueError("Cannot have more than 1 comparator!")
        node.right = node.comparators[0]
        return vyBinOp(node, parent)


class vylist(vyAST):
    pass
    # We have two different kinds of lists, so route appropiately
    #def __new__(self, node: ast.AST, parent: vyAST):


from .utils import module_classes
from .operators import classes as operators
classes = module_classes(__name__)
classes.update(operators)

# Transform Python AST Node to vyper AST Node automagically
def transform(node: ast.AST, parent: vyAST=None) -> vyAST:
    class_name = type(node).__name__
    if class_name in ['Load', 'Store']:
        return None
    class_name = "vy" + class_name  # Prefix all the classes so we don't get confused
    if class_name not in classes.keys():
        raise NotImplementedError("Class '{}' is not implemented!".format(class_name))
    return classes[class_name](node, parent)
