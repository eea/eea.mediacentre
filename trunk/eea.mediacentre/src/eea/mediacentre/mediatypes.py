from zope.app.annotation.interfaces import IAnnotations
from zope.app.schema.vocabulary import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary
from zope.component import adapts
from zope.interface import implements, alsoProvides, directlyProvidedBy
from zope.interface import directlyProvides
from persistent.dict import PersistentDict
from persistent.list import PersistentList

from eea.mediacentre.interfaces import IInterview, IMap, IVideo, IMindStretcher
from eea.mediacentre.interfaces import IMediaType, IPossibleMediaFile

KEY = 'eea.mediacentre.mediafile'

MEDIA_TYPES = {
    'interview': { 'title': 'Interview', 'interface': IInterview },
    'map': { 'title': 'Map', 'interface': IMap },
    'video': { 'title': 'Video', 'interface': IVideo },
    'stretcher': { 'title': 'Mind Stretcher', 'interface': IMindStretcher },
    }

class MediaTypesAdapter(object):
    implements(IMediaType)
    adapts(IPossibleMediaFile)

    def __init__(self, context):
        self.context = context
        annotations = IAnnotations(context)
        mapping = annotations.get(KEY)
        if mapping is None:
            mediafile =  { 'type': None }
            mapping = annotations[KEY] = PersistentDict(mediafile)
        self.mapping = mapping

    def media_type():
        def get(self):
            anno = IAnnotations(self.context)
            mapping = anno.get(KEY)
            return mapping['type']
        def set(self, value):
            anno = IAnnotations(self.context)
            mapping = anno.get(KEY)
            old_value = mapping['type']
            mapping['type'] = value

            ifaces = directlyProvidedBy(self.context)
            if old_value:
                old_iface = MEDIA_TYPES[old_value]['interface']
                ifaces = ifaces - old_iface

            if value:
                new_iface = MEDIA_TYPES[value]['interface']
                ifaces = ifaces + new_iface

            directlyProvides(self.context, ifaces)
            self.context.reindexObject()
        return property(get, set)
    media_type = media_type()


class MediaTypesVocabulary(object):
    implements(IVocabularyFactory)

    def __call__(self, context):
        terms = []
        for media_id, media_type in MEDIA_TYPES.items():
            term = SimpleTerm(media_id, media_id, media_type['title'])
            terms.append(term)
        return SimpleVocabulary(terms)

MediaTypesVocabularyFactory = MediaTypesVocabulary()
