项目概述
========

``YYDict``\ 把一个普通字典转成一个属性字典
YYDict is a module that exposes a dictionary subclass that allows items to be set like attributes.
Values are gettable and settable using both attribute and item syntax.

INSTALL
--------

``YYDict`` 安装也非常方便,只要使用pip 工具即可.

.. code:: python


   pip install yydict

USAGE
-----

HOW TO USE THE YYDict ?

YYDict 使用起来非常方便,可以使用 ``obj.xxx`` 来访问字典中对应的\ ``key``
, 对于字典中的\ ``key`` 可以通过访问属性的方式进行访问.

.. code:: python


   from yydict import YYDict

   >>> data = {'foo': 3, 'bar': {'x': 1, 'y': 2}}
   ... d = YYDict(data)
   >>>
   >>> d.foo
   3
   >>> d.bar
   {'x': 1, 'y': 2}
   >>> d.bar.x
   1
   >>> d.bar.y
   2
   >>> d.aaa
   Traceback (most recent call last):
   ...
   AttributeError: 'YYDict' object has no attribute 'aaa'

   >>> # 转成 常规的词典
   >>> regular  = d.to_dict()
   >>> regular
   {'foo': 3, 'bar': {'x': 1, 'y': 2}}
   >>> data
   {'foo': 3, 'bar': {'x': 1, 'y': 2}}
   >>> data  == regular
   True
   >>> data is regular
   False
   >>> type(data),type(regular)
   (<class 'dict'>, <class 'dict'>)


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


   >>> # Values extraction
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

Similar tools
-------------

-  `TreeDict <https://github.com/hoytak/treedict/tree/master>`__, a fast
   and full-featured dict-like tree container.

-  `addict <https://github.com/mewwts/addict>`__

-  `easydict <https://github.com/makinacorpus/easydict/tree/master>`__
