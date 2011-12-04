'''
Created on Dec 3, 2011

@author: adam
'''

import cookielib
from urllib import urlencode
import urllib2
import config

def loginUser(username, password):
    return User({"username": username, "password": password})

class InvalidCredentialsException(exception):
    pass

class User(object):
    '''
    Class for User objects
    '''

    def __init__(self,params):
        '''
        Constructor
        '''
        self._cookiePolicy = cookielib.DefaultCookiePolicy()
        self._cookieJar = cookielib.CookieJar(self._cookiePolicy)
        self._cookieHandler = urllib2.HTTPCookieProcessor(self._cookieJar)
        self._proxyHandler = urllib2.ProxyHandler(config.PROXY)
        self._opener = urllib2.build_opener(self._proxyHandler, self._cookieHandler)
        
        self._loggedIn = False
        
        if (params.has_key('username') and params.has_key('password')):
            self._loggedIn = self._login(params['username'],params['password'])
            if (self._loggedIn == False):
                raise InvalidCredentialsException()
    
    def getAccountInfo(self):
        if not self._loggedIn:
            raise InvalidCredentialsException()
        # TODO
    
    def getMyVideosFeed(self):
        if not self._loggedIn:
            raise InvalidCredentialsException()
        # TODO
    
    def _login(self,username,password):
        req = urllib2.Request(config.LOGIN_URI, urlencode({"username":username,"password":password,"submit":""}), origin_req_host='sbs.com.au')
        fp = self._opener.open(req)
        # TODO: Validate response for a valid sign in
        return True
        
    def logout(self):
        req = urllib2.Request(config.LOGOUT_URI)
        fp = self._opener.open(req)
        self._cookieJar.clear()
        self._loggedIn = False
        