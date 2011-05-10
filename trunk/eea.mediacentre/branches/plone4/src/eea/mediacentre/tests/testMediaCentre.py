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
from eea.mediacentre.tests.MediaCentreTestCase import MediaCentreTestCase
from zope.annotation.attribute import AttributeAnnotations
from zope.component import provideUtility, provideAdapter, provideHandler
from zope.component import queryAdapter
from zope.testing import doctest

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

class TestMediaCentre(MediaCentreTestCase):

    def afterSetUp(self):
        #self.portal.portal_catalog.addIndex("media_types", "KeywordIndex")
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
        self.portal.portal_workflow.doActionFor(barsandtones, 'publish')

        self.portal.invokeFactory('File', id='interview')
        config = self.portal.interview.restrictedTraverse('@@video-config.html')
        config.media_activated = True
        interview = aq_base(self.portal.interview)
        IMediaType(interview).types = ['interview']
        self.portal.portal_workflow.doActionFor(self.portal.interview, 'publish')

        self.portal.invokeFactory('Topic', id='topic')
        crit = self.portal.topic.addCriterion('review_state', 'ATSimpleStringCriterion')
        crit.setValue('published')

    def testTopicMediaProvider(self):
        self.portal.interview.reindexObject()   #fixes test
        provider = IMediaProvider(self.portal.topic)
        # we should now get all the published files
        self.assertEquals(len(provider.media_items), 2)
        provider.media_type = 'interview'
        # now we should only get the interview file
        self.assertEquals(len(provider.media_items), 1)

    def testVideoFlashAdapter(self):
        """ test that a FlashFile can not be adapted to IVideo before it's
            marked with the IVideoEnhanced interface. This follows the p4a.video
            convention on IVideo adapters. """

        self.portal.invokeFactory('FlashFile', id='flashy')

        #NOTE: FlashFile now directly provides IVideoEnhanced, disabling test
        #self.assertTrue(queryAdapter(self.portal.flashy, IVideo) is None)
        #config = self.portal.flashy.restrictedTraverse('@@video-config.html')
        #config.media_activated = True

        self.assertTrue(queryAdapter(self.portal.flashy, IVideo) is not None)

def test_suite():
    from Testing.ZopeTestCase import FunctionalDocFileSuite

    return unittest.TestSuite((
        unittest.makeSuite(TestMediaCentre),
        doctest.DocFileSuite('../README.txt',
                     setUp=setUp, #tearDown=tearDown,
                     optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS,
                     ),
        doctest.DocFileSuite('mediatypes.txt',
                     setUp=setUp2, #tearDown=tearDown,
                     optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS,
                     ),
        FunctionalDocFileSuite('video.txt',
                     test_class = TestMediaCentre,
                     optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE,
                     package = 'eea.mediacentre.tests'),
        ))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
