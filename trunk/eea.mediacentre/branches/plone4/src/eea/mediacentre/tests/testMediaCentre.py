""" Test media centre
"""
import unittest
import os
from Acquisition import aq_base
from p4a.subtyper.engine import Subtyper
from p4a.video.interfaces import IVideo
from p4a.video.media import MediaActivator
from p4a.video.subtype import VideoDescriptor
from eea.mediacentre.mediacentre import MediaCentre
from eea.mediacentre.mediatypes import MediaTypesAdapter
from eea.mediacentre.interfaces import IMediaProvider, IMediaType
from eea.mediacentre.subtyper import subtype_added, subtype_removed
from eea.mediacentre.tests.base import MediaCentreTestCase
from zope.annotation.attribute import AttributeAnnotations
from zope.component import provideUtility, provideAdapter, provideHandler
from zope.component import queryAdapter
from zope.testing import doctest
from Testing.ZopeTestCase import FunctionalDocFileSuite

optionflags =  (doctest.ELLIPSIS |
                doctest.NORMALIZE_WHITESPACE |
                doctest.REPORT_ONLY_FIRST_FAILURE)

def setUp(test):
    """ Setup
    """
    provideUtility(MediaCentre())

def setUp2(test):
    """ Setup 2
    """
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
        self.portal.portal_membership.addMember('manager', 'secret', ['Manager'], [])
        self.login('manager')
        #TODO: fix me, plone4
        #self.portal.portal_workflow.doActionFor(barsandtones, 'publish')

        self.portal.invokeFactory('File', id='interview')
        config = self.portal.interview.restrictedTraverse('@@video-config.html')
        config.media_activated = True
        interview = aq_base(self.portal.interview)
        IMediaType(interview).types = ['interview']
        #TODO: fix me, plone4
        #self.portal.portal_workflow.doActionFor(self.portal.interview, 'publish')

        self.portal.invokeFactory('Topic', id='topic')
        crit = self.portal.topic.addCriterion('review_state', 'ATSimpleStringCriterion')
        crit.setValue('published')

    #TODO: fix me, plone4
    #def testTopicMediaProvider(self):
        #""" Test Topic Media Provider
        #"""
        #self.portal.interview.reindexObject()   #fixes test
        #provider = IMediaProvider(self.portal.topic)
        ## we should now get all the published files
        #self.assertEquals(len(provider.media_items), 2)
        #provider.media_type = 'interview'
        ## now we should only get the interview file
        #self.assertEquals(len(provider.media_items), 1)

    #TODO: fix me, plone4
    #def testVideoFlashAdapter(self):
        #""" Test that a FlashFile can not be adapted to IVideo before it's
            #marked with the IVideoEnhanced interface. This follows the p4a.video
            #convention on IVideo adapters.
        #"""

        #self.portal.invokeFactory('FlashFile', id='flashy')

        ##NOTE: FlashFile now directly provides IVideoEnhanced, disabling test
        ##self.assertTrue(queryAdapter(self.portal.flashy, IVideo) is None)
        ##config = self.portal.flashy.restrictedTraverse('@@video-config.html')
        ##config.media_activated = True

        #self.assertTrue(queryAdapter(self.portal.flashy, IVideo) is not None)

def test_suite():
    """ Test suite
    """
    return unittest.TestSuite((
        unittest.makeSuite(TestMediaCentre),

        #TODO: fix me, plone4
        #doctest.DocFileSuite('../README.txt',
                     #setUp=setUp,
                     #optionflags=optionflags,),
        doctest.DocFileSuite('mediatypes.txt',
                     setUp=setUp2,
                     optionflags=optionflags,),
        #TODO: fix me, plone4
        #FunctionalDocFileSuite('video.txt',
                     #test_class = TestMediaCentre,
                     #optionflags=optionflags,
                     #package = 'eea.mediacentre.tests'),
    ))
