import ast
import operator

class OperatorType:
    pass

class EqualsOperator(OperatorType):
    pass

operator_types = {}
operator_types[ast.Eq] = EqualsOperator

def parse_operator(operator) -> OperatorType:
    operator_type = type(operator)
    assert operator_type in operator_types.keys(), \
        "Operator type '{}' not supported!".format(operator_type)
    return operator_types[operator_type]
