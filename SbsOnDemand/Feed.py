'''
Created on Dec 3, 2011

@author: adam
'''

import re
try:
    import simplejson as json
except ImportError: 
    import json
import urlparse
import urllib
import config
from Video import Video

def getDefaultFeeds():
    feeds = {};
    for feed in config.DEFAULT_FEEDS:
        feeds[feed['name']] = Feed(feed)
    return feeds

def getMenuFeeds():
    def parseMenuItem(menuItem):
        item = {"feed":Feed(menuItem)}
        if (menuItem.has_key('children')):
            item['children'] = {}
            for childItem in menuItem['children']:
                item['children'][childItem['name']] = parseMenuItem(childItem)
        return item
    
    page = urllib.urlopen(config.MENU_URI)
    data = re.match('^VideoMenu\s*=\s*({.*})$', page.read()).group(1)
    menu = json.loads(data)
    feeds = {}
    for rootMenuName in menu.keys():
        feeds[rootMenuName] = parseMenuItem(menu[rootMenuName])
    return feeds   

def searchFeed(query):
    return Feed({"feedId": config.SEARCH_FEEDID, "filter":{"q":query}}) 

def getFeed(url):
    return Feed({"url":url})

class Feed(object):
    '''
    Class for Feed Object
    '''

    def __init__(self,feed):
        '''
        Constructor
        '''
        self.feedId = None
        self.title = None
        self.thumbnail = None
        self.filter = {}
        self._totalResults = None
        self.startIndex = None
        self.itemsPerPage = None
        self._videos = None
        self._parseFeed(feed)
        
    def _updateFeed(self, count = False, startIndex = 0, itemsPerPage = 10):
        # We can't retrieve videos without a feed id
        if self.feedId is None:
            raise Exception("Feed ID not specified")
        
        # Build the URL of the feed
        query = self.filter
        query['form'] = 'json'
        if count is True:
            query['count'] = 'true'
        query['range'] = str(startIndex) + '-' + str(startIndex + itemsPerPage)
        url = config.API_BASE + '/f/' + config.MPX_FEEDID + '/' + self.feedId + '?' + urllib.urlencode(query)
       
        # Fetch the feed
        page = urllib.urlopen(url)
        feed = json.load(page)
        self._parseFeed(feed)
        
    def _parseFeed(self, feed):
        self.title = feed.get("name", self.title)
        self.thumbnail = feed.get("thumbnail", self.thumbnail)
        self.filter = feed.get("filter", self.filter)
        self._totalResults = feed.get('totalResults', self._totalResults)
        self.startIndex = feed.get('startIndex', self.startIndex)
        self.itemsPerPage = feed.get('itemsPerPage', self.itemsPerPage)
    
        if feed.has_key("feedId"):
            self.feedId = feed["feedId"]
        else:
            # Extract feed PID from url
            url = feed.get("furl", feed.get("url",None))
            if url is not None and len(url) > 0:
                parsedurl = urlparse.urlparse(url)
                match = re.match('^/api/video_feed/f/'+config.MPX_FEEDID+'/(.+)$', parsedurl.path)
                if match is None:
                    raise Exception("Cannot extract feed identifier from url")
                self.feedId = match.group(1)
    
                # Extract url parameters into filter dict
                for k, v in urlparse.parse_qs(parsedurl.query).iteritems():
                    if len(v)>1:
                        self.filter[k] = v
                    else:
                        self.filter[k] = v[0] 
        
        # Form is not a filter, get rid of it
        if self.filter.has_key('form'):
            del self.filter['form']
            
        # Parse video entries
        if feed.has_key('entries'):
            videos = []
            for video in feed['entries']:
                videos.append(Video(video))
            self._videos = videos
        
    def getVideos(self, count = False, startIndex = 0, itemsPerPage = 10):
        # Use cached content if we can
        if self._videos is not None and startIndex == self.startIndex and itemsPerPage <= self.itemsPerPage:  # TODO handle pagination (count=true, range=start-finish, etc.)
            if itemsPerPage < self.itemsPerPage:
                return self._videos[0:itemsPerPage]
            else:
                return self._videos
            
        # Call update feed to download new data
        self._updateFeed(count, startIndex, itemsPerPage)
        
        # Return videos
        return self._videos
    
    def getTotalResults(self):
        if self.feedId is None:
            return 0
        
        if self._totalResults is not None:
            return self._totalResults
        
        self._updateFeed(True)
        
        return self._totalResults
    
    videos = property(getVideos)
    totalResults = property(getTotalResults)
        