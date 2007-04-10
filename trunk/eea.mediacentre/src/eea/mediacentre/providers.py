from eea.mediacentre.interfaces import IMediaCentre, IThemeVideoProvider
from eea.mediacentre.interfaces import IThemeInterviewProvider
from eea.mediacentre.interfaces import IThemeInteractiveMapProvider
from eea.mediacentre.interfaces import IThemeMindStretcherProvider
from eea.mediacentre.interfaces import IThemeImageProvider
from eea.mediacentre.mediacentre import MEDIA_SEARCH_KEY
from eea.themecentre.themecentre import getTheme
from p4a.video.interfaces import IVideoProvider, IVideo
from zope.component import getUtility, adapts, queryAdapter
from zope.interface import implements

class BaseMediaProvider(object):
    implements(IVideoProvider)

    def __init__(self, context):
        self.context = context

    @property
    def video_items(self):
        currentTheme = getTheme(self.context.context[0])
        mediacentre = getUtility(IMediaCentre)
        search = { MEDIA_SEARCH_KEY: { 'theme': currentTheme }}
        files = mediacentre.getMedia(self.media_type, search=search)
        videos = []

        for media_dict in files:
            adapted = queryAdapter(media_dict['object'], IVideo)
            if adapted is not None:
                videos.append(adapted)

        return videos

class ThemeVideoProvider(BaseMediaProvider):
    adapts(IThemeVideoProvider)

    media_type = 'video'

class ThemeInterviewProvider(BaseMediaProvider):
    adapts(IThemeInterviewProvider)

    media_type = 'interview'

class ThemeInteractiveMapProvider(BaseMediaProvider):
    adapts(IThemeInteractiveMapProvider)

    media_type = 'interactivemap'

class ThemeMindStretcherProvider(BaseMediaProvider):
    adapts(IThemeMindStretcherProvider)

    media_type = 'mindstretcher'

class ThemeImageProvider(BaseMediaProvider):
    adapts(IThemeImageProvider)

    media_type = 'image'
