import ast
from .types import ArgType
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


class AssertStmt(StmtType):
    def _parse_statement(self):
        self.test = parse_statement(self._statement.test, self._context)

class AssignStmt(StmtType):
    def _parse_statement(self):
        target = self._statement.targets[0]
        self.target = self._context.get(target.attr, namespace=target.value.id)
        self.value = parse_statement(self._statement.value, self._context)

class ReturnStmt(StmtType):
    def _parse_statement(self):
        target = self._statement.value
        var = self._context.get(target.attr, namespace=target.value.id)
        self.returns = var

class CompareStmt(StmtType):
    def _parse_statement(self):
        self.operator = parse_operator(self._statement.ops[0])
        assert len(self._statement.ops) == 1, "Only supports one operator!"
        self.left = parse_statement(self._statement.left, self._context)
        assert len(self._statement.comparators) == 1, "Only supports one comparator!"
        self.right = parse_statement(self._statement.comparators[0], self._context)

statement_types={}
statement_types[ast.Assert] = AssertStmt
statement_types[ast.Assign] = AssignStmt
statement_types[ast.Return] = ReturnStmt
statement_types[ast.Compare] = CompareStmt

def parse_statement(statement: ast.FunctionDef, context: Context) -> StmtType:
    statement_type = type(statement)
    
    if statement_type is ast.Name:
        return context.get(statement.id)

    if statement_type is ast.Attribute:
        return context.get(statement.attr, namespace=statement.value.id)

    assert statement_type in statement_types.keys(), \
        "Statement type '{}' not supported!".format(statement_type)
    return statement_types[statement_type](statement, context)
