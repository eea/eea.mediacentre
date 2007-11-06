from p4a.video.browser.video import VideoListedSingle as P4AVideoListedSingle
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class VideoListedSingle(P4AVideoListedSingle):
    """Video listed single."""

    template = ViewPageTemplateFile('video-listed-single.pt')

class VideoUtils(object):
    """ A browser view for video utility methods. """

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def showEditMetadataTab(self):
        if not self.context.isTranslatable():
            return False

        current = self.context.getLanguage()
        return current != 'en'
