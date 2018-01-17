import ast
from .types import ArgType
from .context import Context

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


class AssertStmt(StmtType):
    pass

class AssignStmt(StmtType):
    def _parse_statement(self):
        target = self._statement.targets[0]
        self.target = self._context.get(target.attr, namespace=target.value.id)
        self.value = parse_statement(self._statement.value, self._context)

class ReturnStmt(StmtType):
    def _parse_statement(self):
        target = self._statement.value
        var = self._context.get(target.attr, namespace=target.value.id)
        self.return_type = var.type


def parse_statement(statement: ast.FunctionDef, context: Context) -> StmtType:
    statement_type = type(statement)
    
    if statement_type is ast.Attribute:
        return context.get(statement.attr, namespace=statement.value.id)

    assert statement_type in statement_types.keys(), \
        "Statement type '{}' not supported!".format(statement_type)
    return statement_types[statement_type](statement, context)

statement_types={}
statement_types[ast.Assert] = AssertStmt
statement_types[ast.Assign] = AssignStmt
statement_types[ast.Return] = ReturnStmt
