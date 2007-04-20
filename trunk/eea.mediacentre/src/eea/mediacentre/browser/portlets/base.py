from zope.component import getMultiAdapter, getUtility
from zope.interface import implements
from eea.themecentre.browser.portlets.catalog import BasePortlet
from eea.mediacentre.browser.interfaces import IMediaPortlet
from Products.CMFPlone import utils
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
            view = VideoPageView(media_file, self.request)
            view.update()
            return view.widgets['media_player']
        else:
            return None

    def item_to_short_dict(self, item):
        return item

    def item_to_full_dict(self, item):
        return item

    def all_link(self):
        mediacentre = getUtility(IMediaCentre)
        media_types = mediacentre.getMediaTypes()
        template = media_types[self.media_type]['template']

        context = utils.context(self)
        return context.absolute_url() + '/' + template
