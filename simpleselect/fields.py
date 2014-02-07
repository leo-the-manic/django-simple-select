import hashlib

import django.db.models
import django.forms

from . import widgets


def sha1(s):
    """Get a SHA1 hash of string `s`."""
    algo = hashlib.new('sha1')
    algo.update(s.encode('ascii'))
    return algo.hexdigest()


REGISTRY = {}


def get_qualname(cls):
    """Get the fully qualified name of a class.

    :rtype: str

    For example:

    >>> get_qualname(AutoRegister)
    'simpleselect.fields.AutoRegister'

    """
    qualname = cls.__module__ + '.' + cls.__name__
    return qualname


class AutoRegister(type):

    def __init__(cls, name, bases, namespace):
        if cls.__module__ != __name__:
            key = cls.registry_key_func()
            REGISTRY[key] = cls

        super().__init__(name, bases, namespace)


class AutoSelectField(django.forms.ModelChoiceField, metaclass=AutoRegister):

    @classmethod
    def registry_key_func(cls):
        return sha1(get_qualname(cls))[:5]

    def __init__(self, *args, **kwargs):
        if not 'widget' in kwargs:
            widget = widgets.AutocompleteSelect(
                queries=self.queries,
                token_generator=lambda w: type(self).registry_key_func())
            widget.choices = self.data
            kwargs['widget'] = widget
        super().__init__(self.data, *args, **kwargs)
