from Products.Five import BrowserView
from zope.component import getUtility
from eea.mediacentre.interfaces import IMediaCentre

class Info(BrowserView):
    def __init__(self, context, request):
        super(Info, self).__init__(context, request)
        self.mediacentre = getUtility(IMediaCentre)

    def getMediaStats(self):
        result = []

        types = self.mediacentre.getMediaTypes()
        for mediatype, type_info in types.items():
            data = self.mediacentre.getMediaByType(mediatype)
            result.append({ 'type': type_info['title'], 'count': len(data) })

        return result

    def getPluginNames(self):
        return self.mediacentre.getPluginNames()
