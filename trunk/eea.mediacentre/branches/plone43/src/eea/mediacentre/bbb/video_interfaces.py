# from zope import interface
# from zope import schema
# from eea.mediacentre.bbb import fileimage_file as p4afile
# from eea.mediacentre.bbb import fileimage_image as p4aimage
#
# from eea.mediacentre import EEAMessageFactory as _
#
#
# class IVideo(interface.Interface):
#     """Objects which have video information.
#     """
#
#     title = schema.TextLine(title=_(u'Title'), required=False)
#     description = schema.Text(title=_(u'Description'), required=False)
#     rich_description = schema.Text(title=_(u'Rich Text Description'),
#                                    required=False)
#     file = p4afile.FileField(title=_(u'File'), required=False)
#     width = schema.Int(title=_(u'Width'), default=480, required=False,
#                        readonly=False)
#     height = schema.Int(title=_(u'Height'), default=360, required=False,
#                         readonly=False)
#     duration = schema.Float(title=_(u'Duration'), required=False, readonly=False)
#
#     video_image = p4aimage.ImageField(title=_(u'Image'), required=False,
#                                       preferred_dimensions=(320, 240))
#
#     video_type = schema.TextLine(title=_(u'Type'),
#                                  required=True,
#                                  readonly=True)
#
#     video_author = schema.TextLine(title=_(u'Author'), required=False)
#
#     urls = schema.Tuple(
#         title=_(u'Video URLs'), required=False, default=(),
#         value_type=schema.Tuple(title=_(u'Mimetype and URL pair'),
#                                 min_length=2, max_length=2))
