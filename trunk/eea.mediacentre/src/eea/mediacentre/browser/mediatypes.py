from zope.formlib.form import Fields, EditForm
from eea.mediacentre.interfaces import IMediaType

class MediaTypesEditForm(EditForm):
    """ Form for changing discover method. """

    form_fields = Fields(IMediaType)
    label = u'Edit media type'
