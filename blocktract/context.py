from .eth.environment import environment_vars

class Context:
    def __init__(self, state=None):
        self.state = state
        self.scopes = []
        self.environment = environment_vars
    
    # Push current scope, either function or branch-level
    def push(self, scope):
        self.scopes.append(scope)

    # Pop off current scope
    def pop(self):
        self.scopes.pop()

    # Get variable if available in namespace
    def get(self, name, namespace=None) -> bool:
        if not namespace:
            for scope in self.scopes:
                if name in scope.keys():
                    return scope[name]
            raise ValueError("'{}' not in local context!".format(name))
        if namespace is 'self':
            assert name in self.state.keys(), "'{}' not in global context!".format(name)
            return self.state[name]
        if namespace in self.environment.keys():
            assert name in self.environment[namespace].keys(), \
                    "'{}' not in environment context!".format(name)
            return self.environment[namespace][name]
        raise ValueError("'{}' not a valid context!".format(namespace))

