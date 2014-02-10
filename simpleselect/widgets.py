"""Widgets that allow autocompletion."""
import uuid
import string

import django.core.urlresolvers
import django.forms
import django.utils.html
from django.utils.safestring import mark_safe


REGISTRY = {}

# This snippet is output by the widget
ACTIVATE_SCRIPT = string.Template('''
<script type="text/javascript">
    window.SIMPLESELECT_ACTIVATORS = window.SIMPLESELECT_ACTIVATORS || [];

    window.SIMPLESELECT_ACTIVATORS.push(function() {
        SimpleSelect.activateWidget("$input_id", "$url");
    });
</script>
''')


def get_json_url_for_widget(widget_instance,
                            urllookup=django.core.urlresolvers.reverse):
    """Get the URL that provides autocomplete suggestions for a widget.

    :type  widget_instance: AutocompleteSelect
    :param widget_instance: The autocomplete widget.

    :type  urllookup: callable
    :param urllookup:
        A function to search the URLconf with.
        ``django.core.urlresolvers.revrse`` should be sufficient. Will be
        called with the string "simpleselect".

    :rtype: str
    :returns:
        A string like::

            http://example.com/?field=ABCDEF

        where ABCDEF is ``widget_instance.token``.

    """
    return "{}?field={}".format(urllookup('simpleselect'),
                                widget_instance.token)


class AutocompleteSelect(django.forms.Widget):
    """TODO write docstring.

    This is *not* strictly compatible with Django's Select widget because it
    assumes that ``choices`` will be a ``ModelChoiceIterator``.

    """

    def __init__(self, queries, attrs=None, registry=None,
                 token_generator=(lambda self: str(uuid.uuid4())),
                 json_url_maker=get_json_url_for_widget,
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


        :param json_url_maker:
            A callable that is given the widget instance and should return a
            string which jQueryUI Autocomplete can use to fetch autocomplete
            suggestions.

        """
        super().__init__(attrs=attrs)
        self.token = token_generator(self)
        if registry is None:
            registry = REGISTRY
        registry[self.token] = self
        self.queries = queries
        self.js_generator = js_initialization_template
        self.js_url_maker = json_url_maker

    def render(self, name, value, attrs=None):
        """TODO: docstring"""
        if attrs is None:
            attrs = {}
        input = django.forms.HiddenInput()
        input_class = attrs.get('class', '') + " simpleselect"
        attrs['class'] = input_class

        # TODO: extract id_{}
        url = self.js_url_maker(self)
        js = self.js_generator(input_id="id_{}".format(name), url=url)

        return input.render(name, value, attrs) + mark_safe(js)
