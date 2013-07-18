import unittest

from .. import widgets


class AutocompleteSelectTest(unittest.TestCase):
    """Tests for the AutoCompleteSelectWidget."""

    def test_constructor_adds_registry_entry(self):
        registry = {}
        w = widgets.AutocompleteSelect(None, None, registry)
        self.assertIn(w.token, registry)
