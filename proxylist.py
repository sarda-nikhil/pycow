import copy
import pycow

class ProxyList(list):
    """
    A proxy wrapper for a normal Python list.

    A lot of functionality is being reproduced from Proxy. Inheriting Proxy would
    simplify things a lot but I get type errors when I try to do so. It is not exactly
    clear what a partial copy entails for a ProxyList so we will not consider this
    option for now.
    """
    __slots__ = ["_obj", "__weakref__", "__slots__", "_is_copied",
                 "_enable_partial_copy", "_attr_map"]

    _is_copied = False

    _list_methods = ['append', 'count', 'extend', 'index', 'insert', 'pop',
                     'remove', 'reverse', 'sort']

    _special_names = [
        '__add__', '__contains__', '__delitem__', '__delslice__', 
        '__eq__', '__ge__', '__getitem__', '__getslice__', '__gt__', '__hash__', 
        '__iadd__', '__imul__', '__iter__', '__le__', '__len__', 
        '__lt__', '__mul__', '__ne__', '__reduce__', '__reduce_ex__', '__repr__', 
        '__reversed__', '__rmul__', '__setitem__', '__setslice__', '__sizeof__',
        '__str__', '__subclasshook__', '__xor__', 'next',
    ]

    def __init__(self, obj, _partial_copy=False):
        object.__setattr__(self, "_obj", obj)
        object.__setattr__(self, "_enable_partial_copy", _partial_copy)

    def append(self, obj):
        if not self._is_copied:
            self._obj = copy.deepcopy(self._obj)
        self._obj.append(obj)

    def count(self, obj):
        return self._obj.count(obj)

    def extend(self, iterable):
        if not self._is_copied:
            self._obj = copy.deepcopy(self._obj)
        self._obj.extend(iterable)

    def index(self, obj):
        return self._obj.index(obj)

    def insert(self, idx, obj):
        if not self._is_copied:
            self._obj = copy.deepcopy(self._obj)
        self._obj.insert(idx, obj)

    def pop(self):
        if not self._is_copied:
            self._obj = copy.deepcopy(self._obj)
        return self._obj.pop()

    def remove(self, obj):
        if not self._is_copied:
            self._obj = copy.deepcopy(self._obj)
        self._obj.remove(obj)

    def reverse(self):
        if not self._is_copied:
            self._obj = copy.deepcopy(self._obj)
        self._obj.reverse()

    def sort(self, cm='None', key='None', reverse='False'):
        if not self._is_copied:
            self._obj = copy.deepcopy(self._obj)
        self._obj.sort(cm, key, reverse)

    @classmethod
    def _create_class_proxy(cls, theclass):
        """creates a proxy for the given class"""
        
        def make_method(name):
            def method(self, *args, **kw):
                if name in cls._special_names and args is not ():
                    args = map(lambda x: x._obj if isinstance(x, pycow.Proxy) else x, args)
                return getattr(object.__getattribute__(self, "_obj"), name)(*args, **kw)
            return method
        
        namespace = {}
        for name in cls._special_names:
            if hasattr(theclass, name):
                namespace[name] = make_method(name)
        return type("%s(%s)" % (cls.__name__, theclass.__name__), (cls,), namespace)
    
    def __new__(cls, obj, *args, **kwargs):
        """
        creates an proxy instance referencing `obj`. (obj, *args, **kwargs) are
        passed to this class' __init__, so deriving classes can define an 
        __init__ method of their own.
        note: _class_proxy_cache is unique per deriving class (each deriving
        class must hold its own cache)
        """
        try:
            cache = cls.__dict__["_class_proxy_cache"]
        except KeyError:
            cls._class_proxy_cache = cache = {}
        try:
            theclass = cache[obj.__class__]
        except KeyError:
            cache[obj.__class__] = theclass = cls._create_class_proxy(obj.__class__)
        ins = list.__new__(theclass)
        theclass.__init__(ins, obj, *args, **kwargs)
        return ins
