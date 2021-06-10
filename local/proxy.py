from multiprocessing.managers import NamespaceProxy


class Proxy(NamespaceProxy):

    _exposed_ = ('__getattribute__', '__setattr__', '__delattr__', 'append')

    def append(self, start_time, processing_delay=None, bandwidth=None, cpu_usage=None, memory_usage=None):
        callmethod = object.__getattribute__(self, '_callmethod')
        return callmethod('append', (start_time, processing_delay, bandwidth, cpu_usage, memory_usage))
