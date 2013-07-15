from zope import schema
from xml.sax import saxutils
from zope.app.form import browser
from zope.app.form.browser import widget
from zope.cachedescriptors.property import Lazy

from zope.i18nmessageid import MessageFactory
_ = MessageFactory('eea.mediacentre')


class FileField(schema.Field):

    def __init__(self, **kw):
        super(FileField, self).__init__(**kw)

    def _validate(self, value):
        super(FileField, self)._validate(value)




class FileDownloadWidget(browser.DisplayWidget):
    """Widget capable of downloading file.
    """

    required = False

    @property
    def base_url(self):
        contentobj = self.context.context.context
        return contentobj.absolute_url() + '/downloadfile'

    @property
    def filename(self):
        filename = getattr(self, '_filename', None)
        if filename is not None:
            return filename

        if self._renderedValueSet():
            value = self._data
        else:
            # when tracing we come here, and value ends up None, or whatever
            value = self.context.default
        #...and then this condition is a match, and we get None returned.
        #if value == self.context.missing_value:
        #    return None
        self._filename = saxutils.escape(getattr(value, '__name__', ''))

        return self._filename

    @property
    def url(self):
        filename = self.filename
        field = self.context
        obj = field.context
        contentobj = obj.context

        ifname = field.interface.__identifier__
        pos = ifname.rfind('.')
        ifpackage = ''
        if pos > -1:
            ifpackage = ifname[:pos]
            ifname = ifname[pos+1:]

        url = '%s?field=%s:%s:%s' % (self.base_url,
                                     ifpackage,
                                     ifname,
                                     field.getName())
        return url

    def __call__(self):
        url = self.url
        filename = self.filename

        return widget.renderElement(
            u'a',
            href=url,
            contents=filename)


# class FileUploadWidget(widget.SimpleInputWidget):
#
#     @Lazy
#     def _modified_name(self):
#         return "_modify_%s" % self.name
#
#     def __call__(self):
#         kwargs = {'name': self.name,
#                   'filename': '',
#                   'modified_name': self._modified_name,
#                   'keep_file_msg': _(u'Keep existing file'),
#                   'replace_file_msg': _(u'Replace with new file:'),
#                   'no_file_msg': _(u'No file'),
#                   'new_file_msg': _(u'New file:')
#                   }
#
#         if self._data is not self._data_marker:
#             filename = getattr(self._data,'filename', '')
#             if not filename:
#                 filename = getattr(self._data,'__name__', '')
#             kwargs['filename'] = filename
#
#             options = """
#             <div><input type="radio" name="%(modified_name)s:int" value="0" checked="checked" /> %(keep_file_msg)s '%(filename)s'</div>
#             <div><input type="radio" name="%(modified_name)s:int" value="1" /> %(replace_file_msg)s</div>
#             """ % kwargs
#         elif self.context.required:
#             options = """
#             <input type="hidden" name="%(modified_name)s:int" value="1" />
#             """ % kwargs
#         else:
#             options = """
#             <div><input type="radio" name="%(modified_name)s:int" value="0" checked="checked" /> %(no_file_msg)s </div>
#             <div><input type="radio" name="%(modified_name)s:int" value="1" /> %(new_file_msg)s</div>
#             """ % kwargs
#
#         kwargs['options'] = options
#
#         return """
#             %(options)s
#             <div class="_file_%(name)s"><input type="file" name=%(name)s /></div>
#         """ % kwargs
#
#     def _getFormInput(self):
#         modify = int(self.request.get('_modify_%s' % self.name, 0))
#         if not modify:
#             return None
#
#         v = self.request.get(self.name, None) or None
#
#         return v
#
#     def hasInput(self):
#         return bool(self.request.get(self._modified_name, 0))
