from p4a.fileimage.browser import ViewImage as P4AViewImage
from p4a.fileimage import utils

class ViewImage(P4AViewImage):
    """A view for streaming image content.
    """

    @property
    def _tempfilename(self):
        ifpackagename, ifname, fieldname = self.request.form.get('field', ':').split(':')
        if fieldname.endswith('.jpg') or fieldname.endswith('.png'):
            fieldname = fieldname[:-4]
        ifpackage = __import__(ifpackagename, {}, {}, ifpackagename)
        iface = getattr(ifpackage, ifname)
        adapted = iface(self.context)
        value = getattr(adapted, fieldname)

        if value is None:
            raise TypeError('Attribute for "%s.%s" should not be None'
                            % (str(adapted), fieldname))

        tempfilename = utils.write_ofsfile_to_tempfile(value)
        return tempfilename
