""" p4a.* cleanup
"""
from zope.interface import noLongerProvides
from p4a.subtyper.interfaces import ISubtyped
from p4a.video.interfaces import IVideoContainerEnhanced, IVideoEnhanced
from zope.annotation import IAnnotations
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


def set_fields_from_annotation(ca):
    """ Set fields from object annotation
    """
    count = 0
    log.info("STARTED setting rich description and image on video file")
    brains = ca.searchResults(object_provides=
                              "eea.mediacentre.interfaces.IVideo",
                              portal_type="File")
    objs = [brain.getObject() for brain in brains]
    for obj in objs:
        info = IAnnotations(obj)
        p4a = info.get('p4a.plonevideo.atct.ATCTFileVideo')
        if p4a:
            rich_description = p4a.get('rich_description')
            if rich_description:
                obj.getField('text').set(obj, rich_description)
                log.info("%s rich_description migrated to text field",
                         obj.absolute_url())

            image = p4a.get('video_image')
            if image:
                obj.getField('image').set(obj, image)
                log.info("%s video_image migrated to image field",
                         obj.absolute_url())
            if rich_description or image:
                obj.reindexObject()
                count += 1
                if count % 50 == 0:
                    transaction.commit()

    log.info("ENDED setting rich description and image on video file")



def cleanup_p4a_traces(context):
    """ Migration steps for getting rid of p4a.* interfaces
    """
    ca = context.portal_catalog
    interfaces = [("p4a.video.interfaces.IVideoEnhanced", IVideoEnhanced),
                  ("p4a.video.interfaces.IVideoContainerEnhanced",
                   IVideoContainerEnhanced),
                  ("p4a.video.interfaces.ISubtyped", ISubtyped)]

    # remove interfaces
    for interface in interfaces:
        remove_interface(ca, interface)

    # set fields from annotation of objects
    set_fields_from_annotation(ca)

