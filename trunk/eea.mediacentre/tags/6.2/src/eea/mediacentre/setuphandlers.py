""" Various setup
"""
from Products.CMFCore.utils import getToolByName
from Products.ATVocabularyManager.utils.vocabs import createSimpleVocabs

VOCABULARIES = {
  'multimedia': (
    ('animation', 'Animation'),
    ('image' , 'Image'),
    ('interactivemap', 'Interactive Map'),
    ('interview', 'Interview'),
    ('mindstretcher', 'Mind Stretcher'),
    ('other', 'Other'),
    ('presentation', 'Presentation'),
    ('video', 'Video'),
    )
}

def installVocabularies(context):
    """creates/imports the atvm vocabs."""
    if context.readDataFile('eea.mediacentre.txt') is None:
        return

    site = context.getSite()
    atvm = getToolByName(site, 'portal_vocabularies')
    createSimpleVocabs(atvm, VOCABULARIES)
