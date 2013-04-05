import copy
import pycow

class ProxySet(set):
    """
    Copy on write implementation of a set.
    """
    def __init__(self, obj):
        raise NotImplementedError()

