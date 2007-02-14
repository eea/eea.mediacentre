from zope.testing import doctest
import unittest
from eea.mediacentre.mediacentre import MediaCentre
from zope.component import provideUtility

def setUp(test):
    provideUtility(MediaCentre())

def test_suite():

    return unittest.TestSuite((
        doctest.DocFileSuite('../README.txt',
                     setUp=setUp, #tearDown=tearDown,
                     optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS,
                     ),
        ))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
