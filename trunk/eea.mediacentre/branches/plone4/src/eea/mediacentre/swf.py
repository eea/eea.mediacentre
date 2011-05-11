""" SWF
"""
#TODO: fix me, plone4
#from Products.EEAContentTypes.content.FlashFile import FlashFile
from eea.mediacentre.interfaces import IMediaDisplayInfo
from p4a.common.formatting import fancy_data_size
from p4a.plonevideo.atct import _ATCTFileVideo
from p4a.video.interfaces import IMediaPlayer
from p4a.video.interfaces import IVideo, IVideoEnhanced
from zope.component import adapts, adapter
from zope.interface import implements, implementer

#TODO: fix me, plone4
#@implementer(IVideo)
#@adapter(FlashFile)
#def SWFAdapter(context):
#    if not IVideoEnhanced.providedBy(context):
#        return None
#    return _SWFAdapter(context)

class _SWFAdapter(_ATCTFileVideo):
    """ We inherit attributes from ATCTFileVideo, but width
        and height are still stored in the FlashFile schema
    """

    def _get_width(self):
        """ Get width
        """
        return self.context.getWidth()

    def _set_width(self, width):
        """ Set width
        """
        self.context.setWidth(width)

    width = property(_get_width, _set_width)

    def _get_height(self):
        """ Get height
        """
        return self.context.getHeight()

    def _set_height(self, height):
        """ Set height
        """
        self.context.setHeight(height)

    height = property(_get_height, _set_height)

class SWFDisplay(_SWFAdapter):
    """ SWF Display
    """
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
    """ Media Player
    """
    implements(IMediaPlayer)
    adapts(object)

    def __init__(self, context):
        self.context = context
        self.use_height_only = False
        self.max_width = 10000
        self.max_height = 10000

    def __call__(self, download_url, image_url, width=None, height=None):
        # we have shockwave flash support both in FlashFile and
        # File portal types. The video is found differently
        if getattr(self.context, 'portal_type', '') == 'FlashFile':
            media_file = IVideo(self.context)
            url = self.context.absolute_url() + '/getFile'
        else:
            media_file  = IVideo(self.context.context.context)
            url = self.context.context.context.absolute_url() + '/getFile'

        width = media_file.width
        height = media_file.height

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
