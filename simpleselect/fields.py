import functools

import django.db.models
import django.forms

from . import widgets


REGISTRY = {}


def get_qualname(cls):
    """Get the fully qualified name of a class.

    :rtype: str

    For example:

    >>> get_qualname(AutoRegister)
    'simpleselect.fields.AutoRegister'

    """
    return cls.__module__ + '.' + cls.__name__


class AutoRegister(type):

    registry_key_func = get_qualname

    def __init__(cls, name, bases, namespace):
        if cls.__module__ != __name__:
            qualname = get_qualname(cls)
            REGISTRY[qualname] = cls

        return super(AutoRegister, cls).__init__(name, bases, namespace)


class AutoSelectField(django.forms.ModelChoiceField):
    __metaclass__ = AutoRegister

    widget = widgets.AutocompleteSelect

    def __init__(self, *args, **kwargs):
        super(AutoSelectField, self).__init__(self.data, *args, **kwargs)
