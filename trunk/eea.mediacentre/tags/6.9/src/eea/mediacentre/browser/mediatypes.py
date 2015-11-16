""" Media types
"""
from zope.schema.interfaces import IVocabularyFactory
from zope.component import getUtility
from zope.formlib.form import Fields
from five.formlib.formbase import EditForm
from eea.mediacentre.interfaces import IMediaType

class MediaTypesEditForm(EditForm):
    """ Form for changing discover method.
    """

    form_fields = Fields(IMediaType)
    label = u'Edit media type'

class MediaTypes(object):
    """ Convenient info for templates.
    """

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def title(self, name):
        """ Title
        """
        vocab = getUtility(IVocabularyFactory, name="Media types")(self.context)
        return vocab.getTerm(name).title
