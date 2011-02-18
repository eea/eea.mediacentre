from Products.CMFPlone import utils
from zope.component import getMultiAdapter, getUtility
from zope.interface import alsoProvides
from zope.security.proxy import removeSecurityProxy
from eea.mediacentre.interfaces import IMediaCentre

class MediaTypeProxy(utils.BrowserView):

    def video_items(self, media_type):
        mediacentre = getUtility(IMediaCentre)
        types = mediacentre.getMediaTypes()
        iface = types[media_type]['provider']

        alsoProvides(self, iface)
        context = utils.context(self)
        view = getMultiAdapter((self, self.request), name="video_provider")

        return view.video_items()
