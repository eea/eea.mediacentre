from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import getMultiAdapter
from zope.interface import Interface
from p4a.video.interfaces import IVideo

class IListedSingle(Interface):
    def single(obj=None, pos=None):
        pass

class ListedSingle(object):
    """listed single."""

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def single(self, obj, pos=None, relevance=None):
        video = IVideo(obj, None)
        if video:
            view = getMultiAdapter((self.context, self.request),
                                   name='video_listed_single')
            return view.single(video, pos, relevance)

        if obj.portal_type == 'Image':
            view = getMultiAdapter((self.context, self.request),
                                   name='image_listed_single')
            return view.single(obj, pos)

        return ''


class ImageListedSingle(object):

    template = ViewPageTemplateFile('image-listed-single.pt')

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def single(self, obj=None, pos=None):
        image = {
            'title': obj.Title(),
            'description': obj.Description(),
            'url': obj.absolute_url() + '/view',
            'media_types': 'Image',
            'preview_url': obj.absolute_url() + '/image_mini',
        }
        if pos is not None:
            image['oddeven'] = ['even', 'odd'][pos % 2]

        return self.template(image=image)
