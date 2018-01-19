from .types import LLLNode

def compile_lll(lll: LLLNode) -> (bytes, bytes):
    bytecode = bytes()
    runtime = bytes()
    return bytecode, runtime
