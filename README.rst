Introduction
============

Provides basic gallery components.

The following features for raptus.article are provided by this package:

Components
----------
    * Gallery left (Gallery of the images contained in the article on the left side)
    * Gallery right (Gallery of the images contained in the article on the right side)
    * Gallery columns (Gallery of the images contained in the article arranged in columns)

Dependencies
------------
    * raptus.article.images


Configuration
-------------

Maximum number of Items
```````````````````````

Use the ``gallery_left_maxitems`` (``gallery_right_maxitems`` and
``gallery_columns_maxitems`` respectively) property to limit the
number of images shown in a gallery.
(The `Javascript popup`_ will display the other images as well)


Javascript popup
````````````````

By default this component opens images in a `Products.jsImagePopups`_ gallery.

To use `collective.prettyphoto`_ install the package and set the property
``gallery_rel_attribute`` to ``prettyPhoto``.

.. _`Products.jsImagePopups`: http://pypi.python.org/pypi/Products.jsImagePopups
.. _`collective.prettyphoto`: http://pypi.python.org/pypi/collective.prettyphoto


plone.app.imaging
`````````````````


To use plone.app.imaging scales simply set the corresponding properties to the
name if the image scale.

If present, those will overrule the width and height settings.

available properties:

* ``images_galleryleft_scale``
* ``images_galleryright_scale``
* ``images_gallerycolumns_scale``
* ``imagse_popup_scale``


plone.app.imagecropping
```````````````````````

If you use scales for the image dimensions and `plone.app.imagecropping`__ is
installed you'll see a cropping icon in the management links for the gallery
items (when you are in component editing mode)

This icon will open an overlay to define the cropping region for the used scale
and update the image when the dialog is closed

.. __: https://pypi.python.org/pypi/plone.app.imagecropping


Installation
============

Note if you install raptus.article.default you can skip this installation steps.

To install raptus.article.gallery into your Plone instance, locate the file
buildout.cfg in the root of your Plone instance directory on the file system,
and open it in a text editor.

Add the actual raptus.article.gallery add-on to the "eggs" section of
buildout.cfg. Look for the section that looks like this::

    eggs =
        Plone

This section might have additional lines if you have other add-ons already
installed. Just add the raptus.article.gallery on a separate line, like this::

    eggs =
        Plone
        raptus.article.gallery

Note that you have to run buildout like this::

    $ bin/buildout

Then go to the "Add-ons" control panel in Plone as an administrator, and
install or reinstall the "raptus.article.default" product.

Note that if you do not use the raptus.article.default package you have to
include the zcml of raptus.article.gallery either by adding it
to the zcml list in your buildout or by including it in another package's
configure.zcml.

Usage
=====

Components
----------
Navigate to the "Components" tab of your article and select one of the gallery
components and press "save and view". Note that at least one image has to be contained
in the article in which this component is active.

Copyright and credits
=====================

raptus.article is copyrighted by `Raptus AG <http://raptus.com>`_ and licensed under the GPL.
See LICENSE.txt for details.

Credits:

* Harald Frießnegger (fRiSi), `Webmeisterei GmbH`_

  additional configuration options, support for `collective.prettyPhoto` and
  `plone.app.imaging` scales

.. _`Webmeisterei GmbH`: http://webmeisterei.com
