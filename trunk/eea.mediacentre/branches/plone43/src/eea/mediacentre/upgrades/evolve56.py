""" p4a.* cleanup
"""
from zope.interface import noLongerProvides
from p4a.subtyper.interfaces import ISubtyped
from p4a.video.interfaces import IVideoContainerEnhanced, IVideoEnhanced
import transaction
import logging
log = logging.getLogger(__name__)


def remove_video_enhanced_interfaces(ca):
    """ Remove p4a.video.interfaces.IVideoEnhanced from objects
    """
    count = 0
    log.info("STARTED p4a.video.interfaces.IVideoEnhanced Removal")
    brains = ca.searchResults(object_provides=
                              "p4a.video.interfaces.IVideoEnhanced",
                              Language="all")
    for brain in brains:
        obj = brain.getObject()
        noLongerProvides(obj, IVideoEnhanced)
        obj.reindexObject(idxs=["object_provides"])
        log.info("p4a.video.interfaces.IVideoEnhanced removed for %s",
                 obj.absolute_url(1))
        count += 1
        if count % 50 == 0:
            transaction.commit()
    log.info("ENDED p4a.video.interfaces.IVideoEnhanced Removal")


def cleanup_p4a_traces(context):
    """ Migration steps for getting rid of p4a.* interfaces
    """
    ca = context.portal_catalog
    remove_video_container(ca)
    remove_subtyper_interfaces(ca)
    remove_video_enhanced_interfaces(ca)


def remove_video_container(ca):
    """ Remove p4a.video.interfaces.IVideoContainerEnhanced from objects
    """
    count = 0
    log.info("STARTED p4a.video.interfaces.IVideoContainerEnhanced Removal")
    brains = ca.searchResults(object_provides=
                              "p4a.video.interfaces.IVideoContainerEnhanced",
                              Language="all")
    for brain in brains:
        obj = brain.getObject()
        noLongerProvides(obj, IVideoContainerEnhanced)
        obj.reindexObject(idxs=["object_provides"])
        log.info("p4a.video.interfaces.IVideoContainerEnhanced removed for %s",
                 obj.absolute_url(1))
        count += 1
        if count % 50 == 0:
            transaction.commit()
    log.info("ENDED p4a.video.interfaces.IVideoContainerEnhanced Removal")


def remove_subtyper_interfaces(ca):
    """ Remove ISubtyper from objects that implement IVideoEnhanced
    """
    log.info("STARTED p4a.subtyper.interfaces.ISubtyped Removal")
    count = 0
    brains = ca.searchResults(object_provides=
                              "p4a.video.interfaces.IVideoEnhanced",
                              Language="all")
    for brain in brains:
        if "p4a.subtyper.interfaces.ISubtyped" in brain.object_provides:
            obj = brain.getObject()
            noLongerProvides(obj, ISubtyped)
            obj.reindexObject(idxs=["object_provides"])
            log.info("p4a.subtyper.interfaces.ISubtyped removed for %s",
                     obj.absolute_url(1))
            count += 1
            if count % 50 == 0:
                transaction.commit()
    log.info("ENDED p4a.subtyper.interfaces.ISubtyped Removal")


