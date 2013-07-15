""" Single
"""
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import getMultiAdapter
from zope.interface import Interface
from p4a.video.interfaces import IVideo

class IListedSingle(Interface):
    """ Listed Single
    """

    def single(self, obj=None, pos=None):
        """ Single
        """
        pass

class ListedSingle(object):
    """ Listed single.
    """

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def single(self, obj, pos=None, relevance=None):
        """ Single
        """
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
    """ Image Listed Single
    """
    template = ViewPageTemplateFile('image-listed-single.pt')

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def single(self, obj=None, pos=None):
        """ Single
        """
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
