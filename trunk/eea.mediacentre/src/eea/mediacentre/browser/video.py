from p4a.video.browser.video import VideoListedSingle as P4AVideoListedSingle
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class VideoListedSingle(P4AVideoListedSingle):
    """Video listed single."""

    template = ViewPageTemplateFile('video-listed-single.pt')
