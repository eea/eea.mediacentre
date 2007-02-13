from zope.testing import doctest
from zope.testing.doctestunit import DocFileSuite, DocTestSuite
from Testing.ZopeTestCase.zopedoctest import ZopeDocFileSuite
import unittest
from eea.mediacentre.mediacentre import MediaCentre
from zope.component import provideUtility

def setUp(test):
    provideUtility(MediaCentre())

def test_suite():

    return unittest.TestSuite((
        DocFileSuite('../README.txt',
                     setUp=setUp, #tearDown=tearDown,
                     optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS,
                     ),
        ))

if __name__ == '__main__':
    print "PROAEAKJSLFKAFJ"
    unittest.main(defaultTest='test_suite')
