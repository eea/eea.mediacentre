""" Subtyper
"""
from eea.mediacentre.interfaces import IMediaType
from zope.annotation.interfaces import IAnnotations
from zope.component import adapter
from p4a.subtyper.interfaces import ISubtypeAddedEvent, ISubtypeRemovedEvent
from eea.mediacentre.mediatypes import KEY

@adapter(ISubtypeAddedEvent)
def subtype_added(evt):
    """ Adds media type to object and indirectly catalog.
    """
    obj = evt.object
    try:
        media = IMediaType(obj)
        if not media.types:
            media.types = ['other']
    except TypeError:
        # an object is subtyped that isn't video enhanced, so we ignore it
        pass

@adapter(ISubtypeRemovedEvent)
def subtype_removed(evt):
    """ Removes media type from object and indirectly catalog.
    """
    obj = evt.object
    anno = IAnnotations(obj)
    if anno.has_key(KEY):
        del anno[KEY]
