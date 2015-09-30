


class ItemException(Exception):
    pass


class LazyItemValue(object):
    pass


class BaseItem(object):
    """
    """
    extra_attributes = []
    translate = {}

    def __init__(self, resource, **kwargs):
        self.resource = resource
        self._extra_data = {}
        self.name = None
        for key in self.extra_attributes:
            setattr(self, key.lower(), LazyItemValue())
        for key, value in kwargs.items():
            attr = key.lower()
            if attr in self.translate:
                attr = self.translate[attr]
            setattr(self, attr, value)

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return "<%s: %s>" % (self.__class__.__name__, str(self))

    def __getattribute__(self, item):
        value = super(BaseItem, self).__getattribute__(item)
        klass = super(BaseItem, self).__getattribute__('__class__')
        if isinstance(value, LazyItemValue) and \
           item not in klass.extra_attributes:
            raise AttributeError('%s is not an attribute' % item)
        if isinstance(value, LazyItemValue):
            d = super(BaseItem, self).__getattribute__('__dict__')
            data = d['resource'].db.get_data(d['resource'].get_path,
                                             id=d['id'])
            for key, value in data.items():
                setattr(self, key.lower(), value)
        return super(BaseItem, self).__getattribute__(item)
