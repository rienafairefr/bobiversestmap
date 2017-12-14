import copy
import os

import json
from collections import OrderedDict
from inspect import ismethod

from dogpile.cache import make_region

os.makedirs('generated', exist_ok=True)

# Define basic in memory caches
file = make_region().configure('dogpile.cache.dbm', expiration_time=30, arguments={
    "filename": os.path.join("generated", "cache.dbm")
})
memory = make_region().configure('dogpile.cache.memory')

def json_dump(obj, filename):
    return json.dump(obj, open(filename, 'w', encoding='utf-8'), indent=2, sort_keys=True)


def make_hash(obj):
    """Make a hash from an arbitrary nested dictionary, list, tuple or
    set.

    """
    if isinstance(obj, set) or isinstance(obj, tuple) or isinstance(obj, list):
        return hash(tuple([make_hash(e) for e in obj]))

    elif not isinstance(obj, dict):
        return hash(obj)

    new_obj = copy.deepcopy(obj)
    for k, v in new_obj.items():
        new_obj[k] = make_hash(v)

    return hash(tuple(frozenset(new_obj.items())))


def fun(t):
    def fun1():
        def fun2():
            return t


def memoize(cache_region=memory, ttl=300, ttl_ignore=False):
    """ Memoized value cache decorator with expiration TTL support.

    :param cache_region:
    :type cache_region: dogpile.cache.CacheRegion
    :param ttl: How long the cache value is valid for (seconds)
    :type ttl: int
    :param ttl_ignore: Return the stored object regardless of TTL
    :type ttl_ignore: bool
    """

    def real_decorator(function):
        def wrap(*args, **kwargs):

            module_name = function.__module__

            if ismethod(function):
                class_name = function.im_class.__name__
            else:
                class_name = ""

            function_name = function.__name__
            tup_key = (module_name, class_name, function_name, args, kwargs)

            cache_key = str(tup_key)

            value = cache_region.get(cache_key, expiration_time=ttl, ignore_expiration=ttl_ignore)
            if not value:
                # print('Stale result %s ' % str(tup_key))
                value = function(*args, **kwargs)
                if value:
                    cache_region.set(cache_key, value)
            # else:
            #   print('Cached result %s ' % str(tup_key))
            return value

        return wrap

    return real_decorator


def sorted_by_key(dictionary):
    return_value = OrderedDict()
    for k in sorted(dictionary):
        return_value[k] = dictionary[k]
    return return_value

