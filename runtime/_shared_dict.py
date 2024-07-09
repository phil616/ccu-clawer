import threading

class _SharedDict:
    """
    一个线程安全的字典,使用可重入锁来保证读写安全。
    内部使用一个普通的字典self._data来存储实际的数据。
    使用一个可重入锁self._lock来保护对self._data的访问,确保在多线程环境下的读写安全。
    对字典的各种常用操作如__getitem__, __setitem__, get, update等都加了锁保护,保证原子性。
    锁采用了 with self._lock 的形式,确保锁能够被正确释放,避免死锁。
    对于返回字典视图的方法如keys(),values(),items()等,为了数据一致性,会返回一个数据快照,即将数据复制一份再返回。
    通过实现__len__,__iter__,__repr__等特殊方法,使得SharedDict的行为与普通字典基本一致。
    """
    def __init__(self):
        self._data = {}
        self._lock = threading.RLock()
    
    def __getitem__(self, key):
        with self._lock:
            return self._data[key]
    
    def __setitem__(self, key, value):
        with self._lock:
            self._data[key] = value
    
    def __delitem__(self, key):
        with self._lock:
            del self._data[key]
    
    def __contains__(self, key):
        with self._lock:
            return key in self._data
    
    def get(self, key, default=None):
        with self._lock:
            return self._data.get(key, default)
    
    def setdefault(self, key, default=None):
        with self._lock:
            return self._data.setdefault(key, default)
    
    def pop(self, key, default=None):
        with self._lock:
            return self._data.pop(key, default)
    
    def popitem(self):
        with self._lock:
            return self._data.popitem()
    
    def clear(self):
        with self._lock:
            self._data.clear()
    
    def update(self, other=None, **kwargs):
        with self._lock:
            if other is not None:
                self._data.update(other)
            self._data.update(kwargs)
    
    def keys(self):
        with self._lock:
            return list(self._data.keys())
    
    def values(self):
        with self._lock:
            return list(self._data.values())
    
    def items(self):
        with self._lock:
            return list(self._data.items())
    
    def __len__(self):
        with self._lock:
            return len(self._data)
    
    def __iter__(self):
        with self._lock:
            return iter(self._data)
    
    def __repr__(self):
        with self._lock:
            return repr(self._data)