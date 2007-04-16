MediaCentre
=================

Media Centre is a utility that you can ask what media files are
available.

  >>> from zope.component import getUtility, provideUtility
  >>> from zope.interface import implements
  >>> from eea.mediacentre.interfaces import IMediaCentre
  >>> from eea.mediacentre.interfaces import IMediaCentrePlugin
  >>> mediacentre = getUtility(IMediaCentre)

From the beginning there are no media centre plugins registered and
therefore media centre can't find any media files.

  >>> mediacentre.getMedia()
  []

Media files lookup is done by plugins. One plugin can look in ZCatalog
while others can look in mysql or directly on filesystem. Let's register
a dummy plugin. A utility that provides IMediaCentrePlugin will
automatically be used by the media centre.

  >>> class DummyPlugin1(object):
  ...     implements(IMediaCentrePlugin)
  ...     def getMediaTypes(self): return {'video': {}}
  ...     def getMedia(self, media_type=None, size=None, search={}):
  ...         return [None, None]
  >>> provideUtility(DummyPlugin1())

Now we can ask the Media Centre if there are any video files. The Media
Centre will know that a plugin has been registered.

  >>> mediacentre.getMediaTypes()
  {'video': {}}
  >>> allvideos = mediacentre.getMedia('video')
  >>> len(allvideos)
  2

Let's register one more dummy plugin.

  >>> class DummyPlugin2(object):
  ...     implements(IMediaCentrePlugin)
  ...     def getMediaTypes(self): return {'map': {}}
  ...     def getMedia(self, media_type=None, size=None, search={}):
  ...         return [None, None, None]
  >>> provideUtility(DummyPlugin2())

Now we can ask the Media Centre for all the media files it knows about.
Media Centre will find two plugins and return the result of them both.

  >>> sorted(mediacentre.getMediaTypes())
  ['map', 'video']
  >>> allmedia = mediacentre.getMedia()
  >>> len(allmedia)
  5
