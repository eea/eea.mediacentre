from zope.interface import Interface
from eea.themecentre.browser.interfaces import IPortlet

class IMediaPortlet(IPortlet):

    def all_link(): #pylint: disable-msg = E0211
        pass

    def short_items(): #pylint: disable-msg = E0211
        pass

    def full_items(): #pylint: disable-msg = E0211
        pass

    def items(): #pylint: disable-msg = E0211
        pass

    def media_player(): #pylint: disable-msg = E0211
        """ Returns the media player for the media file. """

class INavigationPortlet(Interface):

    def mediacentre(): #pylint: disable-msg = E0211
        pass

    def media_types(): #pylint: disable-msg = E0211
        pass
