""" p4a.plonevideo.syndication
"""

from zope import component
from zope import interface
from p4a.video import interfaces
from Products.fatsyndication import adapters as fatadapters
from Products.basesyndication import interfaces as baseinterfaces


class VideoFeedEntry(fatadapters.BaseFeedEntry):
    """ VideoFeedEntry
    """
    interface.implements(baseinterfaces.IFeedEntry)
    component.adapts(interfaces.IVideoEnhanced)

    def __init__(self, context):
        fatadapters.BaseFeedEntry.__init__(self, context)

        self.video = interfaces.IVideo(self.context)

    def getBody(self):
        """See IFeedEntry.
        """
        return ''

    def getEnclosure(self):
        """ getEnclosure
        """
        return baseinterfaces.IEnclosure(self.context)

    def getTitle(self):
        """ getTitle
        """
        return self.video.title

    def getDescription(self):
        """ getDescription
        """
        return self.video.description

