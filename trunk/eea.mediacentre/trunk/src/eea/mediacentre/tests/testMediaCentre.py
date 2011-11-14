""" Test media centre
"""
import doctest
import unittest
import os
from Acquisition import aq_base
from p4a.subtyper.engine import Subtyper
from p4a.video.media import MediaActivator
from p4a.video.subtype import VideoDescriptor
from eea.mediacentre.mediacentre import MediaCentre
from eea.mediacentre.mediatypes import MediaTypesAdapter
from eea.mediacentre.interfaces import (
    IMediaProvider,
    IMediaType,
)
from eea.mediacentre.subtyper import subtype_added, subtype_removed
from eea.mediacentre.tests.base import MediaCentreTestCase
from zope.annotation.attribute import AttributeAnnotations
from zope.component import provideUtility, provideAdapter, provideHandler
from zope.component.testing import setUp
from Testing.ZopeTestCase import FunctionalDocFileSuite
# NOTE: this is needed because when testing you get some parser
# warnings which make the jenkins builds fail
import hachoir_core.config
hachoir_core.config.quiet = True

optionflags =  (doctest.ELLIPSIS |
        doctest.NORMALIZE_WHITESPACE | 
        doctest.REPORT_ONLY_FIRST_FAILURE)

def configurationSetUp(test):
    """ Setup
    """
    setUp()
    provideUtility(MediaCentre())

def configurationSetUp2(test):
    """ Setup 2
    """
    setUp()
    provideAdapter(AttributeAnnotations)
    provideAdapter(MediaTypesAdapter)
    provideAdapter(MediaActivator)
    provideUtility(Subtyper())
    provideUtility(VideoDescriptor(), name="p4a.video.Video")
    provideHandler(subtype_added)
    provideHandler(subtype_removed)

class TestMediaCentre(MediaCentreTestCase):
    """ Test Media Centre
    """
    def afterSetUp(self):
        """ After setup
        """
        self.setRoles(['Manager'])

        self.portal.invokeFactory('File', id='barsandtones')
        self.portal.invokeFactory('Document', id='barsandtones2')
        self.portal.barsandtones2.setText('Cow')
        barsandtones = self.portal.barsandtones
        path = os.path.join(os.path.dirname(__file__), 'barsandtones.flv')
        afile = open(path, 'r')
        barsandtones.setFile(afile)
        afile.close()
        f = barsandtones.getPrimaryField().getAccessor(barsandtones)()
        f.setContentType('video/x-flv')
        config = barsandtones.restrictedTraverse('@@video-config.html')
        config.media_activated = True
        barsandtones.reindexObject()
        self.portal.portal_membership.addMember('manager',
                                                'secret',
                                                ['Manager'],
                                                [])
        self.login('manager')

        self.portal.invokeFactory('File', id='interview')
        config = self.portal.interview.restrictedTraverse('@@video-config.html')
        config.media_activated = True
        interview = aq_base(self.portal.interview)
        IMediaType(interview).types = ['interview']
        
        # NOTE: Plone 4.x doesn't have a workflow for files and images 
        # so we don't search by published state, 
        self.portal.invokeFactory('Topic', id='topic')
        crit = self.portal.topic.addCriterion('Type', 'ATPortalTypeCriterion')
        crit.setValue('File')
        


    def testTopicMediaProvider(self):
        """ Test Topic Media Provider
        """
        self.portal.interview.reindexObject()   #fixes test
        provider = IMediaProvider(self.portal.topic)
        # we should now get all the files we created
        self.assertEquals(len(provider.media_items), 2)
        provider.media_type = 'interview'
        # now we should only get the interview file
        self.assertEquals(len(provider.media_items), 1)


def test_suite():
    """ Test suite
    """
    return unittest.TestSuite((
        unittest.makeSuite(TestMediaCentre),

        doctest.DocFileSuite('README.txt',
                    package='eea.mediacentre',
                    setUp=configurationSetUp,
                    optionflags=optionflags,),
        doctest.DocFileSuite('tests/mediatypes.txt',
                    package='eea.mediacentre',
                    setUp=configurationSetUp2,
                    optionflags=optionflags,),
        FunctionalDocFileSuite('tests/video.txt',
                    package='eea.mediacentre',
                    test_class=TestMediaCentre,
                    optionflags=optionflags,
                    ),
    ))
