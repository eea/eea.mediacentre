from Products.ATContentTypes.interfaces import IATFile
from zope.component import getUtility, adapts, queryAdapter, adapter
from zope.interface import implements, implementer
from eea.mediacentre.interfaces import IMediaCentre, IMediaProvider
from eea.mediacentre.interfaces import IMediaDisplayInfo
from eea.mediacentre.mediacentre import MEDIA_SEARCH_KEY
from eea.themecentre.themecentre import getTheme
from p4a.video.interfaces import IVideoProvider, IVideo, IVideoEnhanced
from p4a.plonevideo.atct import _ATCTFileVideo
from p4a.common.formatting import fancy_time_amount, fancy_data_size


def P4AVideoDisplayInfoAdapter(context):
    if not IVideoEnhanced.providedBy(context):
        return None
    return P4AVideoDisplayInfo(context)

class P4AVideoDisplayInfo(_ATCTFileVideo):

    def __call__(self):
        info = {}
        info['title'] = self.title
        info['description'] = self.context.Description()
        info['height'] = self.height
        info['width'] = self.width
        info['duration'] = fancy_time_amount(int(round(self.duration)))
        info['video_image'] = self.video_image
        info['video_type'] = self.video_type
        info['size'] = fancy_data_size(self.context.get_size())
        info['icon'] = self.context.getIcon()
        info['url'] = self.context.absolute_url()
        return info

class MediaProvider(object):
    implements(IMediaProvider)

    def __init__(self, context):
        self.context = context
        # this can be changed by someone who wants a specific media type
        self.media_type = None

    @property
    def media_items(self):
        currentTheme = getTheme(self.context)
        mediacentre = getUtility(IMediaCentre)
        search = { MEDIA_SEARCH_KEY: { 'theme': currentTheme }}
        files = mediacentre.getMedia(self.media_type, search=search)

        videos = []
        for media_dict in files:
            videos.append(media_dict['object'])
            #adapted = queryAdapter(media_dict['object'], IVideo)
            #if adapted is not None:
            #    videos.append(adapted)

        return videos
