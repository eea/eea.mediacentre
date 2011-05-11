""" Navigation
"""
from Products.CMFPlone import utils
from Products.Five import BrowserView
from zope.component import getUtility
from eea.mediacentre.interfaces import IMediaCentre
from eea.themecentre.themecentre import getThemeCentre

class NavigationPortlet(BrowserView):
    """ Navigation Portlet
    """

    def mediacentre(self):
        """ Mediacentre
        """
        context = self.context()
        themecentre = getThemeCentre(context)

        if not themecentre:
            return None

        if themecentre:
            media = { 'title': 'Multimedia',
                      'url': themecentre.absolute_url() + '/multimedia' }
        return media

    def media_types(self):
        """ Media types
        """
        context = self.context()
        themecentre = getThemeCentre(context)

        if not themecentre:
            return []

        mediacentre = getUtility(IMediaCentre)
        types = mediacentre.getMediaTypes()

        result = []
        for tid, type_info in types.items():
            data = { 'title': type_info['title'] + 's',
                     'url': themecentre.absolute_url() + '/multimedia/' +
                         tid + 's',
                     'icon_url': "media_nav_icon.gif" }
            result.append(data)

        return result
