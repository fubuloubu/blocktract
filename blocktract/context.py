from .debug import debug
from .eth.environment import environment as eth_env

class Context:
    def __init__(self):
        self._scopes = {}
        self._scopes.update(eth_env)
        self.RESTRICTED_SCOPES = eth_env.keys()

    @property
    def scopes(self) -> list:
        return self._scopes.keys()

    def new_scope(self, scope: str):
        if self.has_scope(scope):
            raise ValueError("Scope '{}' already exists in context!".format(scope))
        self._scopes[scope] = {}
        self.current_scope = scope

    def has_scope(self, scope: str) -> bool:
        return scope in self.scopes

    def get_scope(self, scope=None) -> list:
        if not scope:
            return self._scopes[self.current_scope]
        if self.has_scope(scope):
            return self._scopes[scope]
        raise ValueError("Scope '{}' does not exist in context!".format(scope))

    @property
    def all_vars(self):
        for scope in self.scopes:
            for var in self.vars(scope):
                yield scope + '.' + var

    def vars(self, scope=None) -> list:
        if not scope:
            scope = self.current_scope
        return self.get_scope(scope).keys()

    def has(self, varname: str, scope=None) -> bool:
        if not scope:
            scope = self.current_scope
        return varname in self.vars(scope)

    def get(self, varname: str, scope=None):
        if not scope:
            scope = self.current_scope
        if self.has(varname, scope):
            return self.get_scope(scope)[varname]
        raise ValueError("Variable '{}' does not exist in scope '{}'!".format(varname, scope))
    
    def new(self, var, scope=None):
        if not scope:
            scope = self.current_scope
        if scope in self.RESTRICTED_SCOPES:
            raise ValueError("Cannot create variable in scope '{}'!".format(scope))
        if self.has(var.name, scope):
            raise ValueError("Variable '{}' already exists in scope '{}'!".format(var.name, scope))
        self.get_scope(scope)[var.name] = var
        debug(self, "Created " + var.name + " of type " + var.type)
