import unittest

import mock

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
