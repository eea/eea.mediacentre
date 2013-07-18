""" Interfaces
"""
from zope.interface import Interface


class IMultimedia(Interface):
    """ Multimedia
    """
    pass


class IAnimation(IMultimedia):
    """ Animation
    """
    pass


class IVideo(Interface):
    """ Marker interface for any type of videos in our portal
    """


# BBB from p4a.video
class IMediaPlayer(Interface):
    """Media player represented as HTML.
    """

    def __call__(downloadurl, imageurl):
        """Return the HTML required to play the video content located
        at *downloadurl* with the *imageurl* representing the video.
        """


class IPossibleVideo(Interface):
    """Objects which can have video information.
    """
