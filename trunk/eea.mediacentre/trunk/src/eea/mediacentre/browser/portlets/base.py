""" Base
"""
from zope.component import getAdapter, getUtility
from zope.interface import implements
from eea.themecentre.browser.portlets.catalog import BasePortlet
from eea.themecentre.themecentre import getTheme
from eea.mediacentre.browser.interfaces import IMediaPortlet
from p4a.video.interfaces import IMediaPlayer
from eea.mediacentre.interfaces import IMediaCentre
from eea.mediacentre.mediacentre import MEDIA_SEARCH_KEY

class MediaPortlet(BasePortlet):
    """ Media Portlet
    """
    implements(IMediaPortlet)

    def media_player(self):
        """ Returns an html snippet for showing a video.
            This works for the formats that p4avideo supports.
        """
        if self.items:
            media_file = self.items[0]['object']
            mime_type = media_file.get_content_type()
            widget = getAdapter(media_file, IMediaPlayer, name=mime_type)
            widget.use_height_only = True
            return widget(None, None)
        else:
            return None

    def item_to_short_dict(self, item):
        """ Item to short dict
        """
        return item

    def item_to_full_dict(self, item):
        """ Item to full dict
        """
        return item

    def all_link(self):
        """ All link
        """
        template = self.media_type + 's'

        context = self.context
        return context.absolute_url() + '/' + template

    def items(self):
        """ Items
        """
        context = self.context
        theme = getTheme(context)
        mediacentre = getUtility(IMediaCentre)
        query = {MEDIA_SEARCH_KEY: {'theme': theme, }, }
        files = mediacentre.getMedia(self.media_type, 1, search=query)
        return files

    def short_items(self, media_type):
        """ Short items
        """
        self.media_type = media_type
        return super(MediaPortlet, self).short_items()
