from zope.interface import Interface, Attribute
from zope.schema import Choice, List

class IMediaCentre(Interface):
    """ This is the main media centre interface. This utility relies on
        plugins (providing IMediaCentrePlugin) to provide media files. """

    def getMedia(mediatype, size, search):
        """ Returns multimedia files that satisfies the criterias.
            If mediatype is specified only that certain type is returned.
            size is the number of files that should be returned.
            search is a dictionary with contraints of what media should
            be returned. These constraints can be plugin specific. """

    def getMediaTypes():
        """ Returns what media types are available, for instance
            interviews, maps and videos. """

    def getPluginNames():
        """ Returns all plugins that media centre uses. """

class IMediaCentrePlugin(Interface):
    """ A media centre plugin knows of a specific repository. The repository
        can be a catalog, relational database or filesystem. The media
        centre does not have to know about the details, it just asks the
        plugin of what is available. """

    name = Attribute("The name of the plugin")

    def getMedia():
        """ Returns multimedia files that satisfies the criterias.
            If mediatype is specified only that certain type is returned.
            size is the number of files that should be returned.
            search is a dictionary with contraints of what media should
            be returned. These constraints can be plugin specific. """

    def getMediaTypes():
        """ Returns what media types are available, for instance
            interviews, maps and videos. """

class IMediaType(Interface):
    """ A file object can be one of several types, including interviews,
        maps, videos. This interface is the API to ask about this type. """

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

class IPossibleMediaFile(Interface):
    """ Markter interface for files that are not yet media files. """

class IMediaProvider(Interface):
    media_type = Attribute("The type of media for this object")

    def media_items():
        """ Returns a list of media objects this provider finds available. """

class IMediaDisplayInfo(Interface):
    def __call__():
        """ Returns a dict of useful information for the ui. """

class IMultimedia(Interface): pass
class IInterview(IMultimedia): pass
class IVideo(IMultimedia): pass
class IInteractiveMap(IMultimedia): pass
class IAnimation(IMultimedia): pass
class IMindStretcher(IMultimedia): pass
