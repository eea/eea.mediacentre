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
        media = { 'title': 'Multimedia',
                  'url': themecentre.absolute_url() + '/mediacentre_view' }
        return media

    def media_types(self):
        context = utils.context(self)
        mediacentre = getUtility(IMediaCentre)
        types = mediacentre.getMediaTypes()

        result = []
        for type in types:
            data = { 'title': type['title'] + 's',
                     'url': context.absolute_url() + '/' + type['id'],
                     'icon_url': "media_nav_icon.gif" }
            result.append(data)

        return result
