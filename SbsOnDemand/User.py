## @namespace SbsOnDemand::User
# Module for managing user functions

import cookielib
from urllib import urlencode
import urllib2
import config

## Logs in a user 
# @return a User object
# @throws InvalidCredentialsException
def loginUser(username, password):
    return User({"username": username, "password": password})

## This exception is raised when the user credentials supplied are invalid or when invoking a method on a User object that is not logged in
class InvalidCredentialsException(Exception):
    pass

## Represents a single user
class User(object):

    ## Initialises a User object
    # @param params a dict containing username and password 
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
    
    ## Get information about the user
    # @todo implement and document function
    def getAccountInfo(self):
        if not self._loggedIn:
            raise InvalidCredentialsException()
        # TODO
    
    ## Get the user's "My Videos" feed
    # @todo implement and document function
    def getMyVideosFeed(self):
        if not self._loggedIn:
            raise InvalidCredentialsException()
        # TODO
    
    ## Authenticate the user object
    # @param username username
    # @param password password in cleartext 
    # @todo implement and document function
    def _login(self,username,password):
        req = urllib2.Request(config.LOGIN_URI, urlencode({"username":username,"password":password,"submit":""}), origin_req_host='sbs.com.au')
        fp = self._opener.open(req)
        # TODO: Validate response for a valid sign in
        return True
        
    ## Logout the user object
    def logout(self):
        req = urllib2.Request(config.LOGOUT_URI)
        fp = self._opener.open(req)
        self._cookieJar.clear()
        self._loggedIn = False
        