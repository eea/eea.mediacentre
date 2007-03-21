from zope.testing import doctest
import unittest
from eea.mediacentre.mediacentre import MediaCentre
from eea.mediacentre.interfaces import IPossibleMediaFile
from eea.mediacentre.mediatypes import MediaTypesAdapter
from zope.app.annotation.attribute import AttributeAnnotations
from zope.app.folder.folder import Folder
from zope.component import provideUtility, provideAdapter
from zope.interface import classImplements

def setUp(test):
    provideUtility(MediaCentre())

def setUp2(test):
    classImplements(Folder, IPossibleMediaFile)
    provideAdapter(AttributeAnnotations)
    provideAdapter(MediaTypesAdapter)

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
