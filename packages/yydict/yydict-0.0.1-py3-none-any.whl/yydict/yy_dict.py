import warnings


class YYDict(dict):
    """
    Get attributes

    >>> d = YYDict({'foo':3})
    >>> d['foo']
    3
    >>> d.foo
    3
    >>> d.bar
    Traceback (most recent call last):
    ...
    AttributeError: 'YYDict' object has no attribute 'bar'


    Works recursively
    >>> d = YYDict({'foo':3, 'bar':{'x':1, 'y':2}})
    >>> isinstance(d.bar, dict)
    True
    >>> d.bar.x
    1

    Bullet-proof

    >>> YYDict({})
    {}
    >>> YYDict(d={})
    {}
    >>> YYDict(None)
    {}
    >>> d = {'a': 1}
    >>> YYDict(**d)
    {'a': 1}
    >>> YYDict((('a', 1), ('b', 2)))
    {'a': 1, 'b': 2}

    Set attributes

    >>> d = YYDict()
    >>> d.foo = 3
    >>> d.foo
    3
    >>> d.bar = {'prop': 'value'}
    >>> d.bar.prop
    'value'
    >>> d
    {'foo': 3, 'bar': {'prop': 'value'}}
    >>> d.bar.prop = 'newer'
    >>> d.bar.prop
    'newer'


    Values extraction

    >>> d = YYDict({'foo':0, 'bar':[{'x':1, 'y':2}, {'x':3, 'y':4}]})
    >>> isinstance(d.bar, list)
    True
    >>> from operator import attrgetter
    >>> list(map(attrgetter('x'), d.bar))
    [1, 3]
    >>> list(map(attrgetter('y'), d.bar))
    [2, 4]
    >>> d = YYDict()
    >>> list(d.keys())
    []
    >>> d = YYDict(foo=3, bar=dict(x=1, y=2))
    >>> d.foo
    3
    >>> d.bar.x
    1

    Still like a dict though

    >>> o = YYDict({'clean':True})
    >>> list(o.items())
    [('clean', True)]

    And like a class

    >>> class Flower(YYDict):
    ...     power = 1
    ...     mean = {}
    ...     color = {"r": 100, "g": 0, "b": 0}
    ...
    >>> f = Flower()
    >>> f.power
    1
    >>> f.color.r
    100
    >>> f.mean.x = 10
    >>> f.mean.x
    10
    >>> f = Flower({'height': 12})
    >>> f.height
    12
    >>> f['power']
    1
    >>> sorted(f.keys())
    ['color', 'height', 'mean', 'power']

    update and pop items
    >>> d = YYDict(a=1, b='2')
    >>> e = YYDict(c=3.0, a=9.0)
    >>> d.update(e)
    >>> d.c
    3.0
    >>> d['c']
    3.0
    >>> d.get('c')
    3.0
    >>> d.update(a=4, b=4)
    >>> d.b
    4
    >>> d.pop('a')
    4
    >>> d.a
    Traceback (most recent call last):
    ...
    AttributeError: 'YYDict' object has no attribute 'a'
    """

    def __init__(self, d=None, *args, **kwargs):
        super(YYDict, self).__init__(*args, **kwargs)
        d = dict(d) if d else {}
        if kwargs:
            d.update(**kwargs)
        for k, v in d.items():
            try:
                setattr(self, k, v)
            except TypeError as e:
                warnings.warn(f"k:{k},v:{v} , k must be string! this attribute ignored",
                              category=RuntimeWarning,
                              stacklevel=2
                              )
                super(YYDict, self).__setitem__(k, v)

        # Class attributes
        for k in self.__class__.__dict__.keys():
            if not (k.startswith('__') and k.endswith('__')) and \
                    not k in ('update', 'pop', 'to_dict'):
                setattr(self, k, getattr(self, k))

    def __setattr__(self, name, value):
        if isinstance(value, (list,)):
            value = [self.__class__(x)
                     if isinstance(x, dict) else x for x in value]
        elif isinstance(value, (tuple,)):
            value = tuple([self.__class__(x)
                           if isinstance(x, dict) else x for x in value])
        elif isinstance(value, dict) and not isinstance(value, YYDict):
            value = YYDict(value)
        else:
            if name in ['keys', 'items']:
                raise AttributeError(f"can't set {name!r}")
        try:
            super(YYDict, self).__setattr__(name, value)
        except TypeError:
            warnings.warn(f"name:{name!r} must be string! this attribute ignored")
        super(YYDict, self).__setitem__(name, value)

    __setitem__ = __setattr__

    def __delattr__(self, item):
        del self[item]

    def __getattr__(self, item):
        return self.__getitem__(item)

    def __missing__(self, key):
        """
        :param key:
        :return:
        """
        raise AttributeError(f"{self.__class__.__name__!r} object has no attribute {key!r}")

    def __or__(self, other):
        if not isinstance(other, (type(self), dict)):
            return NotImplemented(f'not implemented. {other}')

        ins = self.__class__(self)
        ins.update(other)
        return ins

    def update(self, e=None, **kw):
        d = e or dict()
        d.update(kw)
        for k in d:
            setattr(self, k, d[k])

    def pop(self, k, d=None):
        """
        delete attribute
        :param k:
        :param d:
        :return:
        """
        value = super(YYDict, self).pop(k, d)
        object.__delattr__(self, k)
        return value

    def to_dict(self):
        """
        transfer to a normal dict
        :return:
        """
        base = {}
        for key, value in self.items():
            if isinstance(value, type(self)):
                base[key] = value.to_dict()
            elif isinstance(value, (list, tuple)):
                base[key] = type(value)(
                    item.to_dict() if isinstance(item, type(self)) else
                    item for item in value)
            else:
                base[key] = value

        return base


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print("test docs passed")
    pass
    # d = YYDict({'foo': 3})
    # print(d.bar)

    # d = YYDict(foo=3, bar=dict(x=1, y=2))

    # d = YYDict(a=1, b='2')
    # print(d)
    #
    # c = d.pop('a')
    # print(c)
    #
    # print(d)
    # d = YYDict((('a', 1), ('b', 2)))
    # print(d)

    # d = YYDict({'foo': 3, 'bar': {'x': 1, 'y': 2}})
    # print(type(d))
    #
    # print(d)

    # d.update({'fruits': [1, 2, 3]})
    # d = {'keys': 'test'}

    # some_dict = {'a': {'b': 11111}}

    # b = YYDict([("0", 1), ("1", 2), ("2", 3)])
    # print(b)

    # class Flower(YYDict):
    #     power = 1
    #     mean = {}
    #     color = {"r": 100, "g": 0, "b": 0}
    #
    #
    # f = Flower()
    # print(f.power)

    # prop = YYDict([("0", 1), ("1", 2), ("2", 3)])
    # print(prop)

    # prop = YYDict([(0, 1), (1, 2), (2, 3)])
    # print(prop)
