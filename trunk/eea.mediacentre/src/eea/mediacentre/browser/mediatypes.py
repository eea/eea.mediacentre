from zope.formlib.form import Fields
from Products.Five.formlib.formbase import EditForm
from eea.mediacentre.interfaces import IMediaType

class MediaTypesEditForm(EditForm):
    """ Form for changing discover method. """

    form_fields = Fields(IMediaType)
    label = u'Edit media type'
