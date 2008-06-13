import random
from zope import interface
from zope import component
from p4a.video import interfaces
from Products.CMFCore import utils as cmfutils
from p4a.fileimage.image._widget import ImageURLWidget

class FLVVideoPlayer(object):
    interface.implements(interfaces.IMediaPlayer)
    component.adapts(object)

    def __init__(self, context):
        self.context = context
        # default we want the videos in their original size
        self.max_width = 10000
        self.max_height = 10000
        self.autoplay = True
        self.autobuffer = True

    def __call__(self, downloadurl, imageurl):
        showUrl = True
        if downloadurl:
            contentobj = self.context.context.context
            showUrl = False
        else:
            contentobj = self.context

        portal_tool = cmfutils.getToolByName(contentobj, 'portal_url')
        portal_url = portal_tool.getPortalObject().absolute_url()

        player = portal_url + "/++resource++flowplayer/FlowPlayerThermo.swf"
        fullscreenUrl = portal_url + "/++resource++flowplayer/fullscreen.js"
        
        title = contentobj.title

        videoobj = interfaces.IVideo(contentobj)
        width = int(float(videoobj.width))
        height = int(float(videoobj.height))

        # videos shown as "related multimedia" should only show as 180x135
        if width > self.max_width or height > self.max_height:
            width_diff = float(max(width - self.max_width, 0))/width
            height_diff = float(max(height - self.max_height, 0))/height
            diff = max(width_diff, height_diff)
            if diff > 0:
                width = width * (1-diff)
                height = height * (1-diff)

        # videos have autoplay and autobuffering turned on by default
        # the users of this view/flv-player can turn them off if they want
        autoplay = self.autoplay and 'true' or 'false'
        autobuffer = self.autobuffer and 'true' or 'false'

        downloadurl = contentobj.absolute_url()

        # the flowplayer we use now only supports jpg and png
        # and it only works if the image url actually ends with '.jpg'
        # this needs to be fixed properly in p4a, but for now this works
        # the p4a 'viewname' view is overridden and strips out this extension
        if videoobj.video_image is not None:
            field = interfaces.IVideo['video_image'].bind(videoobj)
            imageurl = ImageURLWidget(field, None).url + '.jpg'
        else:
            imageurl = portal_url + '/video-image.jpg'

        # autoplay doesn't work in flowplayer if there is a playlist with an
        # image at the beginning, so if autoplay we don't use the image
        template_to_use = MAIN_VIDEO_TEMPLATE
        if self.autoplay:
            playlist = "[ "
        else:
            playlist = "[ { url: '%s'}, " % imageurl
            template_to_use = SECONDARY_VIDEA_TEMPLATE
        playlist += "{ url: '%s' } ]" % downloadurl
        
        return template_to_use % {'videoid': contentobj.getId().replace('.','-'),
            			  'player': player,
            			  'title': title,
            			  'width': width,
            			  'height': height+16,
            			  'videoUrl': downloadurl + '/view',
            			  'playlist': playlist,
            			  'fullscreenUrl': fullscreenUrl,
            			  'showUrl': showUrl,
            			  'autoplay': autoplay,
            			  'autobuffer': autobuffer,
            			  'random': random.randint(1,2000000000) }
               
#
# Video templates list
#

MAIN_VIDEO_TEMPLATE = """
        <div class="flowplayer">
            <div id="video%(videoid)s" class="embeddedvideo">
                Please enable javascript or upgrade to <a href="http://www.adobe.com/go/getflashplayer">Flash 9</a> to watch the video.
            </div>
            <script type="text/javascript">
               function loadflash%(random)s() {
                 var so = new SWFObject("%(player)s?config={ playList: %(playlist)s, scaleSplash: true, initialScale: 'scale', showFullScreenButton: false, autoPlay: %(autoplay)s, autoBuffering: %(autobuffer)s }", "FlowPlayer%(random)s", "%(width)s", "%(height)s", "7", "#ffffff");
                 so.addParam("AllowScriptAccess", "always");
                 so.addParam("wmode", "transparent");
                 so.write("video%(videoid)s");
                 return true;
               }
               AttachEvent(window, 'load', loadflash%(random)s, false)
            </script>     
        </div>
"""

SECONDARY_VIDEA_TEMPLATE = """
        <div class="flowplayer">
            <div id="video%(videoid)s" class="embeddedvideo">
                Please enable javascript or upgrade to <a href="http://www.adobe.com/go/getflashplayer">Flash 9</a> to watch the video.
            </div>
            <script type="text/javascript">
               function loadflash%(random)s() {
                 var so = new SWFObject("%(player)s", "FlowPlayer%(random)s", "%(width)s", "%(height)s", "7", "#ffffff");
                 so.addVariable("config", "{ playList: %(playlist)s, scaleSplash: true, initialScale: 'scale', showFullScreenButton: false, autoPlay: %(autoplay)s, autoBuffering: %(autobuffer)s }");
                 so.write("video%(videoid)s");
                 return true;
               }
               AttachEvent(window, 'load', loadflash%(random)s, false)
            </script>     
        </div>
"""
