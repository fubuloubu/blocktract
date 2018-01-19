from .ast import (
        vyModule,
        vyMethod,
    )

def function_abi(method: vyMethod) -> dict:
    function = {}
    function['name'] = method.name
    function['inputs'] = []
    for a in method.args:
        function['inputs'].append({
                'name': a.name,
                'type': str(a.type)
            })
    if method.returns:
        function['outputs'] = [str(t) for t in method.returns]
    return function

def get_abi(module: vyModule) -> list:
    abi = []
    # Treat constructor differently, if available
    if module.constructor:
        constructor = {'type':'constructor'}
        constructor.update(function_abi(module.constructor))
        abi.append(constructor)
    # Add all public methods
    for method in module.methods:
        if 'public' in method.decorators:
            function = {'type':'function'}
            function.update(function_abi(method))
            abi.append(function)
    # TODO Add events
    return abi
