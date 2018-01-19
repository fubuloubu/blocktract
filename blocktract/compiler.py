import ast
import json

from .ast import transform, vyAST
from .debug import debug, ast2objtree
from .abi import get_abi
from .lll.utils import ast_to_lll
from .lll.optimize import optimize_lll
from .lll.compile import compile_lll


def _compile(raw_code: str, 
             debug_py_ast=False,
             debug_vy_ast=False,
             debug_vy_abi=False,
             debug_lll_ir=False,
             optimize=0) -> dict:

    # 1. Python parses to it's own AST
    py_ast = ast.parse(raw_code)
    if debug_py_ast:
        debug('Python AST', ast2objtree(py_ast, ast.AST), level=5)

    # 2. We Transform Python's AST to custom Vyper AST classes
    #    This filters out additional Python features and cleans our AST
    vy_ast = transform(py_ast)
    if debug_vy_ast:
        debug('Vyper AST', ast2objtree(vy_ast, vyAST), level=5)

    # 3. At this point we can obtain the ABI directly from AST
    abi = get_abi(vy_ast)
    if debug_vy_abi:
        debug('Application Binary Interface', abi, level=5)

    # Maybe optimize Vyper AST?

    # 4. Compiler the AST into our IR, which is LLL
    #    This produces a few different outputs
    lll_code = ast_to_lll(vy_ast)
    if debug_lll_ir:
        debug('LLL IR', lll_code, level=5)

    # 5. (optional) Run optimizations on LLL IR
    #    This should not modify functionality, only reducing gas costs
    if optimize > 0:
        lll_code = optimize_lll(lll_code)
    if debug_lll_ir:
        debug('Optimized LLL IR', lll_code, level=5)

    # 6. Last, translate this from LLL IR to EVM Bytecode
    bytecode, runtime = compile_lll(lll_code)

    # Returns JSON-compatible format for our deliverables
    return {
            'abi': abi, 
            'bin': "0x"+bytecode.hex(),
            'run': "0x"+runtime.hex(),
        }

if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser(description='Compiler')
    ap.add_argument('files', nargs='+', help='Path to source code file(s) to compile.')
    flags = ap.add_argument_group('flags')
    flags.add_argument('--debug', type=str, nargs='?', default='', help='''
        Debug options:
        py-ast (Show Python AST),
        vy-ast (Show Vyper AST),
        vy-abi (Show Vyper ABI),
        lll-ir (Show LLL IR)
    ''')
    flags.add_argument('--optimize', type=int, choices=[0, 1], default=0, help='Optimization Level')
    args = ap.parse_args()
    debug_flags = {'debug_'+k.replace('-','_'): True for k in args.debug.split(',')} \
                    if args.debug is not '' else {}
    results = {}
    for source_file in args.files:
        with open(source_file, 'r') as f:
            result = _compile(f.read(), **debug_flags, optimize=args.optimize)
        results[source_file] = result
    # Print output as compactly as possible
    print(json.dumps(results, separators=(',', ':')))
