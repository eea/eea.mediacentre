from eea.mediacentre.bbb.fileimage_file import FileField
from eea.mediacentre.bbb.fileimage_file import FileDownloadWidget
from zope.app.form.browser import widget


class ImageField(FileField):
    """A field for representing an image.
    """

    def __init__(self, preferred_dimensions=None, **kw):
        super(ImageField, self).__init__(**kw)

        self.preferred_dimensions = preferred_dimensions

class ImageURLWidget(FileDownloadWidget):
    """Widget that returns the URL of the image
       This is clearly overkill, but it was the easy way to get
       something working fast.
       Revisit the consumer of this class and probably
       access the url inline there.
    """

    @property
    def base_url(self):
        contentobj = self.context.context.context
        return contentobj.absolute_url() + '/viewimage'

    def __call__(self):
        if not self._data:
            return widget.renderElement(u'span',
                                        cssClass='image-absent',
                                        contents='No image set')

        return self.url


