## @namespace SbsOnDemand::Category
# Module for managing video categories

## Represents a category
class Category(object):
    '''
    
    '''
    
    ## @var name
    # the name of the category
    ## @var scheme
    # the scheme the category fits in to

    ## Creates a Category object
    # @param params Dictionary of parameters, should include `media$name` and `media$scheme`
    def __init__(self,params):
        self.name = params.get('media$name',None)
        self.scheme = params.get('media$scheme',None)
    