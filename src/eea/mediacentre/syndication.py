from p4a.fileimage.image._widget import ImageURLWidget
from p4a.plonevideo.syndication import VideoFeedEntry
from p4a.video.interfaces import IVideoEnhanced, IVideo
from zope.component import adapts
from zope.interface import implements

from Products.basesyndication.interfaces import IFeedEntry
from Products.CMFCore.utils import getToolByName
from Products.fatsyndication.adapters import BaseFeedEntry

class VideoFeedEntryWithDescription(VideoFeedEntry):
    implements(IFeedEntry)
    adapts(IVideoEnhanced)

    def getAuthor(self):
        video = IVideo(self.context)
        author = video.video_author
        if author is None:
            return ''
        else:
            return author

    def getBody(self):
        video = IVideo(self.context)
        image_url = None
        if video.video_image is not None:
            field = IVideo['video_image'].bind(video)
            image_url = ImageURLWidget(field, self.context.REQUEST).url or None

        if image_url is None:
            return self.context.Description()
        else:
            return '<p><img src="%s" /></p><p>%s</p>' % \
                   (image_url, self.context.Description())

    def getWebURL(self):
        url = self.context.absolute_url()
        portal_props = getToolByName(self.context, 'portal_properties')
        site_props = getattr(portal_props, 'site_properties')
        view_action = getattr(site_props, 'typesUseViewActionInListings', ())
        if self.context.portal_type in view_action:
            url += '/view'

        return url  
