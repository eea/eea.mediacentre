""" Test media centre
"""
import doctest
import unittest
import os
from zope.interface import alsoProvides
from eea.mediacentre.mediacentre import MediaCentre
from eea.mediacentre.interfaces import IVideo
from eea.mediacentre.tests.base import MediaCentreTestCase
from zope.component import provideUtility
from zope.component.testing import setUp
from Testing.ZopeTestCase import FunctionalDocFileSuite

optionflags = (doctest.ELLIPSIS |
               doctest.NORMALIZE_WHITESPACE |
               doctest.REPORT_ONLY_FIRST_FAILURE)


def configurationSetUp(test):
    """ Setup
    """
    setUp()
    provideUtility(MediaCentre())


class TestMediaCentre(MediaCentreTestCase):
    """ Test Media Centre
    """

    def afterSetUp(self):
        """ After setup
        """
        self.setRoles(['Manager'])

        self.portal.invokeFactory('File', id='barsandtones')
        barsandtones = self.portal.barsandtones
        path = os.path.join(os.path.dirname(__file__), 'barsandtones.flv')
        afile = open(path, 'r')
        barsandtones.setFile(afile)
        afile.close()
        f = barsandtones.getPrimaryField().getAccessor(barsandtones)()
        f.setContentType('video/x-flv')
        alsoProvides(barsandtones, IVideo)
        barsandtones.reindexObject()
        self.portal.portal_membership.addMember('manager',
                                                'secret',
                                                ['Manager'],
            [])
        self.login('manager')


def test_suite():
    """ Test suite
    """
    return unittest.TestSuite((
        unittest.makeSuite(TestMediaCentre),

        doctest.DocFileSuite('README.txt',
                             package='eea.mediacentre',
                             setUp=configurationSetUp,
                             optionflags=optionflags, ),
        FunctionalDocFileSuite('tests/video.txt',
                               package='eea.mediacentre',
                               test_class=TestMediaCentre,
                               optionflags=optionflags,
        ),
    ))
