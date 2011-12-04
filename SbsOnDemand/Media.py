## @namespace SbsOnDemand::Media
# Module for managing a/v media

import urllib

## Represents an exception that occurs when a method is invoked on a media that doesn't support that method
class InvalidMediaType(Exception):
    pass

## Represents a media (rendition) for a single video
class Media(object):
    
    ## Creates a media object
    # @param params the media data
    def __init__(self,params):
        self.audioChannels = params.get('plfile$audioChannels',None)
        self.audioSampleRate = params.get('plfile$audioSampleRate',None)
        self.bitrate = params.get('plfile$bitrate',None)
        self.checksums = params.get('plfile$checksums',None)
        self.contentType = params.get('plfile$contentType',None)
        self.duration = params.get('plfile$duration',None)
        self.expression = params.get('plfile$expression',None)
        self.fileSize = params.get('plfile$fileSize',None)
        self.frameRate = params.get('plfile$frameRate',None)
        self.format = params.get('plfile$format',None)
        self.height = params.get('plfile$height',None)
        self.isDefault = params.get('plfile$isDefault',None)
        self.language = params.get('plfile$language',None)
        self.sourceTime = params.get('plfile$sourceTime',None)
        self.url = params.get('plfile$url',None)
        self.width = params.get('plfile$width',None)
        self.assetTypes = params.get('plfile$assetTypes',None)
        self._smil = None
        self._smilDOM = None
        
    ## Get the raw url for the media
    # @return a absolute url to the content or SMIL file for the content
    def getUrl(self):
        return self.url
        
    ## Get the raw SMIL data for the media
    # @return a string of raw SMIL data from the server
    # @warning This function is only valid for video media, calling it on other contentTypes will trigger a InvalidMediaType exception
    def getSMIL(self):
        if self.contentType != "video":
            raise InvalidMediaType();
        if self._smil is None:
            if self.url is None:
                raise Exception("No URL Specified For Media")
            fp = urllib.urlopen(self.url)
            self._smil = fp.read()
        return self._smil
    
    ## Get the SMIL data parsed by xml.dom.minidom
    # @return a Document parsed by xml.dom.minidom
    # @warning This function is only valid for video media, calling it on other contentTypes will trigger a InvalidMediaType exception
    def getSMILDOM(self):
        if self.contentType != "video":
            raise InvalidMediaType();
        if self._smilDOM is None:
            self._parseSMIL()
        return self._smilDOM
    
    ## Parse the SMIL data with xml.dom.minidom
    # @warning This function is only valid for video media, calling it on other contentTypes will trigger a InvalidMediaType exception
    def _parseSMIL(self):
        if self.contentType != "video":
            raise InvalidMediaType();
        import xml.dom.minidom
        self._smilDOM = xml.dom.minidom.parseString(self.getSMIL())
    
    ## Get the base url
    # @return the base url (usually for rtmp streams in the form of "rtmp://server/path?auth=token")
    # @warning This function is only valid for video media, calling it on other contentTypes will trigger a InvalidMediaType exception
    def getBaseUrl(self):
        if self.contentType != "video":
            raise InvalidMediaType();
        if self._smilDOM is None:
            self._parseSMIL()
        for meta in self._smilDOM.getElementsByTagName('meta'):
            if len(meta.getAttribute('base'))>0:
                return meta.getAttribute('base')
    
    ## Get the video url
    # @return the video url (usually for rtmp streams in the form of "mp4:path/video.mp4") 
    # @warning This function is only valid for video media, calling it on other contentTypes will trigger a InvalidMediaType exception
    def getVideoUrl(self):
        if self.contentType != "video":
            raise InvalidMediaType();
        if self._smilDOM is None:
            self._parseSMIL()
        for video in self._smilDOM.getElementsByTagName('video'):
            if len(video.getAttribute('src'))>0:
                return video.getAttribute('src')
    
    ## Get captions for the media
    # @return an array of dict objects, each containing the src, lang, and type of the caption    
    # @warning This function is only valid for video media, calling it on other contentTypes will trigger a InvalidMediaType exception
    def getCaptions(self):
        if self.contentType != "video":
            raise InvalidMediaType();
        if self._smilDOM is None:
            self._parseSMIL()
        captions = []
        for textstream in self._smilDOM.getElementsByTagName('textstream'):
            if len(textstream.getAttribute('src')) == 0:
                continue
            captions.append({
                             "src":textstream.getAttribute('src'),
                             "lang":textstream.getAttribute('lang'),
                             "type":textstream.getAttribute('type')
                             })
        return captions
    
    ## @see getBaseUrl
    baseUrl = property(getBaseUrl)
    ## @see getVideoUrl
    videoUrl = property(getVideoUrl)
    ## @see getCaptions
    captions = property(getCaptions)

