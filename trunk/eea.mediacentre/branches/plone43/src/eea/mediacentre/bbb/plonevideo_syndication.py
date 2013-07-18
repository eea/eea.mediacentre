# """ p4a.plonevideo.syndication
# """
#
from zope import component
from zope import interface
from Products.fatsyndication import adapters as fatadapters
from Products.basesyndication import interfaces as baseinterfaces
from eea.mediacentre.interfaces import IVideo


class VideoFeed(fatadapters.BaseFeed):
    """ VideoFeed adapter
    """
    interface.implements(baseinterfaces.IFeed)
    component.adapts(IVideo)


class VideoFeedSource(fatadapters.BaseFeedSource):
    """ VideoFeedSource
    """
    interface.implements(baseinterfaces.IFeedSource)
    component.adapts(IVideo)

    def getFeedEntries(self):
        """See IFeedSoure
        """
        return [baseinterfaces.IFeedEntry(self.context)]



class VideoFeedEntry(fatadapters.BaseFeedEntry):
    """ VideoFeedEntry
    """
    interface.implements(baseinterfaces.IFeedEntry)
    component.adapts(IVideo)

    def __init__(self, context):
        fatadapters.BaseFeedEntry.__init__(self, context)

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
        return self.context.title

    def getDescription(self):
        """ getDescription
        """
        return self.context.description

class ATFileEnclosure(object):
    """ ATFileEnclosure
    """
    interface.implements(baseinterfaces.IEnclosure)
    component.adapts(IVideo)

    def __init__(self, context):
        self.context = context
        self.enclosure = self.context.getFile()

    def getURL(self):
        """ getURL
        """
        return self.context.absolute_url()

    def getLength(self):
        """ getLength
        """
        return self.enclosure.get_size()

    def __len__(self):
        return self.getLength()

    def getMajorType(self):
        return self.getType().split('/')[0]

    def getMinorType(self):
        return self.getType().split('/')[1]

    def getType(self):
        return self.enclosure.getContentType()


