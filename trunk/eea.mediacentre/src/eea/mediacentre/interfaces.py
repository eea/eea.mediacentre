from zope.interface import Interface, Attribute

class IMediaCentre(Interface):
    """ This is the main media centre interface. This utility relies on
        plugins (providing IMediaCentrePlugin) to provide media files. """

    def getMedia():
        """ Returns all existing media. """

    def getMediaByType(mediatype, search):
        """ Returns media of type 'mediatype'. 'search' is a dictionary
            with contraints of what media should be returned. """

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
        """ Returns all existing media. """

    def getMediaByType(mediatype, search):
        """ Returns media of type 'mediatype'. 'search' is a dictionary
            with contraints of what media should be returned. """

    def getMediaTypes():
        """ Returns what media types are available, for instance
            interviews, maps and videos. """
