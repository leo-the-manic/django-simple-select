import unittest
from unittest import mock

from .. import widgets


class AutocompleteSelectTest(unittest.TestCase):
    """Tests for the AutoCompleteSelectWidget."""

    def test_constructor_adds_registry_entry(self):
        """A generated token is used to add an instance to a registry."""
        registry = {}
        w = widgets.AutocompleteSelect(None, registry=registry,
                                       token_generator=lambda self: 'foo'
                                       )
        self.assertIs(registry['foo'], w)

    def test_render_uses_template_func(self):
        """The render method calls a function to get the JS script."""
        test_payload = "Test initialization script"

        def js_template(input_id, url):
            return test_payload

        w = widgets.AutocompleteSelect(
            None, js_initialization_template=js_template)
        with mock.patch.object(w, 'choices', create=True) as choices:
            choices.queryset = {}
            self.assertIn(test_payload, w.render('a', 'b'))

    def test_render_gets_url_from_generator(self):
        """The JS renderer is called with a URL sent from a URL generator."""

        def js_template(input_id, url):
            self.assertEqual(url, "foo")

        def url_gen(widget):
            return 'foo'

        w = widgets.AutocompleteSelect(None,
                                       js_initialization_template=js_template,
                                       json_url_maker=url_gen)
        with mock.patch.object(w, 'choices', create=True) as choices:
            choices.queryset = {}
            w.render('a', 'b')


class UrlGeneratorTest(unittest.TestCase):
    """Tests for the get_json_url_for_widget() function."""

    def test_uses_token_as_getparam(self):
        """The widget's URL contains the widget's token."""
        lookup = lambda s: "foo"
        w = mock.MagicMock()
        w.token = 'bar'

        result = widgets.get_json_url_for_widget(w, lookup)
        self.assertIn(result, "foo?field=bar")
