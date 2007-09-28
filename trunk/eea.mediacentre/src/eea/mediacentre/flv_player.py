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

        playlist = "[ { url: '%s'}, " % imageurl
        playlist += "{ url: '%s' } ]" % downloadurl 
        
        return """
        <div class="flowplayer">
            <div id="video%(videoid)s" class="embeddedvideo">
              Please enable javascript to watch the video.
            </div>
            <script type="text/javascript">
               function loadflash() {
              var so = new SWFObject("%(player)s?config={ playList: %(playlist)s, scaleSplash: true, initialScale: 'scale', showFullScreenButton: false }", "FlowPlayer", "%(width)s", "%(height)s", "7", "#ffffff");
                 so.addParam("AllowScriptAccess", "always");
                 so.addParam("wmode", "transparent");
                 so.write("video%(videoid)s");
                 return true;
               }
               AttachEvent(window, 'load', loadflash, false)
            </script>     
        </div>

        """ % {'videoid': contentobj.getId().replace('.','-'),
               'player': player,
               'title': title,
               'width': width,
               'height': height+16,
               'videoUrl': downloadurl + '/view',
               'playlist': playlist,
               'fullscreenUrl': fullscreenUrl,
               'showUrl': showUrl}
