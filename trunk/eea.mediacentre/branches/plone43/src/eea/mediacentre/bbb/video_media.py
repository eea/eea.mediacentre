from zope.formlib import form
from eea.mediacentre.bbb import video_widget as widget


class BaseMediaDisplayView(form.PageDisplayForm):
    """Base view for displaying media.
    """

    adapted_interface = None
    media_field = None

    def _media_player(self):
        import pdb; pdb.set_trace()
        video = self.adapters.get(self.adapted_interface,
                                  self.adapted_interface(self.context))
        field = self.adapted_interface[self.media_field].bind(video)
        player_widget = widget.MediaPlayerWidget(field, self.request)
        player_widget.name = self.prefix + 'media_player'
        player_widget._data = field.get(video)
        return player_widget

    def update(self):
        super(BaseMediaDisplayView, self).update()
        player_widget = self._media_player()
        self.widgets += form.Widgets([(None, player_widget)], len(self.prefix))
