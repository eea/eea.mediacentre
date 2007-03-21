from zope.interface import Interface
from eea.themecentre.browser.interfaces import IPortlet

class IMediaPortlet(IPortlet):

    def all_link():
        pass

    def short_items():
        pass

    def full_items():
        pass

    def media_player():
        """ Returns the media player for the media file. """
