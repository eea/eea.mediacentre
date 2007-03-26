from Products.CMFCore.utils import getToolByName
from zope.interface import implements
from zope.app.component.hooks import getSite
from zope.app.component.interface import interfaceToName
from eea.mediacentre.plugins.interfaces import ICatalogPlugin
from eea.mediacentre.mediatypes import MEDIA_TYPES

class CatalogPlugin(object):
    implements(ICatalogPlugin)

    def getMedia(self, media_type=None, size=None):
        site = getSite()
        catalog = getToolByName(site, 'portal_catalog')
        query = { 'portal_type': 'File' ,
                  'sort_on': 'Date',
                  'sort_order': 'reverse',
                  'review_state': 'published' }

        if media_type:
            iface = MEDIA_TYPES[media_type]['interface']
            query['object_provides'] = interfaceToName(site, iface)

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

    def getMediaByType(self, mediatype, search=None):
        site = getSite()
        portal_type = self.mapping[mediatype]
        catalog = getToolByName(site, 'portal_catalog')
        result = catalog.searchResults(portal_type=portal_type)
        return result

    def getMediaTypes(self):
        types = []
        for id, type_dict in MEDIA_TYPES.items():
            types.append({ 'id': id, 'title': type_dict['title'],
                           'interface': type_dict['interface'] })

        return types

    @property
    def name(self):
        return 'Catalog Plugin'
