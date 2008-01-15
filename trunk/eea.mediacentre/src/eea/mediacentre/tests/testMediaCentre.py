from zope.testing import doctest
import unittest
from p4a.video.media import MediaActivator
from p4a.subtyper.engine import Subtyper
from p4a.video.subtype import VideoDescriptor
from eea.mediacentre.mediacentre import MediaCentre
from eea.mediacentre.mediatypes import MediaTypesAdapter
from eea.mediacentre.subtyper import subtype_added, subtype_removed
from zope.app.annotation.attribute import AttributeAnnotations
from zope.app.folder.folder import Folder
from zope.component import provideUtility, provideAdapter, provideHandler
from zope.interface import classImplements

def setUp(test):
    provideUtility(MediaCentre())

def setUp2(test):
    provideAdapter(AttributeAnnotations)
    provideAdapter(MediaTypesAdapter)
    provideAdapter(MediaActivator)
    provideUtility(Subtyper())
    provideUtility(VideoDescriptor(), name="p4a.video.Video")
    provideHandler(subtype_added)
    provideHandler(subtype_removed)

def test_suite():

    return unittest.TestSuite((
        doctest.DocFileSuite('../README.txt',
                     setUp=setUp, #tearDown=tearDown,
                     optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS,
                     ),
        doctest.DocFileSuite('mediatypes.txt',
                     setUp=setUp2, #tearDown=tearDown,
                     optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS,
                     ),
        ))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
