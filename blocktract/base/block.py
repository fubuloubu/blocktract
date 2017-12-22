class block(object):
    '''
    blocktract base object that all base blocks inherit from
    '''
    @property
    def abi(self):
        '''
        return dict representing this object's ABI
        '''
        raise NotImplemented("Inherited class must produce ABI")
    
    @property
    def bytecode(self):
        '''
        return LLL segment representing this object's init code
        '''
        raise NotImplemented("Inherited class must produce LLL for init")

    @property
    def runtime(self):
        '''
        return LLL segment representing this object's runtime code
        '''
        raise NotImplemented("Inherited class must produce LLL for runtime")
