""" p4a.common.at module
"""
from zope.app.form.browser.textwidgets import TextAreaWidget

from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from Acquisition import aq_inner, aq_base


class RichTextEditWidget(BrowserView, TextAreaWidget):
    """A Zope 3 based formlib widget that exposes whatever rich text
    editor is configured inside Plone.
    """

    template = ViewPageTemplateFile('atwidget.pt')

    def __init__(self, *args, **kwargs):
        BrowserView.__init__(self, *args, **kwargs)
        TextAreaWidget.__init__(self, *args, **kwargs)

    def content_context(self):
        """ content_context
        """
        current = aq_inner(self.context.context)
        content_context = None
        for _x in range(100):
            if hasattr(current, '__of__'):
                content_context = current
                break
            if hasattr(current, 'context'):
                current = current.context
            else:
                break
        return content_context

    def __call__(self):
        self.context.REQUEST = self.request
        if not 'body' in self.request.form:
            self.request.form['body'] = self.context.get(self.context.context)
        template = aq_base(self.template)
        widget = aq_base(self)
        content_context = self.content_context()

        template = template.__of__(widget.__of__(content_context))
        return template()

    def hasInput(self):
        """ hasInput
        """
        return 'body' in self.request.form

    def getInputValue(self):
        """ getInputValue
        """
        return self.request.form.get('body', None)

