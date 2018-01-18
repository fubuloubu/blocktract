
# Base class of all types
class vyType:
    def __repr__(self):
        return self.__class__.__name__[2:]

    def can_store(self, _value):
        #TODO change to NotImplementedError
        return True

def get_type(typename: str) -> vyType:
    return vyType
