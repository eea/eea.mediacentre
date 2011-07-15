""" Media types
"""
from Products.ATContentTypes.content.image import ATImage
from Products.ATContentTypes.interfaces import IATImage

from Products.CMFCore.utils import getToolByName
from eea.mediacentre.interfaces import IMediaType
from p4a.video.interfaces import IVideoEnhanced
from persistent.dict import PersistentDict
from persistent.list import PersistentList
from zope.annotation.interfaces import IAnnotations
from zope.app.schema.vocabulary import IVocabularyFactory
from zope.component import adapts
from zope.interface import implements
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary
import logging

KEY = 'eea.mediacentre.mediafile'
logger = logging.getLogger('eea.mediacentre.mediatypes')

class MediaTypesAdapter(object):
    """ Media Types Adapter
    """
    implements(IMediaType)
    adapts(IVideoEnhanced)

    def __init__(self, context):
        self.context = context
        annotations = IAnnotations(context)
        mapping = annotations.get(KEY)
        if mapping is None:
            mediafile =  { 'types': [] }
            mapping = annotations[KEY] = PersistentDict(mediafile)
        self.mapping = mapping

    def gett(self):
        """ Get types
        """
        anno = IAnnotations(self.context)
        mapping = anno.get(KEY)
        return mapping['types']

    def sett(self, values):
        """ Set types
        """
        anno = IAnnotations(self.context)
        mapping = anno.get(KEY)
        mapping['types'] = PersistentList(values)

        try:
            self.context.reindexObject()
        except AttributeError:
            logger.info('Reindex skipped')

    types = property(gett, sett)

class MediaTypesImageAdapter(object):
    """ Media Types Image Adapter
    """
    implements(IMediaType)
    adapts(IATImage)

    def __init__(self, context):
        self.context = context

    def gett(self):
        """ Get types
        """
        return ['image']

    def sett(self):
        """ Set types
        """
        pass

    types = property(gett, sett)

class MediaTypesVocabulary(object):
    """ Media Types Vocabulary
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        obj = getattr(context, 'context', context)
        portal_vocab = getToolByName(obj, 'portal_vocabularies')
        types = getattr(portal_vocab, 'multimedia').getDisplayList(obj)
        terms = [SimpleTerm(key, key, value) for key, value in types.items()]
        return SimpleVocabulary(terms)

MediaTypesVocabularyFactory = MediaTypesVocabulary()
