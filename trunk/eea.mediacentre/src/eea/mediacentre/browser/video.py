from zope.app.schema.vocabulary import IVocabularyFactory
from zope.component import getUtility
from zope.formlib.form import FormFields
from p4a.video.browser.video import VideoListedSingle as P4AVideoListedSingle
from p4a.video.interfaces import IVideo, IMediaActivator
from p4a.video.browser import video
from eea.mediacentre.interfaces import IMediaType
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName

class VideoEditForm(video.VideoEditForm):
    """Form for editing video fields.  """

    form_fields = FormFields(IVideo).omit('rich_description', 'urls')

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
                type_ids = IMediaType(obj.context).types
            else:
                type_ids = IMediaType(obj).types

            types = sorted([vocab.getTerm(type_id).title for type_id in type_ids])
            if types:
                video['media_types'] = ', '.join(types)
            else:
                video['media_types'] = 'Other'

            video['portal_url'] = self.portal_url
        return video

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
