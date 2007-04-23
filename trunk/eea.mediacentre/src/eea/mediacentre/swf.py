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
        self.use_height_only = False

    def __call__(self):
        media_file = self.context
        width = media_file.width
        height = media_file.height
        bgcolor = media_file.context.getBgcolor()
        url = media_file.context.absolute_url() + '/download'

        if self.use_height_only:
            width_str = 'width="100%"'
        else:
            width_str = 'width="%d"' % width

        return """
        <div class="flashmovie">
            <embed type="application/x-shockwave-flash"
                   %(width)s height="%(height)s"
                   wmode="opaque" quality="high"
                   src="%(url)s" />
        </div>
        """ % { 'height': height,
                'width': width_str,
                'url': url }
