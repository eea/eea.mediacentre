from Products.Five import BrowserView
from zope.component import getUtility
from eea.rdfrepository.interfaces import IRDFRepository

class Info(BrowserView):
    def __init__(self, context, request):
        super(Info, self).__init__(context, request)
        self.rdfrepository = getUtility(IRDFRepository)

    def getRDFStats(self):
        """ Returns a list of feed dictionaries. """
        result = []
        query = {}

        theme = self.request.get('theme', None)
        if theme:
            query = { 'title': theme,
                      'subject': theme }

        rdfrepository = getUtility(IRDFRepository)
        data = rdfrepository.getFeedData(query)

        for feed in data:
            result.append({ 'url': feed['link'] })

        return result

    def getPluginNames(self):
        return self.rdfrepository.getPluginNames()
