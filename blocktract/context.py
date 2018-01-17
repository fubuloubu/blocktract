from .types import Type
from .eth.environment import environment

class Context:
    def __init__(self, state=None):
        self.state = state
        self.scopes = []
    
    # Push current scope, either function or branch-level
    def push(self, scope):
        self.scopes.append(scope)

    # Pop off current scope
    def pop(self):
        self.scopes.pop()

    # Get scope of variable
    def is_state_var(name: str) -> bool:
        return name in self.state.keys()

    # Get variable if available in namespace
    def get(self, name: str, namespace: str=None) -> Type:
        if not namespace:
            for scope in self.scopes:
                if name in scope.keys():
                    return scope[name]
            raise ValueError("'{}' not in local context!".format(name))
        if namespace is 'self':
            assert name in self.state.keys(), "'{}' not in global context!".format(name)
            return self.state[name]
        if namespace in environment.keys():
            assert name in environment[namespace].keys(), \
                    "'{}' not in '{}' environment context!".format(name, namespace)
            return environment[namespace][name]
        raise ValueError("'{}' not a valid context!".format(namespace))

    # Create variable in current namespace
    def set(self, name: str, val: Type):
        self.scopes[-1][name] = val
