""" p4a.* cleanup
"""
from zope.annotation import IAnnotations
import transaction
import logging
log = logging.getLogger(__name__)


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

    # set fields from annotation of objects
    set_fields_from_annotation(ca)

