from zope import interface
from zope import component
from p4a.video import interfaces
from Products.CMFCore import utils as cmfutils

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
    
    def __call__(self, downloadurl, imageurl, width, height):
        if downloadurl:
            contentobj = self.context.context.context
        else:
            contentobj = self.context

        portal_tool = cmfutils.getToolByName(contentobj, 'portal_url')
        portal_url = portal_tool.getPortalObject().absolute_url()
        player = portal_url + "/++resource++flowplayer/FlowPlayerLight.swf"
        
        videoobj = interfaces.IVideo(contentobj)
        downloadurl = contentobj.absolute_url()
        videoid = 'video' + contentobj.getId().replace('.','')

        config = generate_config(videoFile=downloadurl,
                                 autoPlay=True,
                                 autoBuffering=True,
                                 useNativeFullScreen='true',
                                 initialScale='fit') 

        template_to_use = MAIN_VIDEO_TEMPLATE
        return template_to_use % {'videoid': videoid,
                                  'player': player,
                                  'title': contentobj.title,
                                  'config': config}

        
MAIN_VIDEO_TEMPLATE = """
        <div class="flowplayer">
            <div id="%(videoid)s" class="embeddedvideo">
                Please enable javascript or upgrade to <a href="http://www.adobe.com/go/getflashplayer">Flash 9</a> to watch the video.
            </div>

            <script type="text/javascript">
            $(document).ready(function() {
                $("#%(videoid)s").flashembed({
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
