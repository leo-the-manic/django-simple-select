import unittest
from unittest import mock

from .. import fields


class AutoSelectFieldTest(unittest.TestCase):

    def test_doesnt_register_baseclass(self):
        """The default registry begins empty."""
        self.assertFalse(fields.REGISTRY)

    def test_new_classes_get_reigstered(self):
        """A new class gets saved to the default registry."""
        registry = {}
        with mock.patch.object(fields, 'REGISTRY', registry):
            class MyField(fields.AutoSelectField):
                pass
        self.assertTrue(registry)
