Media Centre
============
Media Centre offers an API to search for media content on the website.
The actual content is looked up by plugins. A plugin should register
itself as a utility that provides IMediaCentrePlugin. Then media centre
will find it and can ask it what media content it provides.


In order to get media centre working there are a few things that has to be done.

* Copy site.zcml from Five/skel to your own etc folder.
* Create a package-includes directory in etc.
* Put the slugs you want in package-includes and the packages will get
  loaded automatically
* zopectl test (at least in 2.9.x of Zope) only checks what's in
  lib/python and does not handle eggs. To test media centre:

      ./bin/zopectl test --test-path lib/python/eea.mediacentre/src
      -m testMediaCentre
