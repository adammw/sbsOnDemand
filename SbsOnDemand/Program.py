## @namespace SbsOnDemand::Program
# Module for managing programs

## Get a Program object by its id
# @param programId numeric identifier from sbs.com.au website 
# @return a single Program object
# @todo implement and document function
def getProgram(programId):
    pass

## Get all programs specified on sbs.com.au website
# @return array of Program objects
# @todo implement and document function
def getAllPrograms():
    pass

## Represents a tv program
# @todo implement and document class
class Program(object):
    
    ## Initialises a Program object
    # @todo implement and document function
    def __init__(self,params):
        pass
    
    ## Get a feed of all the videos for the program
    # @todo implement and document function
    # @return a Feed object
    def getFeed(self):
        pass