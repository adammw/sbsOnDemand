## @namespace SbsOnDemand::Category
# Module for managing video categories

import config

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
    
    ## Gets a video feed of all videos in that category
    # @param feedId the feed unique identifier 
    def getFeed(self,feedId = config.ALLDATA_FEEDID):
        from Feed import Feed
        return Feed({"feedId": feedId, "filter": {"byCategories": self.name}})

    ## @see getFeed
    feed = property(getFeed)