from setuptools import setup, find_packages

setup(name='eea.mediacentre',
      version='0.1',
      url='http://svn.eionet.europa.eu/repositories/Zope',
      description='Media Centre utility and API',
      author='Tim Terlegard',
      long_description=file('README.txt').read(),
      classifiers=['Development Status :: 5 - Production/Stable',
                   'Framework :: Zope3',
                   'Intended Audience :: Developers'],
      packages=find_packages('src'),
      package_dir={'': 'src'},
      include_package_data=True,
      zip_safe=False,
      )
