from Acquisition import aq_inner
from zope import interface, component

from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase
from plone.memoize.instance import memoize
from plone.registry.interfaces import IRegistry



try: # Plone 4 and higher
    from Products.ATContentTypes.interfaces.image import IATImage
except: # BBB Plone 3
    from Products.ATContentTypes.interface.image import IATImage

from raptus.article.core.config import MANAGE_PERMISSION
from raptus.article.core import RaptusArticleMessageFactory as _
from raptus.article.core import interfaces
from raptus.article.images.interfaces import IImages, IImage

import pkg_resources


try:
    pkg_resources.get_distribution('plone.app.imagecropping')
except pkg_resources.DistributionNotFound:
    HAS_CROPPING = False
else:
    HAS_CROPPING = True


class IGalleryLeft(interface.Interface):
    """ Marker interface for the gallery left viewlet
    """

class ComponentLeft(object):
    """ Component which lists the images on the left side
    """
    interface.implements(interfaces.IComponent, interfaces.IComponentSelection)
    component.adapts(interfaces.IArticle)

    title = _(u'Gallery left')
    description = _(u'Gallery of the images contained in the article on the left side.')
    image = '++resource++gallery_left.gif'
    interface = IGalleryLeft
    viewlet = 'raptus.article.gallery.left'

    def __init__(self, context):
        self.context = context

class ViewletLeft(ViewletBase):
    """ Viewlet listing the images on the left side
    """

    index = ViewPageTemplateFile('gallery.pt')
    css_class = "componentLeft gallery-left"
    thumb_size = "galleryleft"
    component = "gallery.left"
    type = "left"

    def update(self):
        super(ViewletLeft, self).update()
        props = getToolByName(self.context, 'portal_properties').raptus_article
        self.show_description = props.getProperty('gallery_%s_description' % self.type, False)
        self.maxItems = props.getProperty('gallery_%s_maxitems' % self.type, 0)
        self.relAttr = props.getProperty('gallery_rel_attribute', 'lightbox')
        self.scale = props.getProperty('images_gallery%s_scale' % self.type, None)


    def _class(self, brain, i, l):
        cls = []
        if i == 0:
            cls.append('first')
        if i == l - 1:
            cls.append('last')
        if i % 2 == 0:
            cls.append('odd')
        if i % 2 == 1:
            cls.append('even')
        return ' '.join(cls)


    def _getProperty(self, propertyName, default=None):
        props = getToolByName(self.context, 'portal_properties').raptus_article
        return props.getProperty(propertyName, default)

    @property
    @memoize
    def showCropping(self):
        """Returns True the following conditions are met:
        * plone.app.imagecropping is installed
        * the component uses a plone.app.imaging scale for the gallery image
        * and the scale is croppable
        """
        if self.scale is None or not HAS_CROPPING:
            return False

        from plone.app.imagecropping.browser.settings import ISettings
        registry = component.getUtility(IRegistry)
        settings = registry.forInterface(ISettings)
        if not settings.constrain_cropping:
            return True
        elif self.scale in settings.cropping_for:
            return True

        return False

    @property
    @memoize
    def images(self):
        provider = IImages(self.context)
        manageable = interfaces.IManageable(self.context)
        mship = getToolByName(self.context, 'portal_membership')
        canManage = interfaces.IArticleEditView.providedBy(self.view) and mship.checkPermission(MANAGE_PERMISSION, self.context)
        if canManage:
            items = provider.getImages()
        else:
            items = provider.getImages(component=self.component)

        items = manageable.getList(items, self.component)
        i = 0
        l = len(items)

        for item in items:
            img = IImage(item['obj'])
            item.update({'caption': img.getCaption(),
                         'class': self._class(item['brain'], i, l),
                         'img': img.getImage(self.thumb_size),
                         'img_url': img.getImageURL(self.thumb_size),
                         'description': item['brain'].Description,
                         'rel': None,
                         'url': None,
                         'viewUrl': None})
            if item.has_key('show') and item['show']:
                item['class'] += ' hidden'
            if (self.maxItems and i >= self.maxItems) and not canManage:
                item['class'] += ' invisible'
            w, h = item['obj'].getSize()
            tw, th = img.getSize(self.thumb_size)
            if (tw < w and tw > 0) or (th < h and th > 0):
                item['rel'] = '%s[%s]' % (self.relAttr, self.css_class)
                item['url'] = img.getImageURL(size="popup")
                item['viewUrl'] = item['obj'].absolute_url() + '/view'
            if canManage and self.showCropping:
                item['crop'] = '%s/@@croppingeditor?scalename=%s' % (item['obj'].absolute_url(), self.scale)
            i += 1
        return items

class IGalleryRight(interface.Interface):
    """ Marker interface for the gallery right viewlet
    """

class ComponentRight(object):
    """ Component which lists the images on the right side
    """
    interface.implements(interfaces.IComponent, interfaces.IComponentSelection)
    component.adapts(interfaces.IArticle)

    title = _(u'Gallery right')
    description = _(u'Gallery of the images contained in the article on the right side.')
    image = '++resource++gallery_right.gif'
    interface = IGalleryRight
    viewlet = 'raptus.article.gallery.right'

    def __init__(self, context):
        self.context = context

class ViewletRight(ViewletLeft):
    """ Viewlet listing the images on the right side
    """
    css_class = "componentRight gallery-right"
    thumb_size = "galleryright"
    component = "gallery.right"
    type = "right"

class IGalleryColumns(interface.Interface):
    """ Marker interface for the gallery columns viewlet
    """

class ComponentColumns(object):
    """ Component which lists the articles in multiple columns
    """
    interface.implements(interfaces.IComponent, interfaces.IComponentSelection)
    component.adapts(interfaces.IArticle)

    title = _(u'Gallery columns')
    description = _(u'Gallery of the images contained in the article arranged in columns.')
    image = '++resource++gallery_columns.gif'
    interface = IGalleryColumns
    viewlet = 'raptus.article.gallery.columns'

    def __init__(self, context):
        self.context = context

class ViewletColumns(ViewletLeft):
    """ Viewlet listing the images in multiple columns
    """
    css_class = "columns gallery-columns"
    thumb_size = "gallerycolumns"
    component = "gallery.columns"
    type = "columns"

    def _class(self, brain, i, l):
        i = i % self._getProperty('gallery_columns', 3)
        return super(ViewletColumns, self)._class(brain, i, self._getProperty('gallery_columns', 3))

