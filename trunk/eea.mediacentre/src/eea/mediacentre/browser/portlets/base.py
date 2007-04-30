from zope.component import getAdapter, getUtility
from zope.interface import implements
from eea.themecentre.browser.portlets.catalog import BasePortlet
from eea.mediacentre.browser.interfaces import IMediaPortlet
from Products.CMFPlone import utils
from p4a.video.interfaces import IMediaPlayer
from p4a.video.browser.video import VideoPageView
from eea.mediacentre.interfaces import IMediaCentre

class MediaPortlet(BasePortlet):
    implements(IMediaPortlet)

    def media_player(self):
        """ Returns an html snippet for showing a video.
            This works for the formats that p4avideo supports. """
        context = utils.context(self)
        if self.items:
            media_file = self.items[0]['object']
            mime_type = media_file.get_content_type()
            widget = getAdapter(media_file, IMediaPlayer, name=mime_type)
            widget.use_height_only = True
            return widget(None, None)
        else:
            return None

    def item_to_short_dict(self, item):
        return item

    def item_to_full_dict(self, item):
        return item

    def all_link(self):
        mediacentre = getUtility(IMediaCentre)
        media_types = mediacentre.getMediaTypes()
        template = self.media_type + 's'

        context = utils.context(self)
        return context.absolute_url() + '/' + template

    def items(self):
        mediacentre = getUtility(IMediaCentre)
        files = mediacentre.getMedia(self.media_type, 1)
        self.items = files
        return files

    def short_items(self, media_type):
        self.media_type = media_type
        return super(MediaPortlet, self).short_items()
