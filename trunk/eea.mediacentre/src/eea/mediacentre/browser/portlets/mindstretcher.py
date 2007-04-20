from zope.component import getUtility
from eea.mediacentre.interfaces import IVideo, IMediaCentre
from eea.mediacentre.browser.portlets.base import MediaPortlet

class MindStretcherPortlet(MediaPortlet):

    media_type = 'mindstretcher'

    def items(self):
        mediacentre = getUtility(IMediaCentre)
        files = mediacentre.getMedia(self.media_type, 1)
        self.items = files
        return files

    def item_to_short_dict(self, item):
        return item

    def item_to_full_dict(self, item):
        return item
