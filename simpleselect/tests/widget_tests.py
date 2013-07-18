import unittest

from .. import widgets


class AutocompleteSelectTest(unittest.TestCase):
    """Tests for the AutoCompleteSelectWidget."""

    def test_constructor_adds_registry_entry(self):
        registry = {}
        w = widgets.AutocompleteSelect(None, registry=registry,
                                       token_generator=lambda self: 'foo'
                                       )
        self.assertIs(registry['foo'], w)
