""" EEA Media Centre installer
"""
import os
from setuptools import setup, find_packages

NAME = 'eea.mediacentre'
PATH = NAME.split('.') + ['version.txt']
VERSION = open(os.path.join("src/", *PATH)).read().strip()


setup(name=NAME,
      version=VERSION,
      url='https://github.com/eea/eea.mediacentre',
      description='EEA Media Centre',
      author='European Environment Agency: IDM2 A-Team',
      author_email='eea-edw-a-team-alerts@googlegroups.com',
      license='GPL',
      long_description=open("README.rst").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # https://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
          "Framework :: Zope2",
          "Framework :: Plone",
          "Framework :: Plone :: 4.0",
          "Framework :: Plone :: 4.1",
          "Framework :: Plone :: 4.2",
          "Framework :: Plone :: 4.3",
          "Programming Language :: Zope",
          "Programming Language :: Python",
          "Programming Language :: Python :: 2.7",
          "Topic :: Software Development :: Libraries :: Python Modules",
          "License :: OSI Approved :: GNU General Public License (GPL)",
      ],
      keywords='EEA media centre Add-ons Plone Zope',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=['eea'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          "setuptools",
          "eventlet",
          'eea.vocab',
          "eea.themecentre",
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
