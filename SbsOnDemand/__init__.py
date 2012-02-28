## @package SbsOnDemand
# @mainpage SBS On Demand Service Package    
# 
# @section intro_sec Introduction
# 
# This package is designed to help third-party applications to interface with the SBS On Demand service 
# without worrying about the underlying complexity
# 
# @section using_sec Using the module
# 
# The module is object-oriented, however it is recommended that you let the package create the objects
# using either the static functions within each module or calling an object's method rather than directly
# using the class constructors. Properties are either pre-populated or are populated on request as getters.
# As such, there may be a delay when accessing properties or methods of objects as the functions are blocking.
# It is therefore recommended that if used in GUI programs that data is accessed from a separate thread.
#
# @subsection example_feed Example: Finding a video feed
# %Video feeds can be retrieved using static methods in Feed. 
#
# This example finds all the feeds from the SBS On Demand menu, and chooses the one entitled 'Program'
# @code
# import SbsOnDemand.Feed
# feeds = SbsOnDemand.Feed.getMenuFeeds()
# feed = feeds['Programs']['feed']
# @endcode
#
# @subsection example_video_feed Example: Getting videos from a feed 
# This example prints the title of each video in the feed
# @code
# for video in feed.videos:
#   print video.title
# @endcode
#
# @subsection example_video_id Example: Getting a video title when we know the ID number
# This example gets a video object for a specific video ID, and then prints the video's title
# @code
# import SbsOnDemand.Video
# video = SbsOnDemand.Video.getVideo(videoID)
# print video.title
# @endcode
# @subsection example_media Example: Getting a video's content url for the first media rendition
# This example uses the video object from Example 1, gets all the media associated with it, 
# and then prints each media with its (rtmp) url parameters
# @code
# for media in video.media['content']:
#   print media.bitrate, media.baseUrl, media.videoUrl
# @endcode
__all__ = ["config","Category","Feed","Media","Program","User","Video"]