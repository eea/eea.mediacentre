""" Media centre test case
"""
from Products.PloneTestCase import PloneTestCase
from Products.PloneTestCase.layer import onsetup
from Products.Five import zcml
from Products.Five import fiveconfigure
import Products.Five
import eea.mediacentre
import p4a.fileimage
import p4a.video
import p4a.plonevideo
import p4a.subtyper
import valentine.linguaflow

PRODUCTS = ('ATVocabularyManager', 'LinguaPlone',
            'EEAContentTypes', 'valentine.linguaflow', 'EEAPloneAdmin')

@onsetup
def setup_mediacentre():
    fiveconfigure.debug_mode = True
    zcml.load_config('meta.zcml', Products.Five)
    zcml.load_config('configure.zcml', p4a.z2utils)
    zcml.load_config('configure.zcml', p4a.fileimage)
    zcml.load_config('configure.zcml', p4a.video)
    zcml.load_config('configure.zcml', p4a.plonevideo)
    zcml.load_config('meta.zcml', p4a.subtyper)
    zcml.load_config('configure.zcml', p4a.subtyper)
    zcml.load_config('configure.zcml', eea.mediacentre)
    zcml.load_config('configure.zcml', valentine.linguaflow)
    fiveconfigure.debug_mode = False

    PloneTestCase.installProduct('Five')
    PloneTestCase.installProduct('ATVocabularyManager')
    PloneTestCase.installProduct('LinguaPlone')
    PloneTestCase.installProduct('EEAContentTypes')
    PloneTestCase.installProduct('valentine.linguaflow')
    PloneTestCase.installProduct('EEAPloneAdmin')

setup_mediacentre()
PloneTestCase.setupPloneSite(products=PRODUCTS)

class MediaCentreTestCase(PloneTestCase.FunctionalTestCase):
    """ A test case for mediacentres. """
