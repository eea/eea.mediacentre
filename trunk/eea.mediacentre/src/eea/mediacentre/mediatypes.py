from zope.app.annotation.interfaces import IAnnotations
from zope.app.schema.vocabulary import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary
from zope.component import adapts
from zope.interface import implements, alsoProvides, directlyProvidedBy
from zope.interface import directlyProvides
from persistent.dict import PersistentDict
from persistent.list import PersistentList

from eea.mediacentre.interfaces import IMediaType, IPossibleMediaFile

KEY = 'eea.mediacentre.mediafile'

class MediaTypesAdapter(object):
    implements(IMediaType)
    adapts(IPossibleMediaFile)

    def __init__(self, context):
        self.context = context
        annotations = IAnnotations(context)
        mapping = annotations.get(KEY)
        if mapping is None:
            mediafile =  { 'types': None }
            mapping = annotations[KEY] = PersistentDict(mediafile)
        self.mapping = mapping

    def types():
        def get(self):
            anno = IAnnotations(self.context)
            mapping = anno.get(KEY)
            return mapping['types']
        def set(self, values):
            anno = IAnnotations(self.context)
            mapping = anno.get(KEY)
            mapping['types'] = PersistentList(values)

            self.context.reindexObject()
        return property(get, set)
    types = types()


class MediaTypesVocabulary(object):
    implements(IVocabularyFactory)

    def __call__(self, context):
        portal_vocab = getToolByName(context.context, 'portal_vocabularies')
        types = getattr(portal_vocab, 'multimedia').getDisplayList(context.context)
        terms = [SimpleTerm(key, key, value) for key, value in types.items()]
        return SimpleVocabulary(terms)


MediaTypesVocabularyFactory = MediaTypesVocabulary()
