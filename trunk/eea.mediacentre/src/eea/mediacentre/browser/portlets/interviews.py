from zope.component import getUtility
from eea.mediacentre.interfaces import IVideo, IMediaCentre
from eea.mediacentre.browser.portlets.base import MediaPortlet

class InterviewsPortlet(MediaPortlet):

    media_type = 'interview'

    def items(self):
        mediacentre = getUtility(IMediaCentre)
        files = mediacentre.getMedia(self.media_type, 1)
        self.items = files
        return files
