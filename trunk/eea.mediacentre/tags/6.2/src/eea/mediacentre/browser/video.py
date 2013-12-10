""" Video
"""
from Products.Archetypes.interfaces import ISchema
from Products.CMFCore.utils import getToolByName
from eea.mediacentre.interfaces import IVideo, IMediaPlayer
from zope.component import queryAdapter
from zope.component import adapts
from zope.interface import Interface, implements
from zope import schema
from Products.EEAContentTypes.content.validators import video_cloud_validator

from zope.schema import ValidationError
from zope.annotation.interfaces import IAnnotations

from eea.forms.widgets.ManagementPlanWidget import ManagementPlanCode

from Products.Five.browser import BrowserView

KEY = 'eea.mediacentre.multimedia'


def fancy_time_amount(v, show_legend=True):
    """Produce a friendly representation of the given time amount.  The
    value is expected to be in seconds as an int.

      >>> fancy_time_amount(391)
      u'06:31 (mm:ss)'

      >>> fancy_time_amount(360)
      u'06:00 (mm:ss)'

      >>> fancy_time_amount(6360)
      u'01:46:00 (hh:mm:ss)'

      >>> fancy_time_amount(360, False)
      u'06:00'

    """

    remainder = v
    hours = remainder / 60 / 60
    remainder -= hours * 60 * 60
    mins = remainder / 60
    secs = remainder - (mins * 60)

    if hours > 0:
        val = u'%02i:%02i:%02i' % (hours, mins, secs)
        legend = u' (hh:mm:ss)'
    else:
        val = u'%02i:%02i' % (mins, secs)
        legend = u' (mm:ss)'

    if show_legend:
        full = val + legend
    else:
        full = val

    return full


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
    adapts(IVideo)

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
        required=False,
        constraint=validateCloudUrl)


class CloudUrlEdit(object):
    """ Edit adapter for cloud url field which contains the embedding code
    for the video
    """
    implements(ICloudUrlEdit)
    adapts(IVideo)


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


class IVideoView(Interface):
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


class VideoView(BrowserView):
    """ Video view
    """

    def __init__(self, context, request):
        super(VideoView, self).__init__(context, request)
        self.context = context
        self.request = request
        self.video = IAnnotations(context).get(
            'p4a.plonevideo.atct.ATCTFileVideo') or {
                         "video_author": "",
                         "width": 600,
                         "height": 389,
                         "rich_description":
                                self.context.getField('text').get(self.context)
                     }


    def duration(self):
        """ duration
        """
        time = self.video.get('duration')
        if time:
            time = int(round(time or 0.0))
            return fancy_time_amount(time, show_legend=False)
        else:
            return None

    def author(self):
        """ Author
        """
        return self.video.get('video_author')

    def published_date(self):
        """ Published date
        """
        return getPublishedDate(self.context)

    def width_incl_player(self):
        """ Width  incl player
        """
        return self.video.get('width', 600) + 35

    def rich_description(self):
        """ Width  incl player
        """
        return self.context.getField('text').get(self.context)

    def cloud_url(self):
        """ Cloud Url
        """
        field = ICloudUrlEdit(self.context).cloud_url
        cloud_url = False
        if field:
            return cloudUrl(self)
        return cloud_url

    def media_player(self):
        """ Returns the flowplayer embed string
        """
        media_player = queryAdapter(self.context,
                                    interface=IMediaPlayer,
                                    name=u"video/x-flv")
        width = self.video.get('width', 600)
        height = self.video.get('height', 380)

        if media_player is None:
            return None
            # downloadUrl and ImageUrl are the params that we send as None since
        # they are  not needed
        s = u'<div class="media-player">%s</div>' % media_player(None, None,
                                                                 width, height)
        return s


class CloudVideoView(BrowserView):
    """ CloudVideo BrowserView
    """

    def cloud_url(self):
        """ Retrieve cloudUrl entry
        """
        return cloudUrl(self)

    def author(self):
        """ Author info
        """
        pass

    def rich_description(self):
        """ Rich Description
        """
        return self.context.getField('text').get(self.context)


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
