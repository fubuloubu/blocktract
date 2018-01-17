import ast
import operator

class OperatorType:
    pass

class LessthanEqualsOperator(OperatorType):
    def __str__(self):
        return "'<='"

class EqualsOperator(OperatorType):
    def __str__(self):
        return "'=='"

class AndOperator(OperatorType):
    def __str__(self):
        return "'&&'"

class AddOperator(OperatorType):
    def __str__(self):
        return "'+'"

operator_types = {}
operator_types[ast.LtE] = LessthanEqualsOperator
operator_types[ast.Eq] = EqualsOperator
operator_types[ast.And] = AndOperator
operator_types[ast.Add] = AddOperator

def parse_operator(operator) -> OperatorType:
    operator_type = type(operator)
    assert operator_type in operator_types.keys(), \
        "Operator type '{}' not supported!".format(operator_type)
    return operator_types[operator_type]()
