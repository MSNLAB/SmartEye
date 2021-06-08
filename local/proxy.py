from multiprocessing.managers import NamespaceProxy


class Proxy(NamespaceProxy):
    # We need to expose the same __dunder__ methods as NamespaceProxy,
    # in addition to the b method.
    _exposed_ = ('__getattribute__', '__setattr__', '__delattr__', 'append')

    def append(self, start_time, processing_delay=None, bandwidth=None, cpu_usage=None, memory_usage=None):
        callmethod = object.__getattribute__(self, '_callmethod')
        return callmethod('append', (start_time, processing_delay, bandwidth, cpu_usage, memory_usage))
