""" Media centre test case
"""
from Products.PloneTestCase import PloneTestCase
from Products.PloneTestCase.layer import onsetup
from Zope2.App import zcml
from Products.Five import fiveconfigure
import eea.mediacentre

PloneTestCase.installProduct('ATVocabularyManager')
PloneTestCase.installProduct('LinguaPlone')
PloneTestCase.installProduct('EEAContentTypes')
PloneTestCase.installProduct('EEAPloneAdmin')
PloneTestCase.installProduct('eea.themcentre')

@onsetup
def setup_mediacentre():
    """ Setup media centre
    """
    fiveconfigure.debug_mode = True
    zcml.load_config('configure.zcml', eea.mediacentre)
    fiveconfigure.debug_mode = False

    PloneTestCase.installPackage('valentine.linguaflow')
    PloneTestCase.installPackage('ATVocabularyManager')
    PloneTestCase.installPackage('p4a.z2utils')
    PloneTestCase.installPackage('p4a.fileimage')
    PloneTestCase.installPackage('p4a.video')
    PloneTestCase.installPackage('eea.themcentre')
    PloneTestCase.installPackage('p4a.plonevideo')
    PloneTestCase.installPackage('p4a.subtyper')

setup_mediacentre()
PloneTestCase.setupPloneSite(extension_profiles=(
    'eea.themecentre:default','eea.mediacentre:default'))

class MediaCentreTestCase(PloneTestCase.FunctionalTestCase):
    """ A test case for mediacentres.
    """
