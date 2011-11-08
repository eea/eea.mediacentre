""" Multimedia. Logic for EEA multimedia frontpage.
"""
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from DateTime import DateTime

from Products.EEAContentTypes.content.interfaces import IFlashAnimation
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
        query['object_provides'] = 'p4a.video.interfaces.IVideoEnhanced'
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
        interface = 'p4a.video.interfaces.IVideoEnhanced'
        # querying for extra objects because Animations also implement 
        # IVideoEnhanced
        result = _getItems(self,
                    interfaces = interface,
                    noOfItems=self.noOfLatestMultimedia)

        return result

    def getVideos(self):
        """ retrieves videos filtered by date and by topic """
        interface = 'p4a.video.interfaces.IVideoEnhanced'
        # querying for extra objects because Animations also implement 
        # IVideoEnhanced
        result = _getItems(self,
                    interfaces = interface,
                    noOfItems=self.noOfVideos + 20)
        result = [i for i in result if not IFlashAnimation.providedBy(
                                          i.getObject())][:self.noOfVideos]
        return result

    def getAnimations(self):
        """ retrieves multimedia swf animations filtered by date and topic """
        result = _getItems(self, interfaces = \
                'Products.EEAContentTypes.content.interfaces.IFlashAnimation',
                noOfItems = self.noOfAnimations)
        return result

    def getImageGalleries(self):
        """ retrieves image galleries filtered by date and by topic """
        #query = {'sort_on': 'effective',
        #         'sort_order': 'reverse',
        #         'effectiveRange': self.now,
        #         'portal_type' :'Image',
        #         'path' : 'www/SITE/pressroom/pictures'}
        query = {'sort_on': 'effective',
                 'sort_order': 'reverse',
                 'effectiveRange': self.now,
                 'portal_type' :'EyewitnessStory',
                 'path' : 'www/SITE/signals/galleries'}
        #http://www.eea.europa.eu/signals/galleries/createObject?type_name=EyewitnessStory
        res = self.catalog(query)
        return res
