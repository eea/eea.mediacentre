""" Media
"""
from archetypes.schemaextender.field import ExtensionField
from archetypes.schemaextender.interfaces import ISchemaExtender
from datetime import datetime
from eea.forms.fields.ManagementPlanField import ManagementPlanField
from eea.forms.widgets.ManagementPlanWidget import ManagementPlanWidget
from plone.app.blob.field import ImageField
from Products.Archetypes.atapi import AnnotationStorage
from Products.Archetypes.atapi import RichWidget, ImageWidget
from Products.Archetypes.atapi import TextAreaWidget
from Products.Archetypes.atapi import TextField
from Products.EEAContentTypes.content.interfaces import ICloudVideo
from zope.interface import implements
from eea.mediacentre.interfaces import IMediaCentre, IMediaProvider
from eea.mediacentre.mediacentre import MEDIA_SEARCH_KEY
from eea.themecentre.themecentre import getTheme
from zope.component import getUtility


class ExtensionManagementPlanfield(ExtensionField, ManagementPlanField):
    """ Derivative of blobfield for extending schemas
    """


class ExtensionVideoCloudUrlfield(ExtensionField, TextField):
    """ TextField wrapped in ExtensionField for extending schemas
    """


class ExtensionVideoRichField(ExtensionField, TextField):
    """ TextField wrapped in ExtensionField for extending schemas
    """


class ExtensionVideoImageField(ExtensionField, ImageField):
    """ ImageField wrapped in ExtensionField for extending schemas
    """


class SchemaExtender(object):
    """ Schema Extender
    """
    implements(ISchemaExtender)

    fields = [
        ExtensionVideoImageField(
            name='image',
            required=False,
            storage=AnnotationStorage(migrate=True),
            languageIndependent=True,
            widget=ImageWidget(
                label='Image',
                label_msgid='EEAContentTypes_label_image',
                description_msgid='EEAContentTypes_help_image',
                i18n_domain='eea',
                show_content_type=False
            )
        ),

        ExtensionManagementPlanfield(
            name='eeaManagementPlan',
            languageIndependent=True,
            required=True,
            default=(datetime.now().year, ''),
            validators=('management_plan_code_validator',),

            vocabulary_factory="Temporal coverage",
            storage=AnnotationStorage(migrate=True),
            widget=ManagementPlanWidget(
                format="select",
                label="EEA Management Plan",
                description="EEA Management plan code.",
                label_msgid='dataservice_label_eea_mp',
                description_msgid='dataservice_help_eea_mp',
                i18n_domain='eea.dataservice',
            )
        ),

        ExtensionVideoCloudUrlfield(
            name='cloudUrl',
            languageIndependent=True,
            required=False,
            schemata='default',
            storage=AnnotationStorage(migrate=True),
            default_content_type='text/plain',
            validators=('videoCloudUrlValidator',),
            allowable_content_types=('text/plain',),
            default_output_type='text/plain',
            widget=TextAreaWidget(
                description='The embedding code for the video from'
                            ' external sites eg. Vimeo or Youtube',
                label="Cloud Url"
            )
        ),

        ExtensionVideoRichField(
            name='text',
            languageIndependent=True,
            required=False,
            schemata='default',
            widget=RichWidget(
                label="Rich Text Description",
                label_msgid="EEAContentTypes_label_rich_description",
                i18n_domain="eea",
                rows=10,
            )
        )
    ]

    def __init__(self, context):
        self.context = context

    def getFields(self):
        """ Get fields
        """
        # CloudUrl already has these fields
        if ICloudVideo.providedBy(self.context):
            return []
        else:
            # cloudUrl isn't required for File with IVideo interface
            self.fields[1].required = False
        return self.fields

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
        search = {MEDIA_SEARCH_KEY: {'theme': currentTheme}}
        files = mediacentre.getMedia(self.media_type, full_objects=False,
                                     search=search)

        videos = []
        for media_dict in files:
            videos.append(media_dict['object'])

        return videos
