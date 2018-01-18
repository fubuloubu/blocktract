import ast
import json

from .ast import transform, AST as VyAST
from .debug import debug, ast2objtree


def _compile(raw_code: str, 
             debug_py_ast=False,
             debug_vy_ast=False,
             debug_vy_abi=False,
             debug_lll_ir=False,
             optimize=0) -> dict:
    py_ast = ast.parse(raw_code)
    if debug_py_ast:
        debug('Python AST', ast2objtree(py_ast, ast.AST), level=5)
    vy_ast = transform(py_ast)
    if debug_vy_ast:
        debug('Vyper AST', ast2objtree(vy_ast, VyAST), level=5)
    #abi = get_abi(vy_ast)
    #if debug_vy_abi:
    #    debug('Application Binary Interface', abi, level=5)
    #lll_code = ast_to_lll(ast)
    #if debug_lll:
    #    debug('LLL IR', lll_code, level=5)
    #if optimize > 0:
    #    lll_code = optimize_lll(lll_code)
    #if debug_lll:
    #    debug('Optimized LLL IR', lll_code, level=5)
    #bytecode, runtime = compile_lll(lll_code)
    #return {'abi': abi, 'bin': bytecode, 'run': runtime}
    return dict()

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
    flags.add_argument('--optimize', type=int, choices=[0, 1], help='Optimization Level')
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
