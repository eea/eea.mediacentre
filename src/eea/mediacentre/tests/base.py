""" Media centre test case
"""
from Products.PloneTestCase import PloneTestCase
from Products.PloneTestCase.layer import onsetup
from Products.Five import fiveconfigure
from Zope2.App import zcml
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
    PloneTestCase.installPackage('eea.themcentre')

setup_mediacentre()
PloneTestCase.setupPloneSite(extension_profiles=(
    'eea.themecentre:default', 'eea.mediacentre:default'))

class MediaCentrePloneTestCase(PloneTestCase.PloneTestCase):
    """Base class for integration tests for the 'eea.mediacentre' product.
    """

class MediaCentreTestCase(MediaCentrePloneTestCase,
                                            PloneTestCase.FunctionalTestCase):
    """ A test case for mediacentres.
    """
