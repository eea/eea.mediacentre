from p4a.video.interfaces import IVideoProvider
from p4a.common.formatting import fancy_data_size
from eea.mediacentre.swf import MediaPlayerWidget

class ContainerView(object):
    """View for mind stretchers.
    """

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def video_items(self):
        provider = IVideoProvider(self.context)
        items = []

        for x in provider.video_items:
            aFile = x.context
            field = aFile.getFile()
            items.append( \
                {'title': x.title,
                 'url': aFile.absolute_url(),
                 'description': x.context.Description(),
                 'icon': aFile.getIcon(),
                 'size': fancy_data_size(aFile.get_size()),
                 'widget': MediaPlayerWidget(x)(),
                 })

        return items
