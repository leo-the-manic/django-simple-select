"""Widgets that allow autocompletion."""
import uuid
import string

import django.forms
import django.utils.html
from django.utils.safestring import mark_safe


REGISTRY = {}

ACTIVATE_SCRIPT = string.Template('''
<script language="javascript">
    jQuery(function() {
        var args = jQuery.extend({ source: $url }, simpleselectDefaultArgs);
        jQuery("#$input_id").autocomplete(args);
    });
</script>
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

        :param token_generator:
            A callable which takes the widget instance and returns a suitable
            token. Note that the widget does not have a "field name" or
            anything of that sort at its disposal, and this is due to the
            architecture of the Django form system.  Defaults to the Python
            standard library ``uuid.uuid4`` function.

        :type  registry: dict
        :param registry:
            A map of tokens to widget instances; the widget adds itself to this
            registry when constructed. By default this is used in the JSON
            service to access the choices of this widget. By default, uses a
            plain dictionary at ``simpleselect.REGISTRY``.
            TODO: make sure this forward is setup properly

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
        self.js_generator = js_initialization_template

    def render(self, name, value, attrs=None):
        if attrs is None:
            attrs = {}
        input = django.forms.HiddenInput()
        msg = mark_safe("Queryset: <code>{}</code>".format(
            django.utils.html.escape(repr(self.choices.queryset))))
        input_class = attrs.get('class', '') + " simpleselect"
        attrs['class'] = input_class
        js = self.js_generator(input_id="id_" + name, url='http://google.com/')

        return msg + input.render(name, value, attrs) + mark_safe(js)
