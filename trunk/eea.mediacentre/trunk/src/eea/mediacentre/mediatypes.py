from Products.ATContentTypes.content.image import ATImage
from Products.CMFCore.utils import getToolByName
from eea.mediacentre.interfaces import IMediaType
from p4a.video.interfaces import IVideoEnhanced
from persistent.dict import PersistentDict
from persistent.list import PersistentList
from zope.app.annotation.interfaces import IAnnotations
from zope.app.schema.vocabulary import IVocabularyFactory
from zope.component import adapts
from zope.interface import implements #, alsoProvides, directlyProvidedBy
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary

#from zope.interface import directlyProvides

KEY = 'eea.mediacentre.mediafile'


class MediaTypesAdapter(object):
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

    #def types():
    def gett(self):
        anno = IAnnotations(self.context)
        mapping = anno.get(KEY)
        return mapping['types']
    def sett(self, values):
        anno = IAnnotations(self.context)
        mapping = anno.get(KEY)
        mapping['types'] = PersistentList(values)

        self.context.reindexObject()
    #return property(get, set)
    types = property(gett, sett)


class MediaTypesImageAdapter(object):
    implements(IMediaType)
    adapts(ATImage)

    def __init__(self, context):
        self.context = context

    #def types():
    def gett(self):
        return ['image']
    def sett(self):
        pass
    #return property(get, set)
    types = property(gett, sett)


class MediaTypesVocabulary(object):
    implements(IVocabularyFactory)

    def __call__(self, context):
        obj = getattr(context, 'context', context)
        portal_vocab = getToolByName(obj, 'portal_vocabularies')
        types = getattr(portal_vocab, 'multimedia').getDisplayList(obj)
        terms = [SimpleTerm(key, key, value) for key, value in types.items()]
        return SimpleVocabulary(terms)

MediaTypesVocabularyFactory = MediaTypesVocabulary()
