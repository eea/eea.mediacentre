""" PloneVideo atct module
"""

from Products.ATContentTypes import interface as atctifaces
# from p4a.video import videoanno
from eea.mediacentre.bbb import video_videoanno as videoanno
from zope import component
from zope import interface
# from p4a.video import interfaces
from eea.mediacentre import interfaces
from p4a.video.interfaces import IMediaActivator, IVideoDataAccessor
from p4a.common.descriptors import atfield
from OFS import Image as ofsimage

import os
from eea.mediacentre.bbb import fileimage_fileutils as fileutils

import logging
logger = logging.getLogger(__name__)


# class AbstractATCTVideo(videoanno.AnnotationVideo):
class AbstractATCTVideo(videoanno.AnnotationVideo):
    """ AbstractATCTVideo
    """

    interface.implements(interfaces.IVideoAdapter)
    component.adapts(atctifaces.IFileContent)

    file = None

    title = atfield('title', 'context')
    description = atfield('description', 'context')

    def _get_video_image(self):
        """ _get_video_image
        """
        v = self.video_data.get('video_image', None)
        if v == None or v.get_size() == 0:
            return None
        return v
    def _set_video_image(self, v):
        """ _set_video_image
        """
        if v == interfaces.IVideoAdapter['video_image'].missing_value:
            return
        upload = v
        if isinstance(upload, ofsimage.Image):
            image = upload
        else:
            image = ofsimage.Image(id=upload.filename,
                                   title=upload.filename,
                                   file=upload)
        self.video_data['video_image'] = image
    video_image = property(_get_video_image, _set_video_image)

    @property
    def video_type(self):
        """ video_type
        """
        mime_type = self.context.get_content_type()
        adapters = component.getAdapters((self.context,),
                                         IVideoDataAccessor)
        if unicode(mime_type) in [adapter[0] for adapter in adapters]:
            accessor = component.getAdapter(self.context,
                                            IVideoDataAccessor,
                                            unicode(mime_type))
            return accessor.video_type
        else:
            return None

    def _load_video_metadata(self):
        """Retrieve video metadata from the raw file data and update
        this object's appropriate metadata fields.
        """
        # currently unused

    def _save_video_metadata(self):
        """Write the video metadata fields of this object as metadata
        on the raw file data.
        """
        # currently unused

    def __str__(self):
        """ __str__
        """
        return '<p4a.video %s title=%s>' % (self.__class__.__name__, self.title)
    __repr__ = __str__


@interface.implementer(interfaces.IVideoAdapter)
@component.adapter(atctifaces.IFileContent)
def ATCTFileVideo(context):
    """ ATCTFileVideo
    """
    if not interfaces.IVideo.providedBy(context):
        return None
    return _ATCTFileVideo(context)


class _ATCTFileVideo(AbstractATCTVideo):
    """An IVideo adapter designed to handle ATCT based file content.
    """

    ANNO_KEY = 'p4a.plonevideo.atct.ATCTFileVideo'

    def _get_file(self):
        """ _get_file
        """
        field = self.context.getPrimaryField()
        return field.getEditAccessor(self.context)()
    def _set_file(self, v):
        """ _set_file
        """
        if v != interfaces.IVideoAdapter['file'].missing_value:
            field = self.context.getPrimaryField()
            field.getMutator(self.context)(v)
    file = property(_get_file, _set_file)

    def _load_video_metadata(self):
        """Retrieve video metadata from the raw file data and update
        this object's appropriate metadata fields.
        """
        mime_type = self.context.get_content_type()
        accessor = component.queryAdapter(self.context,
                                          IVideoDataAccessor,
                                          unicode(mime_type))
        if accessor is not None:
            field = self.context.getPrimaryField()
            filename = fileutils.write_ofsfile_to_tempfile(
                field.getEditAccessor(self.context)(),
                self.context.getId())
            accessor.load(filename)
            try:
                os.remove(filename)
            except OSError, err:
                logger.exception('Error while trying to clean up temp files %s',
                                 err)



def load_metadata(obj, evt):
    """An event handler for loading metadata.
    """
    obj._load_video_metadata()


def attempt_media_activation(obj, evt):
    """Try to activiate the media capabilities of the given object.
    """

    activator = IMediaActivator(obj)

    if activator.media_activated:
        return

    mime_type = obj.get_content_type()
    try:
        accessor = component.getAdapter(obj,
                                        IVideoDataAccessor,
                                        unicode(mime_type))
    except Exception:
        accessor = None

    if accessor is not None:
        activator.media_activated = True
        update_dublincore(obj, evt)
        update_catalog(obj, evt)


def update_dublincore(obj, evt):
    """Update the dublincore properties.
    """

    video = interfaces.IVideoAdapter(obj, None)
    if video is not None:
        obj.setTitle(video.title)

def update_catalog(obj, evt):
    """Reindex the object in the catalog.
    """
    obj.reindexObject()
