""" Media
"""
from Products.Archetypes.atapi import AnnotationStorage
from datetime import datetime
from Products.CMFCore.utils import getToolByName
from archetypes.schemaextender.field import ExtensionField
from archetypes.schemaextender.interfaces import ISchemaExtender
from zope.component import getUtility
from zope.interface import implements
from p4a.common.formatting import fancy_time_amount, fancy_data_size
from p4a.plonevideo.atct import _ATCTFileVideo
from p4a.video.interfaces import IVideoEnhanced
from eea.mediacentre.interfaces import IMediaCentre, IMediaProvider
from eea.mediacentre.mediacentre import MEDIA_SEARCH_KEY
from eea.themecentre.themecentre import getTheme
from eea.dataservice.fields.ManagementPlanField import ManagementPlanField
from eea.dataservice.widgets.ManagementPlanWidget import ManagementPlanWidget

def P4AVideoDisplayInfoAdapter(context):
    """ P4A Video Display Info Adapter
    """
    if not IVideoEnhanced.providedBy(context):
        return None
    return P4AVideoDisplayInfo(context)

class P4AVideoDisplayInfo(_ATCTFileVideo):
    """ P4A Video Display Info
    """
    def __call__(self):
        info = {}
        info['title'] = self.title
        info['description'] = self.context.Description()
        info['height'] = self.height
        info['width'] = self.width
        info['duration'] = fancy_time_amount(int(round(self.duration)))
        info['video_image'] = self.video_image
        info['video_type'] = self.video_type
        info['size'] = fancy_data_size(self.context.get_size())
        info['icon'] = self.context.getIcon()
        info['url'] = self.context.absolute_url()
        return info


class MediaProvider(object):
    """ Media Provider
    """
    implements(IMediaProvider)

    def __init__(self, context):
        self.context = context
        # this can be changed by someone who wants a specific media type
        self.media_type = None

    @property
    def media_items(self):
        """ Media items
        """
        currentTheme = getTheme(self.context)
        mediacentre = getUtility(IMediaCentre)
        search = { MEDIA_SEARCH_KEY: { 'theme': currentTheme }}
        files = mediacentre.getMedia(self.media_type, full_objects=False,
                                     search=search)

        videos = []
        for media_dict in files:
            videos.append(media_dict['object'])

        return videos


class TopicMediaProvider(object):
    """ Topic Media Provider
    """
    implements(IMediaProvider)

    def __init__(self, context):
        self.context = context
        # this can be changed by someone who wants a specific media type
        self.media_type = None

    @property
    def media_items(self):
        """ Media items
        """
        portal_catalog = getToolByName(self.context, 'portal_catalog')
        query = self.context.buildQuery()
        if self.media_type:
            query['media_types'] = self.media_type
        brains = portal_catalog.searchResults(query)
        return brains

class ExtensionManagementPlanfield(ExtensionField, ManagementPlanField):
    """ Derivative of blobfield for extending schemas
    """

class SchemaExtender(object):
    """ Schema Extender
    """
    implements(ISchemaExtender)

    fields = [
        ExtensionManagementPlanfield(
            name='eeaManagementPlan',
            languageIndependent=True,
            required=True,
            default=(datetime.now().year, ''),
            validators = ('management_plan_code_validator',),

            vocabulary_factory="Temporal coverage",
            storage = AnnotationStorage(migrate=True),
            widget = ManagementPlanWidget(
                format="select",
                label="EEA Management Plan",
                description = ("EEA Management plan code."),
                label_msgid='dataservice_label_eea_mp',
                description_msgid='dataservice_help_eea_mp',
                i18n_domain='eea.dataservice',
                )
            )
    ]

    def __init__(self, context):
        self.context = context

    def getFields(self):
        """ Get fields
        """
        return self.fields
