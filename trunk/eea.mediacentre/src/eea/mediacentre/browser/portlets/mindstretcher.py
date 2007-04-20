from Products.CMFPlone import utils
from zope.component import getUtility
from eea.mediacentre.interfaces import IVideo, IMediaCentre
from eea.mediacentre.browser.portlets.base import MediaPortlet
from eea.mediacentre.browser.swf import MediaPlayerWidget
from p4a.video.interfaces import IVideo

class MindStretcherPortlet(MediaPortlet):

    media_type = 'mindstretcher'

    def media_player(self):
        context = utils.context(self)
        if self.items:
            media_file = IVideo(self.items[0]['object'])
            widget = MediaPlayerWidget(media_file)
            return widget()
        else:
            return None

    def items(self):
        mediacentre = getUtility(IMediaCentre)
        files = mediacentre.getMedia(self.media_type, 1)
        self.items = files
        return files

    def item_to_short_dict(self, item):
        return item

    def item_to_full_dict(self, item):
        return item
