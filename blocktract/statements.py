import ast
from .types import Type, local_types, compute_type
from .context import Context
from .operators import parse_operator

class StmtType:
    def __init__(self, statement, context: Context):
        self._statement = statement
        self._context = context

        # Debug print
        self._py_ast = type(self._statement).__name__
        self._lineno = self._statement.lineno
        self._col_offset = self._statement.col_offset

        # Call parsing statement
        self._parse_statement()

    def _parse_statement(self):
        raise NotImplementedError("Statement Not Implemented '{}'".format(self._py_ast))

    def __repr__(self):
        return "{} @ ({}, {})".format(self._py_ast, self._lineno, self._col_offset)

    @property
    def return_type(self):
        return None


class AssertStmt(StmtType):
    def _parse_statement(self):
        self.test = parse_statement(self._statement.test, self._context)
    
    def __repr__(self):
        return "{'assert': " + str(self.test) + "}"

class AssignStmt(StmtType):
    def _parse_statement(self):
        target = self._statement.targets[0]
        # TODO: Handle missing from current scope by adding variable
        self.target = self._context.get(target.attr, namespace=target.value.id)
        if isinstance(self._statement.value, ast.NameConstant):
            self.value = local_types[self.target._type]("literal", value=self._statement.value.value)
        else:
            self.value = parse_statement(self._statement.value, self._context)
    
    def __repr__(self):
        return "{'assign': {" + str(self.target) + ": " + str(self.value) + "}}"

class ReturnStmt(StmtType):
    def _parse_statement(self):
        target = self._statement.value
        self.returns = parse_statement(self._statement.value, self._context)

    @property
    def return_type(self):
        return self.returns.return_type

    def __repr__(self):
        return "{'return': " + str(self.returns) + "}"

class BinOpStmt(StmtType):
    def _parse_statement(self):
        self.operator = parse_operator(self._statement.op)
        self.left = parse_statement(self._statement.left, self._context)
        self.right = parse_statement(self._statement.right, self._context)

    def __repr__(self):
        return "{'compare': {'left': "+ str(self.left) + \
                ", 'op': " + str(self.operator) + \
                ", 'right': "+ str(self.right) + "}}"

    def compute_type(self, right: Type):
        return compute_type(self.left, self.right)

    @property
    def return_type(self):
        return compute_type(self.left, self.right)

class CompareStmt(BinOpStmt):
    def _parse_statement(self):
        assert len(self._statement.ops) == 1, "Only supports one operator!"
        self.operator = parse_operator(self._statement.ops[0])
        self.left = parse_statement(self._statement.left, self._context)
        assert len(self._statement.comparators) == 1, "Only supports one comparator!"
        self.right = parse_statement(self._statement.comparators[0], self._context)

class BoolOpStmt(BinOpStmt):
    def _parse_statement(self):
        self.operator = parse_operator(self._statement.op)
        assert len(self._statement.values) == 2, "Only supports binary operations"
        self.left = parse_statement(self._statement.values[0], self._context)
        self.right = parse_statement(self._statement.values[1], self._context)

statement_types={}
statement_types[ast.Assert] = AssertStmt
statement_types[ast.Assign] = AssignStmt
statement_types[ast.Return] = ReturnStmt
statement_types[ast.Compare] = CompareStmt
statement_types[ast.BinOp] = BinOpStmt
statement_types[ast.BoolOp] = BoolOpStmt

def parse_statement(statement: ast.FunctionDef, context: Context) -> StmtType:
    statement_type = type(statement)
    
    if statement_type is ast.Name:
        return context.get(statement.id)

    if statement_type is ast.Attribute:
        return context.get(statement.attr, namespace=statement.value.id)

    assert statement_type in statement_types.keys(), \
        "Statement type '{}' not supported!".format(statement_type)
    return statement_types[statement_type](statement, context)
