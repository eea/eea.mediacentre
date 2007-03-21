from eea.mediacentre.interfaces import IMediaCentre, IMediaCentrePlugin
from zope.interface import implements
from zope.component import getAllUtilitiesRegisteredFor

class MediaCentre(object):
    implements(IMediaCentre)

    def getMedia(self, media_type=None, size=None):
        result = []
        plugins = self._getPlugins()

        for plugin in plugins:
            mediaobjects = plugin.getMedia(media_type, size)
            result.extend(mediaobjects)

        return result

    def getMediaByType(self, mediatype, search=None):
        result = []
        plugins = self._getPlugins()

        for plugin in plugins:
            mediaobjects = plugin.getMediaByType(mediatype, search)
            result.extend(mediaobjects)

        return result

    def getMediaTypes(self):
        mediatypes = set()
        plugins = self._getPlugins()

        for plugin in plugins:
            mediatypes.update(plugin.getMediaTypes())

        return list(mediatypes)

    def getPluginNames(self):
        plugins = self._getPlugins()
        return [plugin.name for plugin in plugins]

    def _getPlugins(self):
        plugins = getAllUtilitiesRegisteredFor(IMediaCentrePlugin)
        return plugins
