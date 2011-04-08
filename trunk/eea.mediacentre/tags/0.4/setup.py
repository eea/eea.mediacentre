from setuptools import setup, find_packages
import os
name = 'eea.mediacentre'
path = name.split('.') + ['version.txt']
version = open(os.path.join("src/",*path)).read().strip()

setup(name='eea.mediacentre',
        version=version,
        url='http://svn.eionet.europa.eu/projects/'
        'Zope/browser/trunk/eea.mediacentre',
        description='Media Centre utility and API',
        author='Tim Terlegard, Antonio De Marinis (EEA), European Environment Agency (EEA)',
        author_email='webadmin@eea.europa.eu',
        license='GPL',
        long_description=open("README.txt").read() + "\n" +
                  open(os.path.join("docs", "HISTORY.txt")).read(),
        classifiers=['Development Status :: 5 - Production/Stable',
            'Framework :: Zope3',
            'Intended Audience :: Developers'],
        packages=find_packages('src'),
        package_dir={'': 'src'},
        namespace_packages = ['eea'],
        include_package_data=True,
        zip_safe=False,
        install_requires=[
            "setuptools",
            ],
        entry_points="""
        # -*- Entry points: -*-
        """,
 )
