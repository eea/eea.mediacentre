""" Interfaces
"""
from zope.interface import Interface, Attribute
from zope.schema import Choice, List

class IMediaCentre(Interface):
    """ This is the main media centre interface. This utility relies on
        plugins (providing IMediaCentrePlugin) to provide media files.
    """

    def getMedia(self, mediatype, size, full_objects, search):
        """ Returns multimedia files that satisfies the criterias.
            If mediatype is specified only that certain type is returned.
            size is the number of files that should be returned.
            search is a dictionary with contraints of what media should
            be returned. These constraints can be plugin specific.
        """

    def getMediaTypes(self):
        """ Returns what media types are available, for instance
            interviews, maps and videos.
        """

    def getPluginNames(self):
        """ Returns all plugins that media centre uses.
        """

class IMediaCentrePlugin(Interface):
    """ A media centre plugin knows of a specific repository. The repository
        can be a catalog, relational database or filesystem. The media
        centre does not have to know about the details, it just asks the
        plugin of what is available.
    """

    name = Attribute("The name of the plugin")

    def getMedia(self):
        """ Returns multimedia files that satisfies the criterias.
            If mediatype is specified only that certain type is returned.
            size is the number of files that should be returned.
            search is a dictionary with contraints of what media should
            be returned. These constraints can be plugin specific.
        """

    def getMediaTypes(self):
        """ Returns what media types are available, for instance
            interviews, maps and videos.
        """

class IMediaType(Interface):
    """ A file object can be one of several types, including interviews,
        maps, videos. This interface is the API to ask about this type.
    """

    types = List(
        title = u"Media types",
        description = u"List of media types that this media file can tagged "
                      "with.",
        required = False,

        value_type=Choice(
            title = u"Media type",
            description = u"Media type of this file",
            vocabulary = """Media types""",
            )
    )

class IMediaProvider(Interface):
    """ Media Provider
    """
    media_type = Attribute("The type of media for this object")

    def media_items(self):
        """ Returns a list of media objects this provider finds available.
        """

class IMediaDisplayInfo(Interface):
    """ Media Display Info
    """
    def __call__(self):
        """ Returns a dict of useful information for the ui.
        """

class IMultimedia(Interface):
    """ Multimedia
    """
    pass

class IInterview(IMultimedia):
    """ Interview
    """
    pass


class IInteractiveMap(IMultimedia):
    """ Interactive Map
    """
    pass

class IAnimation(IMultimedia):
    """ Animation
    """
    pass

class IMindStretcher(IMultimedia):
    """ Mind Stretcher
    """
    pass


# class IVideo(Interface):
#     """ Marker interface for any type of videos in our portal
#     """

from zope import interface
from zope import schema
from eea.mediacentre.bbb import fileimage_file as p4afile
from eea.mediacentre.bbb import fileimage_image as p4aimage

from eea.mediacentre import EEAMessageFactory as _


class IVideo(interface.Interface):
    """Objects which have video information.
    """

    title = schema.TextLine(title=_(u'Title'), required=False)
    description = schema.Text(title=_(u'Description'), required=False)
    rich_description = schema.Text(title=_(u'Rich Text Description'),
                                   required=False)
    file = p4afile.FileField(title=_(u'File'), required=False)
    width = schema.Int(title=_(u'Width'), default=480, required=False,
                       readonly=False)
    height = schema.Int(title=_(u'Height'), default=360, required=False,
                        readonly=False)
    duration = schema.Float(title=_(u'Duration'), required=False, readonly=False)

    video_image = p4aimage.ImageField(title=_(u'Image'), required=False,
                                      preferred_dimensions=(320, 240))

    video_type = schema.TextLine(title=_(u'Type'),
                                 required=True,
                                 readonly=True)

    video_author = schema.TextLine(title=_(u'Author'), required=False)

    urls = schema.Tuple(
        title=_(u'Video URLs'), required=False, default=(),
        value_type=schema.Tuple(title=_(u'Mimetype and URL pair'),
                                min_length=2, max_length=2))

# BBB from p4a.video
class IMediaPlayer(Interface):
    """Media player represented as HTML.
    """

    def __call__(downloadurl, imageurl):
        """Return the HTML required to play the video content located
        at *downloadurl* with the *imageurl* representing the video.
        """


class IPossibleVideo(interface.Interface):
    """Objects which can have video information.
    """
