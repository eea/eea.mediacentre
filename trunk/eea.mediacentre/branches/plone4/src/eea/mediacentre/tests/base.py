""" Media centre test case
"""
from Products.PloneTestCase import PloneTestCase
from Products.PloneTestCase.layer import onsetup
from Products.Five import zcml
from Products.Five import fiveconfigure
import eea.mediacentre

PloneTestCase.installProduct('ATVocabularyManager')
PloneTestCase.installProduct('LinguaPlone')
#TODO: fix me, plone4
#PloneTestCase.installProduct('EEAContentTypes')
PloneTestCase.installProduct('EEAPloneAdmin')

@onsetup
def setup_mediacentre():
    """ Setup media centre
    """
    fiveconfigure.debug_mode = True
    zcml.load_config('configure.zcml', eea.mediacentre)
    fiveconfigure.debug_mode = False

    PloneTestCase.installPackage('valentine.linguaflow')
    PloneTestCase.installPackage('p4a.z2utils')
    PloneTestCase.installPackage('p4a.fileimage')
    PloneTestCase.installPackage('p4a.video')
    PloneTestCase.installPackage('p4a.plonevideo')
    PloneTestCase.installPackage('p4a.subtyper')

setup_mediacentre()
PloneTestCase.setupPloneSite(extension_profiles=('eea.mediacentre:default',))

class MediaCentreTestCase(PloneTestCase.FunctionalTestCase):
    """ A test case for mediacentres. """
