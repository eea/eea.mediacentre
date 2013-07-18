# from persistent.dict import PersistentDict
# try:
#     from zope.app.annotation import interfaces as annointerfaces
# except ImportError, err:
#     # Zope 2.10 support
#     from zope.annotation import interfaces as annointerfaces
#
# _marker = object()
#
#
# class AnnotationDescriptor(property):
#     """A descriptor for accessing annotated fields.
#
#       >>> import zope.interface
#       >>> import zope.schema
#       >>> class IFoo(zope.interface.Interface):
#       ...     field1 = zope.schema.Text(title=u'Field1')
#       >>> class Foo(dict):
#       ...     zope.interface.implements(IFoo, annointerfaces.IAnnotations)
#       ...     field1 = AnnotationDescriptor('key', IFoo['field1'])
#
#       >>> foo = Foo()
#       >>> foo.field1
#
#       >>> foo.field1 = u'abc'
#       >>> foo.field1
#       u'abc'
#
#       >>> del foo.field1
#       >>> foo.field1
#       Traceback (most recent call last):
#         ...
#       AttributeError: 'field1'
#
#     """
#
#     def __init__(self, anno_key, field, subobj_name=None):
#         self.anno_key = anno_key
#         self.field = field
#         self.subobj_name = subobj_name
#
#     def __get__(self, obj, type=None):
#         if self.subobj_name:
#             obj = getattr(obj, self.subobj_name)
#         anno = annointerfaces.IAnnotations(obj)
#         name = self.field.__name__
#         default = getattr(self.field, 'default', _marker)
#
#         d = anno.get(self.anno_key, _marker)
#         if d is _marker:
#             if default is _marker:
#                 raise AttributeError(name)
#             return default
#
#         try:
#             return d[name]
#         except KeyError, e:
#             raise AttributeError(str(e))
#
#     def __set__(self, obj, v):
#         if self.subobj_name:
#             obj = getattr(obj, self.subobj_name)
#         anno = annointerfaces.IAnnotations(obj)
#         d = anno.get(self.anno_key, None)
#         if d is None:
#             d = PersistentDict()
#             anno[self.anno_key] = d
#         name = self.field.__name__
#         d[name] = v
#
#     def __delete__(self, obj):
#         if self.subobj_name:
#             obj = getattr(obj, self.subobj_name)
#         anno = annointerfaces.IAnnotations(obj)
#         d = anno.get(self.anno_key, None)
#         name = self.field.__name__
#         if d is None:
#             raise AttributeError(name)
#         try:
#             del d[name]
#         except KeyError, e:
#             raise AttributeError(str(e))
#
# class ATSchemaFieldDescriptor(property):
#     """A descriptor for accessing AT schema fields.
#
#       >>> class Mock(object):
#       ...     def __init__(self, **kwargs):
#       ...         for key, value in kwargs.items(): setattr(self, key, value)
#       >>> class MockField(object):
#       ...     def __init__(self, v=''): self.attr = v
#       ...     def getAccessor(self, x):
#       ...         return lambda obj=self: obj.attr
#       ...     def getMutator(self, x):
#       ...         def set(v, obj=self):
#       ...             obj.attr = v
#       ...         return set
#       >>> mockfield = MockField()
#       >>> someattr = Mock(schema={'foobar': mockfield})
#       >>> class MockTest(object):
#       ...     someattr = someattr
#       ...     somefield = ATSchemaFieldDescriptor('foobar', 'someattr')
#       >>> obj = MockTest()
#
#       >>> obj.somefield
#       u''
#
#       >>> obj.somefield = 'abc'
#       >>> obj.somefield
#       u'abc'
#
#       >>> obj.somefield = u'someuni'
#       >>> obj.somefield
#       u'someuni'
#
#     """
#
#     def __init__(self, field, subobj_name=None, uni=True):
#         self.field = field
#         self.subobj_name = subobj_name
#         self.ensure_unicode = uni
#
#     def _decode(self, v):
#         v = v or u''
#         if not isinstance(v, unicode) and self.ensure_unicode:
#             v = unicode(v, 'utf-8')
#         return v
#
#     def obj(self, obj):
#         if self.subobj_name:
#             obj = getattr(obj, self.subobj_name)
#         return obj
#
#     def atfield_accessor(self, obj):
#         obj = self.obj(obj)
#         return obj.schema[self.field].getAccessor(obj)
#
#     def atfield_mutator(self, obj):
#         obj = self.obj(obj)
#         return obj.schema[self.field].getMutator(obj)
#
#     def __get__(self, obj, type=None):
#         return self._decode(self.atfield_accessor(obj)())
#
#     def __set__(self, obj, v):
#         self.atfield_mutator(obj)(self._decode(v))
#
#     def __delete__(self, obj):
#         self.atfield_mutator(obj)(None)
#
#
# anno = AnnotationDescriptor
# atfield = ATSchemaFieldDescriptor
