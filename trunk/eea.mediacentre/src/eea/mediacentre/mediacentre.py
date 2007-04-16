from Products.CMFPlone import utils
from Products.Five.traversable import FiveTraversable
from eea.mediacentre.interfaces import IMediaCentre, IMediaCentrePlugin
from eea.themecentre.interfaces import IThemeCentre
from zope.app.traversing.interfaces import ITraverser
from zope.interface import implements
from zope.component import getAllUtilitiesRegisteredFor, adapts
from zope.publisher.interfaces import IPublishTraverse

MEDIA_SEARCH_KEY = 'eea.mediacentre.search'

class MediaCentre(object):
    implements(IMediaCentre)

    def getMedia(self, media_type=None, size=None, search={}):
        result = []
        plugins = self._getPlugins()

        for plugin in plugins:
            mediaobjects = plugin.getMedia(media_type, size, search)
            result.extend(mediaobjects)

        return result

    def getMediaTypes(self):
        mediatypes = {}
        plugins = self._getPlugins()

        for plugin in plugins:
            mediatypes.update(plugin.getMediaTypes())

        return mediatypes

    def getPluginNames(self):
        plugins = self._getPlugins()
        return [plugin.name for plugin in plugins]

    def _getPlugins(self):
        plugins = getAllUtilitiesRegisteredFor(IMediaCentrePlugin)
        return plugins
