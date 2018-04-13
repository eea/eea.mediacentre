================
EEA Media Centre
================
.. image:: https://ci.eionet.europa.eu/buildStatus/icon?job=eea/eea.mediacentre/develop
  :target: https://ci.eionet.europa.eu/job/eea/job/eea.mediacentre/job/develop/display/redirect
  :alt: develop
.. image:: https://ci.eionet.europa.eu/buildStatus/icon?job=eea/eea.mediacentre/master
  :target: https://ci.eionet.europa.eu/job/eea/job/eea.mediacentre/job/master/display/redirect
  :alt: master

Media Centre offers an API to search for media content on the website.
The actual content is looked up by plugins. A plugin should register
itself as a utility that provides IMediaCentrePlugin. Then media centre
will find it and can ask it what media content it provides.

Contents
========

.. contents::


Getting started
===============

In order to get media centre working there are a few things that has to be done.

* Copy site.zcml from Five/skel to your own etc folder.
* Create a package-includes directory in etc.
* Put the slugs you want in package-includes and the packages will get
  loaded automatically
* zopectl test (at least in 2.9.x of Zope) only checks what's in
  lib/python and does not handle eggs. To test media centre:

      ./bin/zopectl test --test-path lib/python/eea.mediacentre/src
      -m testMediaCentre

Source code
===========

- Latest source code (Plone 4 compatible):
  https://github.com/eea/eea.mediacentre

Copyright and license
=====================
The Initial Owner of the Original Code is European Environment Agency (EEA).
All Rights Reserved.

The EEA Media Centre (the Original Code) is free software;
you can redistribute it and/or modify it under the terms of the GNU
General Public License as published by the Free Software Foundation;
either version 2 of the License, or (at your option) any later
version.

More details under docs/License.txt


Funding
=======

EEA_ - European Environment Agency (EU)

.. _EEA: http://www.eea.europa.eu/
