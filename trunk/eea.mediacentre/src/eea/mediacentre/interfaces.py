from zope.interface import Interface, Attribute
from zope.schema import Choice

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

    media_type = Choice(
            title = u"Media type",
            description = u"Media type of this file",
            required = False,
            vocabulary = """Media types""",
            )

class IPossibleMediaFile(Interface):
    """ Markter interface for files that are not yet media files. """

class IMultimedia(Interface):
    """ Marker interface for multimedia. """

class IInterview(IMultimedia):
    """ Marker interface for interviews. """

class IThemeInterviewProvider(Interface):
    """ Marker interface for interview folder. """

class IInteractiveMap(IMultimedia):
    """ Marker interface for maps. """

class IThemeInteractiveMapProvider(Interface):
    """ Marker interface for map folder. """

class IVideo(IMultimedia):
    """ Marker interface for videos. """

class IThemeVideoProvider(Interface):
    """ Marker interface for video folder. """

class IMindStretcher(IMultimedia):
    """ Marker interface for mind stretchers. """

class IThemeMindStretcherProvider(Interface):
    """ Marker interface for mind stretcher folder. """

class IImage(IMultimedia):
    """ Marker interface for images. """

class IThemeImageProvider(Interface):
    """ Marker interface for image folder. """

class IAnimation(IMultimedia):
    """ Marker interface for animations. """

class IThemeAnimationProvider(Interface):
    """ Marker interface for animation folder. """
