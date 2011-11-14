from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from DateTime import DateTime

class Multimedia(BrowserView):
    """Multimedia page with coverflow, categories, tags, maps"""
    videos = []
    def __init__(self, context, request):
        super(Multimedia, self).__init__(context, request)
	catalog = getToolByName(self.context, 'portal_catalog')
	query = { 'sort_on': 'effective','sort_order': 'reverse','Language':self.context.getLanguage(),'effectiveRange': DateTime() }
	query['object_provides'] = 'p4a.video.interfaces.IVideoEnhanced'
	brains = catalog.searchResults(query)[0:5]
	self.videos = []
	for brain in brains:
	    self.videos.append({
		'title':brain.Title,
		'url':brain.getURL(),
	    })
