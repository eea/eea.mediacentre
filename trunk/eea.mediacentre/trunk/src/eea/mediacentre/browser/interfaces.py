""" Interfaces
"""
from zope.interface import Interface
from eea.themecentre.browser.interfaces import IPortlet

class IMediaPortlet(IPortlet):
    """ Media portlet
    """

    def all_link(self):
        """ All link
        """
        pass

    def short_items(self):
        """ Short items
        """
        pass

    def full_items(self):
        """ Full items
        """
        pass

    def items(self):
        """ Items
        """
        pass

    def media_player(self):
        """ Returns the media player for the media file.
        """

class INavigationPortlet(Interface):
    """ Navigation Portlet
    """

    def mediacentre(self):
        """ Mediacentre
        """
        pass

    def media_types(self):
        """ Media types
        """
        pass
