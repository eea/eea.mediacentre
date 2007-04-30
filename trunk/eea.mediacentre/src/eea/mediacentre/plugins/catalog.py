from Products.CMFCore.utils import getToolByName
from zope.interface import implements
from zope.app.component.hooks import getSite
from eea.mediacentre.plugins.interfaces import ICatalogPlugin
from eea.mediacentre.mediacentre import MEDIA_SEARCH_KEY

class CatalogPlugin(object):
    implements(ICatalogPlugin)

    def getMedia(self, media_type=None, size=None, searchfor={}):
        site = getSite()
        search = self._getValidData(searchfor)
        catalog = getToolByName(site, 'portal_catalog')
        query = { 'portal_type': ['File', 'FlashFile'],
                  'sort_on': 'Date',
                  'sort_order': 'reverse',
                  'review_state': 'published' }

        # if search is not none, assume it's a dict and merge it with query
        if search:
            query['getThemes'] = search['theme']

        if media_type:
            query['media_types'] = media_type

        result = []
        brains = catalog.searchResults(query)
        for brain in brains:
            data = { 'title': brain.Title,
                     'url': brain.getURL(),
                     'object': brain.getObject() }
            result.append(data)

        if size:
            return result[:size]
        else:
            return result

    def getMediaTypes(self):
        site = getSite()
        vocab = getToolByName(site, 'portal_vocabularies')
        multimedia = getattr(vocab, 'multimedia')
        types = {}
        for id in multimedia.objectIds():
            title = getattr(multimedia, id).Title()
            types[id] = { 'title': title }
        return types

    @property
    def name(self):
        return 'Catalog Plugin'

    def _getValidData(self, searchfor):
        return searchfor.get(MEDIA_SEARCH_KEY, None)
