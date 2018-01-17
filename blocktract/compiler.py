from .parser import parse_vy

def compile_vy(raw_code: str) -> hex:
    ast = parse_vy(raw_code)
    #lll_code = ast_to_lll(ast)
    #lll_code = optimize_lll(lll_code)
    #bytecode = compile_lll(lll_code)
    return 0x0

if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser(description='Compiler')
    ap.add_argument('files', nargs='+', help='Path to source code file(s) to compile.')
    args = ap.parse_args()
    for source_file in args.files:
        with open(source_file, 'r') as f:
            raw_code = f.read()
        bytecode = compile_vy(raw_code)
