from ..ast import *
from ..types import Type


# Recursive function to map all Vyper AST Nodes to lisp of LLLNodes
def convert(node: vyAST) -> list:
    print(node._fields)
    if isinstance(node, vyMethod):
        safety = []
        if 'payable' not in node.decorators:
            # Enforce 'msg.value = 0'
            safety.append(['assert', ['iszero', 'callvalue']])
        return [convert(stmt) for stmt in node.body]
    
    # Statements
    if isinstance(node, vyAssert):
        return ['assert', convert(node.stmt)]
    if isinstance(node, vyBinOp):
        return [str(node.operator), convert(node.left), convert(node.right)]

    # Stuff that deals with registers
    if isinstance(node, vyAssign):
        [mem_ptr, _, _] = convert(node.var)
        [_, reg_ptr, _] = convert(node.stmt)
        return ['sstore', mem_ptr, ['mload', reg_ptr]]
    if isinstance(node, vyReturn):
        [mem_ptr, reg_ptr, size] = convert(node.returns)
        return [['mstore', reg_ptr, ['sload', mem_ptr]], ['return', reg_ptr, size]]
    # Ends recursion, figures out what the value of the mem_ptr and reg_ptr are
    # at the moment of access, also what the size of the underlying type is
    if isinstance(node, vyVariable):
        return [0, 0, 0]
    raise NotImplementedError("LLL Conversion for '{}' not implemented!".format(node))


def keccak(string: str) -> bytes:
    return bytes(string, 'utf-8')


def method_signature(method: vyMethod) -> bytes:
    # Compose signature e.g. 'method_name(type1,type2,type3,...)'
    method_signature = \
            "{}({})".format(method.name, ",".join([a.type.compiled_type for a in method.args]))
    # Take the keccak hash of that signature, extract the first 4 bytes, and convert to int
    return int('0x'+keccak(method_signature).hex()[:8], 16)


def create_call(signature: int, runtime: list) -> list:
    # If calling context is for this function matches signature,
    # Execute statements in order given
    return ['if', ['eq', ['mload', 0], signature], ['seq', runtime, 'stop']]


def state_schema(state_list: list) -> list:
    # Contract creation needs to know what the state looks like
    return []


def ast_to_lll(contract: vyModule) -> (list, list):
    schema = state_schema(contract.state)
    constructor = convert(contract.constructor) if contract.constructor else []
    method_runtimes = \
            [(method_signature(method), convert(method)) for method in contract.methods]
    return link(schema, constructor, method_runtimes)


def link(schema, constructor, method_runtimes):
    runtime = ['lll', ['seq', *schema, *[create_call(s,r) for s,r in method_runtimes]], 0]
    program = ['seq', *schema, *constructor, ['return', 0, runtime]]
    return program
