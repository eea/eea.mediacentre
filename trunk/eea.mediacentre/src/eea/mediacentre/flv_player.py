from zope import interface
from zope import component
from p4a.video import interfaces
from Products.CMFCore import utils as cmfutils
from p4a.fileimage.image._widget import ImageURLWidget

def generate_config(**kw):
    text = 'config : {'
    for key, value in kw.items():
        if value is not None and value is not 'false' and value is not 'true':
            text += "%s: '%s', " % (key, value)
        else:
            text += "%s: %s, " % (key, value)            
    if text.endswith(', '):
        text = text[:-2]
    text += ' }'
    return text

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
    
    def __call__(self, downloadurl, imageurl, width, height):
        showUrl = True
        if downloadurl:
            contentobj = self.context.context.context
            showUrl = False
        else:
            contentobj = self.context

        portal_tool = cmfutils.getToolByName(contentobj, 'portal_url')
        portal_url = portal_tool.getPortalObject().absolute_url()

        player = portal_url + "/++resource++flowplayer/FlowPlayerLight.swf"
        
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
        # valentine.imagescale handles this and strips out the extension
        imageurl = contentobj.absolute_url() + '/image_thumb.jpg'

        config = generate_config(videoFile=downloadurl,
                                 splashImageFile=imageurl,
                                 autoPlay=autoplay,
                                 autoBuffering=autobuffer,
                                 useNativeFullScreen='true',
                                 initialScale='fit') 

        template_to_use = MAIN_VIDEO_TEMPLATE
        return template_to_use % {'videoid': contentobj.getId().replace('.',''),
                                  'player': player,
                                  'title': contentobj.title,
                                  'width': width,
                                  'height': height+16,
                                  'config': config}

        
MAIN_VIDEO_TEMPLATE = """
        <div class="flowplayer">
            <div id="video%(videoid)s" class="embeddedvideo">
                Please enable javascript or upgrade to <a href="http://www.adobe.com/go/getflashplayer">Flash 9</a> to watch the video.
            </div>

            <script type="text/javascript">
            $(document).ready(function() {
                $("#video%(videoid)s").flashembed({
                    src:'%(player)s'
                  },
                  { 
                    %(config)s
                  } 
                );
            });
            </script>

        </div>
"""
