""" Media Centre
"""
from eea.mediacentre.interfaces import IMediaCentre, IMediaCentrePlugin
from zope.interface import implements
from zope.component import getAllUtilitiesRegisteredFor

MEDIA_SEARCH_KEY = 'eea.mediacentre.search'

class MediaCentre(object):
    """ Media Centre
    """
    implements(IMediaCentre)

    def getMedia(self, media_type=None, size=None, full_objects=True, search=None):
        """ Get Media
        """
        if search is None:
            search = {}
        result = []
        plugins = self._getPlugins()

        for plugin in plugins:
            mediaobjects = plugin.getMedia(media_type, size, full_objects, search)
            result.extend(mediaobjects)

        return result

    def getMediaTypes(self):
        """ Get Media Types
        """
        mediatypes = {}
        plugins = self._getPlugins()

        for plugin in plugins:
            mediatypes.update(plugin.getMediaTypes())

        return mediatypes

    def getPluginNames(self):
        """ Get Plugin Names
        """
        plugins = self._getPlugins()
        return [plugin.name for plugin in plugins]

    def _getPlugins(self):
        """ Get Plugins
        """
        plugins = getAllUtilitiesRegisteredFor(IMediaCentrePlugin)
        return plugins
