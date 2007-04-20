from Products.EEAContentTypes.content.FlashFile import FlashFile
from zope.component import adapts
from zope.interface import implements
from p4a.video.interfaces import IVideo
from p4a.common.formatting import fancy_time_amount

class SWFAdapter(object):
    implements(IVideo)
    adapts(FlashFile)

    def __init__(self, context):
        self.context = context

    @property
    def title(self):
        return self.context.Title()

    @property
    def file(self):
        return self.context.getFile()

    @property
    def width(self):
        return self.context.getWidth()

    @property
    def height(self):
        return self.context.getHeight()

    @property
    def duration(self):
        return 0

    @property
    def video_image(self):
        return None

    @property
    def video_type(self):
        return 'SWF'


class MediaPlayerWidget(object):

    def __init__(self, context):
        self.context = context

    def __call__(self):
        media_file = self.context
        width = media_file.width
        height = media_file.height
        bgcolor = media_file.context.getBgcolor()
        url = media_file.context.absolute_url() + '/download'

        return """
        <div style="width: %(width)s; height: %(height)s" class="flashmovie">
            <embed type="application/x-shockwave-flash"
                   width="%(width)s" height="%(height)s"
                   wmode="opaque" bgcolor="%(bgcolor)s"
                   quality="high" src="%(url)s" />
        </div>
        """ % { 'width': width,
                'height': height,
                'url': url,
                'bgcolor': bgcolor }
