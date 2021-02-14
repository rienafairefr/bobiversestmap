import copy
import json
import os
from inspect import ismethod
from os.path import exists

from dogpile.cache import make_region
from sortedcontainers import SortedDict
from sqlalchemy import TypeDecorator, String
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm.exc import NoResultFound

if not exists("generated"):
    os.makedirs("generated")

# Define basic in memory caches
file_cache = make_region().configure(
    "dogpile.cache.dbm",
    expiration_time=30,
    arguments={"filename": os.path.join("generated", "cache.dbm")},
)
memory_cache = make_region().configure("dogpile.cache.memory")


def json_dump(obj, filename):
    return json.dump(
        obj,
        open(filename, "w", encoding="utf-8"),
        indent=2,
        sort_keys=True,
        cls=ObjectEncoder,
    )


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


def memoize(cache_region=memory_cache, ttl=300, ttl_ignore=False):
    """Memoized value cache decorator with expiration TTL support.

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

            value = cache_region.get(
                cache_key, expiration_time=ttl, ignore_expiration=ttl_ignore
            )
            if not value:
                # print('Stale result %s ' % str(tup_key))
                value = function(*args, **kwargs)
                if value:
                    cache_region.set(cache_key, value)
            else:
                pass
                # print('Cached result %s ' % str(tup_key))
            return value

        return wrap

    return real_decorator


def sorted_by_key(dictionary):
    return_value = SortedDict()
    for k in sorted(dictionary):
        return_value[k] = dictionary[k]
    return return_value


def stripped(li):
    return [el.strip() for el in li]


class JsonSerializable(object):
    def to_json(self):
        return self.__dict__


class ObjectEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [
                x for x in dir(obj) if not x.startswith("_") and x != "metadata"
            ]:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(
                        data
                    )  # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj)


class ArrayType(TypeDecorator):
    """Sqlite-like does not support arrays.
    Let's use a custom type decorator.

    See http://docs.sqlalchemy.org/en/latest/core/types.html#sqlalchemy.types.TypeDecorator
    """

    impl = String

    def process_bind_param(self, value, dialect):
        if value is None:
            pass
        return json.dumps(value)

    def process_result_value(self, value, dialect):
        return json.loads(value)

    def copy(self):
        return ArrayType(self.impl.length)


def get_one_or_create(
    session, model, create_method="", create_method_kwargs=None, **kwargs
):
    try:
        return session.query(model).filter_by(**kwargs).one(), False
    except NoResultFound:
        kwargs.update(create_method_kwargs or {})
        created = getattr(model, create_method, model)(**kwargs)
        try:
            session.add(created)
            session.flush()
            return created, True
        except IntegrityError as e:
            session.rollback()
            return session.query(model).filter_by(**kwargs).one(), True


class ComparableMixin(object):
    def _compare(self, other, method):
        try:
            return method(self._cmpkey(), other._cmpkey())
        except (AttributeError, TypeError):
            # _cmpkey not implemented, or return different type,
            # so I can't compare with "other".
            return NotImplemented

    def __lt__(self, other):
        return self._compare(other, lambda s, o: s < o)

    def __le__(self, other):
        return self._compare(other, lambda s, o: s <= o)

    def __eq__(self, other):
        return self._compare(other, lambda s, o: s == o)

    def __ge__(self, other):
        return self._compare(other, lambda s, o: s >= o)

    def __gt__(self, other):
        return self._compare(other, lambda s, o: s > o)

    def __ne__(self, other):
        return self._compare(other, lambda s, o: s != o)
