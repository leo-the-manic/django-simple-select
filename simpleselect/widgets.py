"""Widgets that allow autocompletion."""
import uuid
import string

import django.forms
import django.utils.html
from django.utils.safestring import mark_safe


REGISTRY = {}

ACTIVATE_SCRIPT = string.Template('''
jQuery(function() {
    var args = jQuery.extend({ source: $url }, simpleselectDefaultArgs);
    jQuery("#$input_id").autocomplete(args);
});
''')


class AutocompleteSelect(django.forms.Widget):
    """TODO write docstring.

    This is *not* strictly compatible with Django's Select widget because it
    assumes that ``choices`` will be a ``ModelChoiceIterator``.

    """

    def __init__(self, queries, attrs=None, registry=None,
                 token_generator=(lambda self: uuid.uuid4),
                 js_initialization_template=ACTIVATE_SCRIPT.substitute):
        """Create a new autocompleting select widget.

        :type  registry: dict
        :param registry: A map of tokens to widget instances; the widget adds
                         itself to this registry when constructed. By default
                         this is used in the JSON service to access the
                         choices of this widget.

        :param js_initialization_template:
            A callable that produces a string which when injected into the
            page's markup will initialize the the autocomplete widget. The
            callable will recieve the following keyword arguments:

            * url

            * input_id

            It should produce a string (which will be marked safe).

        """
        super(AutocompleteSelect, self).__init__(attrs=attrs)
        self.token = token_generator(self)
        if registry is None:
            registry = REGISTRY
        registry[self.token] = self

    def render(self, name, value, attrs=None,
               template_renderer=ACTIVATE_SCRIPT.substitute):
        input = django.forms.HiddenInput()
        msg = mark_safe("Queryset: <code>{}</code>".format(
            django.utils.html.escape(repr(self.choices.queryset))))
        input_class = attrs.get('class', '') + " simpleselect"
        attrs['class'] = input_class

        return msg + input.render(name, value, attrs)
