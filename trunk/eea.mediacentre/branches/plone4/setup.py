""" EEA Media Centre installer
"""
from setuptools import setup, find_packages
import os

name = 'eea.mediacentre'
path = name.split('.') + ['version.txt']
version = open(os.path.join("src/",*path)).read().strip()

setup(name=name,
        version=version,
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

            #TODO: fix me, plone4
            #"eea.dataservice",
            #"Products.EEAContentTypes",
            #"eea.themecentre",
            #"eea.geotags",
            #"p4a.video",
            #"p4a.plonevideo",
            #"p4a.common",
            #"p4a.subtyper",
            #"p4a.fileimage",

            #TODO: plone4, dependencies from tests
            #"Products.EEAPloneAdmin",
            #"Products.ATVocabularyManager",
            #"Products.LinguaPlone",
            #"valentine.linguaflow",
            ],
        entry_points="""
        # -*- Entry points: -*-
        """,
 )
