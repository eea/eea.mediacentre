""" p4a.* cleanup
"""
from zope.interface import noLongerProvides
from p4a.subtyper.interfaces import ISubtyped
from p4a.video.interfaces import IVideoContainerEnhanced, IVideoEnhanced
import transaction
import logging
log = logging.getLogger(__name__)


def remove_interface(ca, interface):
    """ Remove p4a.* from objects
    """
    count = 0
    iname = interface[0]
    iface = interface[1]
    log.info("STARTED %s Removal", iname)
    brains = ca.searchResults(object_provides=
                              iname,
                              Language="all")
    for brain in brains:
        obj = brain.getObject()
        try:
            noLongerProvides(obj, iface)
        except ValueError:
            log.info("could remove inteface %s from %s", iface, obj)
            continue
        obj.reindexObject(idxs=["object_provides"])
        log.info("%s removed for %s", iname, obj.absolute_url(1))
        count += 1
        if count % 50 == 0:
            transaction.commit()
    log.info("ENDED %s Removal", iname)


def cleanup_p4a_traces(context):
    """ Migration steps for getting rid of p4a.* interfaces
    """
    ca = context.portal_catalog
    interfaces = [("p4a.video.interfaces.IVideoEnhanced", IVideoEnhanced),
                  ("p4a.video.interfaces.IVideoContainerEnhanced",
                   IVideoContainerEnhanced),
                  ("p4a.video.interfaces.ISubtyped", ISubtyped)]
    for interface in interfaces:
        remove_interface(ca, interface)
