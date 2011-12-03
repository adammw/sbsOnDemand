'''
Created on Dec 3, 2011

@author: adam
'''

API_BASE = "http://www.sbs.com.au/api/video_feed"
MENU_URI = "http://www.sbs.com.au/ondemand/js/video-menu"
MPX_FEEDID = "dYtmxB"
SEARCH_FEEDID = "search"
ALLDATA_FEEDID = "CxeOeDELXKEv"
DEFAULT_FEEDS = [
    {"name": "Programs", "feedId": "section-programs"},
    {"name": "Clips", "feedId": "section-clips"},
    {"name": "Events", "feedId": "section-events"},
    {"name": "Last Chance", "feedId":"videos-lastchance"},
    {"name": "Featured Programs", "feedId":"featured-programs-prod"},
    {"name": "Featured Clips", "feedId":"featured-clips"}
]