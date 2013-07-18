""" Syndication
"""
from eea.mediacentre.bbb.plonevideo_syndication import VideoFeedEntry
from eea.mediacentre.interfaces import IVideo
from zope.component import adapts
from zope.interface import implements
from Products.basesyndication.interfaces import IFeedEntry
from Products.CMFCore.utils import getToolByName


class VideoFeedEntryWithDescription(VideoFeedEntry):
    """ Video Feed Entry With Description
    """
    implements(IFeedEntry)
    adapts(IVideo)

    def getAuthor(self):
        """ Get author
        """
        try:
            video = self.context.restrictedTraverse('@@video_view')
        except AttributeError:
            return ''
        author = video.author()
        if author is None:
            return ''
        else:
            return author

    def getBody(self):
        """ Get body
        """
        image_url = self.context.absolute_url() + \
            "/image_large"
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
