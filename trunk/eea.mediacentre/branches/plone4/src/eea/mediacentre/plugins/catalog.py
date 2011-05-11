""" Catalog
"""
from Products.CMFCore.utils import getToolByName
from zope.interface import implements
from zope.app.component.hooks import getSite
from eea.mediacentre.plugins.interfaces import ICatalogPlugin
from eea.mediacentre.mediacentre import MEDIA_SEARCH_KEY

class CatalogPlugin(object):
    """ Catalog Plugin
    """
    implements(ICatalogPlugin)

    def getMedia(self, media_type=None, size=None, full_objects=True, searchfor=None):
        """ Returns media files as dicts. media_type arg can be e.g.
            video, interview or other. Other means that no type is chosen.
            Returned media can be ATImage, ATFile or FlashFile objects.
        """
        if searchfor is None:
            searchfor = {}
        site = getSite()
        search = self._getValidData(searchfor)
        catalog = getToolByName(site, 'portal_catalog')

        # first search for videos and then search for images

        query = { 'portal_type': ['File', 'FlashFile'],
                  'object_provides': 'p4a.video.interfaces.IVideoEnhanced',
                  'sort_on': 'Date',
                  'sort_order': 'reverse',
                  'review_state': 'published' }

        # if search is not none, assume it's a dict and merge it with query
        if search:
            query['getThemes'] = search['theme']

        if media_type and media_type != 'image':
            query['media_types'] = media_type

        video_brains = []
        if media_type is None or media_type != 'image':
            video_brains = catalog.searchResults(query)

        image_brains = []
        if media_type is None or media_type == 'image':
            del query['object_provides']
            query['portal_type'] = 'Image'
            image_brains = catalog.searchResults(query)

        result = []

        for brains in [video_brains, image_brains]:
            for brain in brains:
                data = { 'title': brain.Title,
                         'url': brain.getURL() }
                if full_objects:
                    data['object'] = brain.getObject()
                else:
                    data['object'] = brain
                result.append(data)

        if size:
            return result[:size]
        else:
            return result

    def getMediaTypes(self):
        """ Get Media Types
        """
        site = getSite()
        vocab = getToolByName(site, 'portal_vocabularies')
        multimedia = getattr(vocab, 'multimedia')
        types = {}
        for mid in multimedia.objectIds():
            title = getattr(multimedia, mid).Title()
            types[mid] = { 'title': title }
        return types

    @property
    def name(self):
        """ Name
        """
        return 'Catalog Plugin'

    def _getValidData(self, searchfor):
        """ Get Valid Data
        """
        return searchfor.get(MEDIA_SEARCH_KEY, None)
