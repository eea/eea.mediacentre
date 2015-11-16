""" Multimedia. Logic for EEA multimedia frontpage.
"""
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from DateTime import DateTime

from eea.design.browser.frontpage import _getItems

class Multimedia(BrowserView):
    """ Multimedia frontpahe with coverflow, latest videos,
    green tips animations categories, tags,
    """
    videos = []

    def __init__(self, context, request):
        super(Multimedia, self).__init__(context, request)
        self.catalog = getToolByName(context, 'portal_catalog')
        portal_properties = getToolByName(context, 'portal_properties')
        frontpage_properties = getattr(portal_properties,
                                                'frontpage_properties')

        self.noOfVideos = frontpage_properties.getProperty(
                                                           'noOfVideos', 8)
        self.noOfAnimations = frontpage_properties.getProperty(
                                                        'noOfAnimations', 8)
        self.noOfLatestMultimedia = frontpage_properties.getProperty(
                                                     'noOfLatestMultimedia', 8)
        self.now = DateTime()

        #'Language': self.context.getLanguage(),
        query = {'sort_on': 'effective',
                 'sort_order': 'reverse',
                 'effectiveRange': DateTime()}
        query['object_provides'] = 'eea.mediacentre.interfaces.IVideo'
        brains = self.catalog.searchResults(query)[0:5]
        self.videos = []
        for brain in brains:
            self.videos.append({
                'title':brain.Title,
                'url':brain.getURL(),
            })

    def getLatestMultimedia(self):
        """ retrieves latest published
        multimedia objects (videos/animations etc..)
        filtered by date and by topic """
        interface = {
              'query': [
              'eea.mediacentre.interfaces.IVideo',
              'Products.EEAContentTypes.content.interfaces.IFlashAnimation'
              ],
              'operator': 'or'
              }

        # querying for extra objects because Animations also implement
        # IVideoEnhanced
        result = _getItems(self,
                    interfaces=interface,
                    noOfItems=self.noOfLatestMultimedia)

        return result

    def getLatestVideos(self):
        """ retrieves latest published cloudVideos or videos
        filtered by date and by topic """
        interface = 'eea.mediacentre.interfaces.IVideo'
        result = _getItems(self,
                    interfaces=interface,
                    noOfItems=self.noOfLatestMultimedia)
        return result

    def getVideos(self):
        """ retrieves videos filtered by date and by topic """
        interface = 'eea.mediacentre.interfaces.IVideo'
        result = _getItems(self,
                    interfaces=interface,
                    noOfItems=self.noOfVideos + 20)
        return result

    def getAnimations(self):
        """ retrieves multimedia swf animations filtered by date and topic """
        result = _getItems(self, interfaces=\
                'Products.EEAContentTypes.content.interfaces.IFlashAnimation',
                noOfItems=self.noOfAnimations)
        return result

    def getImageGalleries(self):
        """ retrieves image galleries filtered by date and by topic """
        res = []
        query = {'sort_on': 'effective',
                 'sort_order': 'reverse',
                 'id' : 'pictures',
                 'portal_type' :'Folder',
                 'review_state': 'published',
                 'path' : 'www/SITE/pressroom'}
        res_pressroom = self.catalog(query)
        query.pop('id')

        query['portal_type'] = 'EyewitnessStory'
        query['path'] = 'www/SITE/signals/galleries'
        res_eyewitness = self.catalog(query)

        query['portal_type'] = 'Folder'
        query['path'] = {'query' : '/www/SITE/atlas/eea', 'depth': 1}
        res_atlas_brains = self.catalog(query)
        res_brains = []
        for i in range(0, len(res_atlas_brains) - 1):
            if res_atlas_brains[i].getObject().get('photos', 'none') != 'none':
                res_brains.append(res_atlas_brains[i])

        res.extend(res_pressroom)
        res.extend(res_eyewitness)
        res.extend(res_brains)

        return res
