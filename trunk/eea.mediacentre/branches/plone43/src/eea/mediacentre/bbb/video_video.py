from Products.Five import BrowserView
from eea.mediacentre import interfaces
from zope.formlib import form
from eea.mediacentre import EEAMessageFactory as _
from eea.mediacentre.bbb import video_media as media

# class VideoPageView(media.BaseMediaDisplayView, FeatureMixin, BrowserView):
class VideoPageView(media.BaseMediaDisplayView, BrowserView):
    """Page for displaying video.
    """

    adapted_interface = interfaces.IVideo
    media_field = 'file'

    form_fields = form.FormFields(interfaces.IVideo)
    label = u'View Video Info'

    @property
    def template(self):
        return self.index

    def update(self):
        super(VideoPageView, self).update()
        if not interfaces.IVideo(self.context).video_type:
            self.context.plone_utils.addPortalMessage(
                _(u'Unsupported video type'))
