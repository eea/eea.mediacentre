""" EEA Media Centre installer
"""
from setuptools import setup, find_packages
import os

NAME = 'eea.mediacentre'
PATH = NAME.split('.') + ['version.txt']
VERSION = open(os.path.join("src/", *PATH)).read().strip()


setup(name=NAME,
      version=VERSION,
      url='http://svn.eionet.europa.eu/projects/'
          'Zope/browser/trunk/eea.mediacentre',
      description='EEA Media Centre',
      author='Tim Terlegard, Antonio De Marinis (EEA), '
             'European Environment Agency (EEA)',
      author_email='webadmin@eea.europa.eu',
      license='GPL',
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      classifiers=[
          "Framework :: Plone",
          "Programming Language :: Python",
          "Topic :: Software Development :: Libraries :: Python Modules",
          ],
      keywords='eea media centre',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages = ['eea'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          "setuptools",
          'eea.vocab',
          "eea.themecentre",
          "p4a.video",
          # "p4a.plonevideo",
          "Products.fatsyndication",
          "Products.basesyndication",
          #"p4a.common",
          "p4a.subtyper",
          "eea.geotags",
          "Products.EEAContentTypes",
          "eea.dataservice",
          "Products.LinguaPlone",
          "valentine.linguaflow",
          "Products.ATVocabularyManager",
          "Products.EEAPloneAdmin",
          "eea.forms"
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
