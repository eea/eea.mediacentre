""" Syndication
"""
# from p4a.plonevideo.syndication import VideoFeedEntry
from eea.mediacentre.bbb.plonevideo_syndication import VideoFeedEntry
from p4a.video.interfaces import IVideoEnhanced, IVideo
from zope.component import adapts
from zope.interface import implements
from Products.basesyndication.interfaces import IFeedEntry
from Products.CMFCore.utils import getToolByName


class VideoFeedEntryWithDescription(VideoFeedEntry):
    """ Video Feed Entry With Description
    """
    implements(IFeedEntry)
    adapts(IVideoEnhanced)

    def getAuthor(self):
        """ Get author
        """
        video = IVideo(self.context)
        author = video.video_author
        if author is None:
            return ''
        else:
            return author

    def getBody(self):
        """ Get body
        """
        video = IVideo(self.context)
        image_url = None
        if video.video_image is not None:
            image_url = self.context.absolute_url() + \
                "/viewimage?field=p4a.video.interfaces:IVideo:video_image"

        if image_url is None:
            return self.context.Description()
        else:
            return '<p><img src="%s" /></p><p>%s</p>' % \
                   (image_url, self.context.Description())

    def getWebURL(self):
        """ Get Web URL
        """
        url = self.context.absolute_url()
        portal_props = getToolByName(self.context, 'portal_properties')
        site_props = getattr(portal_props, 'site_properties')
        view_action = getattr(site_props, 'typesUseViewActionInListings', ())
        if self.context.portal_type in view_action:
            url += '/view'

        return url
