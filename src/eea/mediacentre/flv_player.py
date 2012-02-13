""" FLV player
"""
from zope import interface
from zope import component
from p4a.video import interfaces
from Products.CMFCore import utils as cmfutils
import simplejson

class FLVVideoPlayer(object):
    """ FLV Video Player
    """
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
        player = portal_url + "/++resource++flowplayer/flowplayer-3.2.2.swf"

        #videoobj = interfaces.IVideo(contentobj)
        downloadurl = contentobj.absolute_url()
        videoid = 'video' + contentobj.getId().replace('.','').replace(' ', '-')

        # See flowplayer.org site for available options
        config = {
                'clip': {
                    'url':downloadurl,
                    'autoPlay': True,
                    'autoBuffering': True,
                    'scaling': 'fit',
                    'useNativeFullScreen': True,
                    },
                'plugins': {
                    'controls': {
                        'autoHide': 'never',
                        'url': portal_url + \
                '/%2B%2Bresource%2B%2Bflowplayer/flowplayer.controls-3.2.1.swf',
                        }
                    },
                }
        config = simplejson.dumps(config)

        # check if aspect ratio fits in 4:3 or 16:9 and fallback to 16:9 
        # if the video aspect ratio is not 4:3 or 16:9
        aspect_ratio = ""
        if width and height:
            ratio = float(width) / float(height)
            if ratio > 1.77:
                aspect_ratio = "-16-9"
            elif ratio < 1.34:
                aspect_ratio = "-4-3"
            else:
                aspect_ratio = "-16-9"
        return MAIN_VIDEO_TEMPLATE % {'videoid': videoid,
                                      'player': player,
                                      'title': contentobj.title,
                                      'config': config,
                                      'ratio' : aspect_ratio
                                      }

MAIN_VIDEO_TEMPLATE = """
        <div class="flowplayer">
            <div id="%(videoid)s" class="embeddedvideo%(ratio)s">
                Please enable javascript or upgrade to
                <a href="http://www.adobe.com/go/getflashplayer">Flash Player 11</a>
                to watch the video.
            </div>

            <script type="text/javascript">
            jQuery(document).ready(function($) {
                $("#%(videoid)s").flashembed({
                    src:'%(player)s',
                    version: [10, 0]
                  },
                  {
                    config:%(config)s,
                  }
                );
            });
            </script>

        </div>
"""
