from Products.CMFPlone import utils
from Products.CMFCore.utils import getToolByName
from zope.component import getUtility
from eea.mediacentre.interfaces import IMediaCentre
from eea.mediacentre.browser.portlets.base import MediaPortlet
from eea.themecentre.themecentre import getThemeCentre

class NavigationPortlet(utils.BrowserView):

    def mediacentre(self):
        context = utils.context(self)
        themecentre = getThemeCentre(context)

        if not themecentre:
            return None

        if themecentre:
            media = { 'title': 'Multimedia',
                      'url': themecentre.absolute_url() + '/multimedia' }
        return media

    def media_types(self):
        context = utils.context(self)
        themecentre = getThemeCentre(context)

        if not themecentre:
            return []

        mediacentre = getUtility(IMediaCentre)
        types = mediacentre.getMediaTypes()

        result = []
        for media_type, type_info in types.items():
            data = { 'title': type_info['title'] + 's',
                     'url': themecentre.absolute_url() + '/multimedia/' +
                         type_info['template'],
                     'icon_url': "media_nav_icon.gif" }
            result.append(data)

        return result
