class block(object):
    '''
    blocktract base object
    '''
    def compile(self):
        '''
        return LLL segment representing this object
        '''
        raise NotImplemented("Inherited class must produce LLL segment")
