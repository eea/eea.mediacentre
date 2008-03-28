from zope.testing import doctest
import unittest
import os
from p4a.video.media import MediaActivator
from p4a.subtyper.engine import Subtyper
from p4a.video.subtype import VideoDescriptor
from eea.mediacentre.mediacentre import MediaCentre
from eea.mediacentre.mediatypes import MediaTypesAdapter
from eea.mediacentre.subtyper import subtype_added, subtype_removed
from eea.mediacentre.tests.MediaCentreTestCase import MediaCentreTestCase
from zope.app.annotation.attribute import AttributeAnnotations
from zope.component import provideUtility, provideAdapter, provideHandler

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
        self.setRoles(['Manager'])
        self.portal.invokeFactory('File', id='barsandtones')
        self.portal.invokeFactory('Document', id='barsandtones2')
        self.portal.barsandtones2.setText('Cow')
        barsandtones = self.portal.barsandtones
        path = os.path.join(os.path.dirname(__file__), 'barsandtones.flv')
        file = open(path, 'r')
        barsandtones.setFile(file)
        file.close()
        f = barsandtones.getPrimaryField().getAccessor(barsandtones)()
        f.setContentType('video/x-flv')
        config = barsandtones.restrictedTraverse('@@video-config.html')
        config.media_activated = True
        barsandtones.reindexObject()
        self.portal.portal_membership.addMember('manager', 'secret', ['Manager'], [])
        self.login('manager')
        self.portal.portal_workflow.doActionFor(barsandtones, 'publish')

def test_suite():
    from Testing.ZopeTestCase import FunctionalDocFileSuite

    return unittest.TestSuite((
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
