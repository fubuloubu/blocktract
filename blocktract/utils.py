import sys
import inspect

# Python magic to get all classes in this module
module_classes = lambda module: dict(inspect.getmembers(sys.modules[module], inspect.isclass))
