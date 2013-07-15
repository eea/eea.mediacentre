""" Video
"""
from Products.Archetypes.interfaces import ISchema
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from eea.mediacentre.interfaces import IMediaType
#from p4a.common import at
from eea.mediacentre.bbb import common_at as at
from p4a.common.formatting import fancy_time_amount
from p4a.video.browser import video as vid
from p4a.video.browser.video import VideoListedSingle as P4AVideoListedSingle
from p4a.video.interfaces import IVideo, IMediaActivator
from p4a.video.interfaces import IVideoEnhanced
from zope.schema.interfaces import IVocabularyFactory
from zope.component import adapts
from zope.component import getUtility
from zope.formlib.form import FormFields
from zope.interface import Interface, implements
from zope import schema
from eea.geotags.widget.location import FormlibGeotagWidget
from Products.EEAContentTypes.content.validators import video_cloud_validator

from zope.schema import ValidationError
from zope.annotation.interfaces import IAnnotations

# Uncomment below is single geotag field is needed
#from Products.EEAContentTypes.subtypes import IGeotagSingleEdit

# Uncomment below is multiple geotags field is needed
from Products.EEAContentTypes.subtypes import IGeotagMultiEdit

from eea.forms.widgets.ManagementPlanWidget import \
                                FormlibManagementPlanWidget
from eea.forms.widgets.ManagementPlanWidget import ManagementPlanCode

from Products.Five.browser import BrowserView


KEY = 'eea.mediacentre.multimedia'

def getMediaTypes(obj):
    """ Get Media Types
    """
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
    """ Get Duration
    """
    video = IVideo(obj)
    if video.duration:
        duration = int(round(video.duration or 0.0))
        return fancy_time_amount(duration, show_legend=False)
    else:
        return None

def getPublishedDate(obj):
    """ Get Published Date
    """
    time = obj.EffectiveDate()
    tool = getToolByName(obj, 'translation_service')
    return tool.ulocalized_time(time, None, None, obj,
                                domain='plone')

def cloudUrl(obj):
    """ Retrieve cloudUrl field information
    """
    cloud_url = False
    mapping = IAnnotations(obj.context)
    multimedia = mapping.get('eea.mediacentre.multimedia')
    if multimedia:
        cloud_url = multimedia.get('cloud_url')
    return cloud_url

class IManagementPlanCodeEdit(Interface):
    """ Interface for edit forms that edit management plan code
    """
    management_plan = ManagementPlanCode(
            title=u"Management plan",
            description=u"The management plan year and code",
            years_vocabulary='Temporal coverage')

class ManagementPlanCodeEdit(object):
    """ Edit adapter for management plan code
    """
    implements(IManagementPlanCodeEdit)
    adapts(IVideoEnhanced)

    def __init__(self, context):
        self.context = context

    def get_management(self):
        """ Get management plan
        """
        obj_schema = ISchema(self.context)
        field = obj_schema['eeaManagementPlan']
        accessor = field.getAccessor(self.context)
        return accessor()

    def set_management(self, value):
        """ Set management plan
        """
        obj_schema = ISchema(self.context)
        field = obj_schema['eeaManagementPlan']
        mutator = field.getMutator(self.context)
        mutator(value)

    management_plan = property(get_management, set_management)


class InvalidCloudUrl(ValidationError, Exception):
    "Please enter a video link from Youtube or Vimeo only"
    pass

def validateCloudUrl(value):
    """ formlib validator for the cloudUrl field
    """
    if value:
        if ('youtu' not in value and 'vimeo' not in value):
            raise InvalidCloudUrl(value)
    return True

class ICloudUrlEdit(Interface):
    """ Interface for zope.formlib edit forms of cloud url field
    """
    cloud_url = schema.Text(
            title=u"Cloud Url",
            description=u"The external video link from Vimeo or Youtube",
            required = False,
            constraint=validateCloudUrl)

class CloudUrlEdit(object):
    """ Edit adapter for cloud url field which contains the embedding code
    for the video
    """
    implements(ICloudUrlEdit)
    adapts(IVideoEnhanced)


    def __init__(self, context):
        self.context = context
        self.context = context

    def get_cloudUrl(self):
        """ Get cloud url embbed code for video
        """
        obj_schema = ISchema(self.context)
        field = obj_schema['cloudUrl']

        accessor = field.getAccessor(self.context)
        return accessor()

    def set_cloudUrl(self, value):
        """ Set cloud url embedd code for video
        """
        # function from eeacontenttypes.validators which
        # sanitizes youtube and vimeo links before it is 
        # added to the cloudUrl field
        video_cloud_validator(value, self.context)
    cloud_url = property(get_cloudUrl, set_cloudUrl)

class VideoEditForm(vid.VideoEditForm):
    """ Form for editing video fields.
    """
    # Uncomment below is single geotag field is needed
#    form_fields = FormFields(IVideo,
#                              IManagementPlanCodeEdit,
#                              IGeotagSingleEdit)

    # Uncomment below is multiple geotags field is needed
    
    form_fields = FormFields( IVideo,
                              IManagementPlanCodeEdit,
                              ICloudUrlEdit,
                              IGeotagMultiEdit)

    
    form_fields = form_fields.omit('urls')
    form_fields['rich_description'].custom_widget = at.RichTextEditWidget
    form_fields['management_plan'].custom_widget = FormlibManagementPlanWidget
    form_fields['geotag'].custom_widget = FormlibGeotagWidget

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.form_fields['cloud_url'].field.required = False

        self.form_fields = self.form_fields.omit('urls')

class VideoListedSingle(P4AVideoListedSingle):
    """ Video listed single.
    """

    template = ViewPageTemplateFile('video-listed-single.pt')

    # override safe_video from p4a.video because we need to add media_types
    def safe_video(self, obj=None, pos=None, relevance=None):
        """ Safe video
        """
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

            types = sorted([vocab.getTerm(type_id).title
                                     for type_id in type_ids])
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
    """ Video view
    """
    def media_types(self):
        """ Media types
        """
        pass

    def duration(self):
        """ Duration
        """
        pass

    def author(self):
        """ Author
        """
        pass

    def published_date(self):
        """ Published date
        """
        pass

    def width_incl_player(self):
        """ Width incl player
        """
        pass

class VideoView(vid.VideoView):
    """ Video view
    """

    def __init__(self, context, request):
        super(VideoView, self).__init__(context, request)
        self.context = context
        self.request = request
        self.video = IVideo(context)

    def media_types(self):
        """ Media types
        """
        return getMediaTypes(self.context)

    def duration(self):
        """ duration
        """
        return getDuration(self.context)

    def author(self):
        """ Author
        """
        return self.video.video_author

    def published_date(self):
        """ Published date
        """
        return getPublishedDate(self.context)

    def width_incl_player(self):
        """ Width  incl player
        """
        return self.video.width + 35

    def cloud_url(self):
        """ Cloud Url
        """
        field = ICloudUrlEdit(self.context).cloud_url
        cloud_url = False
        if field:
            return cloudUrl(self)
        return cloud_url


class CloudVideoView(BrowserView):
    """ CloudVideo BrowserView
    """
    def cloud_url(self):
        """ Retrive cloudUrl entry
        """
        return cloudUrl(self)

    def author(self):
        """ Author info
        """
        pass

    def rich_description(self):
        """ Rich Description
        """
        pass

class VideoUtils(object):
    """ A browser view for video utility methods.
    """

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def showEditMetadataTab(self):
        """ Show Edit Metadata Tab
        """
        mship = getToolByName(self.context, 'portal_membership')
        if mship.isAnonymousUser():
            return False

        if not self.context.isTranslatable():
            return False

        current = self.context.getLanguage()
        return current != 'en'

class Activate(object):
    """ This view activates all FlashFile objects that are not
        already activated.
    """

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

