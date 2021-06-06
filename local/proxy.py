from multiprocessing.managers import NamespaceProxy


class Proxy(NamespaceProxy):
    # We need to expose the same __dunder__ methods as NamespaceProxy,
    # in addition to the b method.
    _exposed_ = ('__getattribute__', '__setattr__', '__delattr__')

    # def append(self, start):
    #     callmethod = object.__getattribute__(self, '_callmethod')
    #     return callmethod('append')
