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

        return MAIN_VIDEO_TEMPLATE % {'videoid': videoid,
                                      'player': player,
                                      'title': contentobj.title,
                                      'config': config,
                                      }

MAIN_VIDEO_TEMPLATE = """
        <div class="flowplayer">
            <div id="%(videoid)s" class="embeddedvideo">
                Please enable javascript or upgrade to
                <a href="http://www.adobe.com/go/getflashplayer">Flash 9</a>
                to watch the video.
            </div>

            <script type="text/javascript">
            jQuery(document).ready(function($) {
                $("#%(videoid)s").flashembed({
                    src:'%(player)s'
                  },
                  {
                    config:%(config)s
                  }
                );
            });
            </script>

        </div>
"""
