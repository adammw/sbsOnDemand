'''
Created on Dec 3, 2011

@author: adam
'''

import urllib

class Media(object):
    '''
    Class for Media Objects
    '''

    def __init__(self,params):
        '''
        Constructor
        '''
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
        
    def getSMIL(self):
        if self._smil is None:
            if self.url is None:
                raise Exception("No URL Specified For Media")
            fp = urllib.urlopen(self.url)
            self._smil = fp.read()
        return self._smil
    
    def getSMILDOM(self):
        if self._smilDOM is None:
            self._parseSMIL()
        return self._smilDOM
    
    def _parseSMIL(self):
        import xml.dom.minidom
        self._smilDOM = xml.dom.minidom.parseString(self.getSMIL())
    
    def getBaseUrl(self):
        if self._smilDOM is None:
            self._parseSMIL()
        for meta in self._smilDOM.getElementsByTagName('meta'):
            if len(meta.getAttribute('base'))>0:
                return meta.getAttribute('base')
            
    def getVideoUrl(self):
        if self._smilDOM is None:
            self._parseSMIL()
        for video in self._smilDOM.getElementsByTagName('video'):
            if len(video.getAttribute('src'))>0:
                return video.getAttribute('src')
            
    def getCaptions(self):
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