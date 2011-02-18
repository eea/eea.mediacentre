from p4a.fileimage.browser import ViewImage as P4AViewImage
from p4a.fileimage import utils

class ViewImage(P4AViewImage):
    """A view for streaming image content. This overrides the
       p4a.fileimage.browser.ViewImage view because of flowplayer.
       image urls must end with .jpg or .png, otherwise flowplayer
       doesn't figure out what type of image it is, so we add the
       extension to the url and remove it here.
    """

    def __call__(self):
        ifpackagename, ifname, fieldname = \
                       self.request.form.get('field', ':').split(':')
        if fieldname.endswith('.jpg') or fieldname.endswith('.png'):
            fieldname = fieldname[:-4]
        ifpackage = __import__(ifpackagename, {}, {}, ifpackagename)
        iface = getattr(ifpackage, ifname)
        adapted = iface(self.context)
        value = getattr(adapted, fieldname)

        return value.index_html(self.request, self.request.response)
