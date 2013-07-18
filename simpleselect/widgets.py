"""Widgets that allow autocompletion."""
import uuid

import django.forms
import django.utils.html
from django.utils.safestring import mark_safe


REGISTRY = {}


class AutocompleteSelect(django.forms.Widget):
    """TODO write docstring."""

    def __init__(self, queries, attrs=None, registry=None):
        super(AutocompleteSelect, self).__init__(attrs=attrs)
        self.token = uuid.uuid4()
        if registry is None:
            registry = REGISTRY
        registry[self.token] = self

    def render(self, name, value, attrs=None):
        input = django.forms.HiddenInput()
        msg = mark_safe("Queryset: <code>{}</code>".format(
            django.utils.html.escape(repr(self.choices.queryset))))
        input_class = attrs.get('class', '') + " simpleselect"
        attrs['class'] = input_class
        return msg + input.render(name, value, attrs)
