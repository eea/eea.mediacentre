from zope.app.schema.vocabulary import IVocabularyFactory
from zope.component import getUtility
from p4a.common.formatting import fancy_time_amount
from p4a.video.browser.video import VideoListedSingle as P4AVideoListedSingle
from p4a.video.interfaces import IVideo, IMediaActivator
from p4a.video.browser import video as vid
from eea.mediacentre.interfaces import IMediaType
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
#from Products.ZCatalog.CatalogBrains import AbstractCatalogBrain

def getMediaTypes(obj):
    if obj is not None:
        vocab = getUtility(IVocabularyFactory, name="Media types")(obj)

        # if obj is an IVideo it's an adapted media file, then we want to
        # use the adapter's context, otherwise we use obj as it is
        if IVideo.providedBy(obj):
            type_ids = IMediaType(obj.context).types
        else:
            type_ids = IMediaType(obj).types

        types = sorted([vocab.getTerm(type_id).title for type_id in type_ids
])
        if types:
            return ', '.join(types)
        else:
            return 'Other'

def getDuration(obj):
    video = IVideo(obj)
    if video.duration:
        duration = int(round(video.duration or 0.0))
        return fancy_time_amount(duration, show_legend=False)
    else:
        return None

def getPublishedDate(obj):
    time = obj.EffectiveDate()
    tool = getToolByName(obj, 'translation_service')
    return tool.ulocalized_time(time, None, obj,
                                domain='plone')

class VideoEditForm(vid.VideoEditForm):
    """Form for editing video fields.  """

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.form_fields = self.form_fields.omit('urls')

class VideoListedSingle(P4AVideoListedSingle):
    """Video listed single."""

    template = ViewPageTemplateFile('video-listed-single.pt')

    # override safe_video from p4a.video because we need to add media_types
    def safe_video(self, obj=None, pos=None, relevance=None):
        video = super(VideoListedSingle, self).safe_video(obj, pos, relevance)
        if obj is not None:
            vocab = getUtility(IVocabularyFactory, name="Media types")(obj)

            # if obj is an IVideo it's an adapted media file, then we want to
            # use the adapter's context, otherwise we use obj as it is
            if IVideo.providedBy(obj):
                videoobj = obj.context
                adapter = obj
            else:
                videoobj = obj
                adapter = IVideo(obj)

            type_ids = IMediaType(videoobj).types

            types = sorted([vocab.getTerm(type_id).title for type_id in type_ids])
            if types:
                video['media_types'] = ', '.join(types)
            else:
                video['media_types'] = 'Other'

            video['portal_url'] = self.portal_url
            video['published_date'] = getPublishedDate(videoobj)
            video['duration'] = getDuration(videoobj)
            video['author'] = adapter.video_author
        return video

class IVideoView(vid.IVideoView):
    def media_types(): #pylint: disable-msg = E0211
        pass
    def duration(): #pylint: disable-msg = E0211 
        pass
    def author():  #pylint: disable-msg = E0211
        pass
    def published_date(): #pylint: disable-msg = E0211 
        pass
    def width_incl_player(): #pylint: disable-msg = E0211 
        pass

class VideoView(vid.VideoView):

    def __init__(self, context, request):
        super(VideoView, self).__init__(context, request)
        self.context = context
        self.request = request
        self.video = IVideo(context)

    def media_types(self):
        return getMediaTypes(self.context)

    def duration(self):
        return getDuration(self.context)

    def author(self):
        return self.video.video_author

    def published_date(self):
        return getPublishedDate(self.context)

    def width_incl_player(self):
        return self.video.width + 35

class VideoUtils(object):
    """ A browser view for video utility methods. """

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def showEditMetadataTab(self):
        mship = getToolByName(self.context, 'portal_membership')
        if mship.isAnonymousUser():
            return False

        if not self.context.isTranslatable():
            return False

        current = self.context.getLanguage()
        return current != 'en'

class Activate(object):
    """ This view activates all FlashFile objects that are not
        already activated. """

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        brains = catalog.searchResults(portal_type='FlashFile')
        for brain in brains:
            obj = brain.getObject()
            activator = IMediaActivator(obj)
            if not activator.media_activated:
                activator.media_activated = True
