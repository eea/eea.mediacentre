from Products.EEAContentTypes.content.FlashFile import FlashFile
from zope.component import adapts
from zope.interface import implements
from p4a.video.interfaces import IVideo
from p4a.common.formatting import fancy_time_amount
from p4a.video.interfaces import IMediaPlayer
from p4a.common.formatting import fancy_data_size
from eea.mediacentre.interfaces import IMediaDisplayInfo

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
    def video_type(self):
        return 'SWF'

    @property
    def video_image(self):
        return None

class SWFDisplay(SWFAdapter):
    implements(IMediaDisplayInfo)

    def __call__(self):
        info = {}
        info['width'] = self.width
        info['height'] = self.height
        info['title'] = self.title
        info['description'] = self.context.Description()
        info['video_type'] = self.video_type
        info['size'] = fancy_data_size(self.context.get_size())
        info['icon'] = self.context.getIcon()
        info['url'] = self.context.absolute_url()

        return info


class MediaPlayer(object):
    implements(IMediaPlayer)
    adapts(object)

    def __init__(self, context):
        self.context = context
        self.use_height_only = False
        self.max_width = 10000
        self.max_height = 10000

    def __call__(self, download_url, image_url):
        media_file = IVideo(self.context)
        width = media_file.width
        height = media_file.height
        url = self.context.absolute_url() + '/download'

        if media_file.width:
            width = int(float(str(media_file.width))) or self.max_width
        else:
            width = self.max_width
        if media_file.height:
            height = int(float(str(media_file.height))) or self.max_height
        else:
            height = self.max_height

        # videos shown as "related multimedia" should only show
        # as 180x135
        if width > self.max_width or height > self.max_height:
            width_diff = float(max(width - 180, 0))/width
            height_diff = float(max(height - 135, 0))/height
            diff = max(width_diff, height_diff)
            if diff > 0:
                width = width * (1-diff)
                height = height * (1-diff)

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
