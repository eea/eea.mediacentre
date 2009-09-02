from Products.CMFPlone import utils
from zope.component import getMultiAdapter, getUtility, queryAdapter
from zope.interface import alsoProvides
from zope.security.proxy import removeSecurityProxy
from eea.mediacentre.interfaces import IMediaCentre, IMediaProvider
from eea.mediacentre.interfaces import IMediaDisplayInfo
from p4a.video.interfaces import IMediaPlayer, IVideo

class MediaContainerVideos(object):

    def __init__(self, context, request):
        self.context = context
        self.reqeust = request

    def media_items(self, media_type):
        """ Returns dicts of all media items available.
            media_type arg is a string, e.g. 'video' """

        provider = IMediaProvider(self.context)
        provider.media_type = media_type

        items = []
        for file in provider.media_items:
            mime_type = file.get_content_type()
            media_info = queryAdapter(file, IMediaDisplayInfo, mime_type)
            widget = queryAdapter(file, IMediaPlayer, mime_type)

            info_dict = media_info()
            if widget:
                info_dict['widget'] = widget(None, None)
            items.append(info_dict)

        return items

class MediaContainerView(object):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def media_items(self, media_type=None):
        provider = IMediaProvider(self.context)
        provider.media_type = media_type

        videos = []
        for file in provider.media_items:
            #video = IVideo(file, None)
            #if video is not None:
            videos.append(file)

        return videos
