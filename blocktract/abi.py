from .ast import (
        vyModule,
        vyMethod,
        vyEvent,
    )

def function_abi(method: vyMethod) -> dict:
    function = {}
    function['name'] = method.name
    function['inputs'] = []
    for a in method.args:
        function['inputs'].append({
                'name': a.name,
                'type': a.type.compiled_type
            })
    if method.returns:
        function['outputs'] = [t.compiled_type for t in method.returns]
    return function

def event_abi(event: vyEvent) -> dict:
    return dict()

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
    # Lastly, add events
    for event in module.events:
        abi.append(event_abi(event))
    return abi
