'''
Created on Dec 3, 2011

@author: adam
'''

class Category(object):
    '''
    classdocs
    '''

    def __init__(self,params):
        '''
        Constructor
        '''
        self.name = params.get('media$name',None)
        self.scheme = params.get('media$scheme',None)