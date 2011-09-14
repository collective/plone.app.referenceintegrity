import unittest

from Products.ATContentTypes.content.schemata import relatedItemsField


from plone.app.referenceintegrity.testing import (
        INTEGRATION_REFERENCE_INTEGRITY)
from plone.app.referenceintegrity.config import set_protected_relationships
from plone.app.referenceintegrity.config import get_protected_relationships
from plone.app.referenceintegrity.config import DisabledProtection


class ConfigTestCase(unittest.TestCase):

    layer = INTEGRATION_REFERENCE_INTEGRITY

    def test_config(self):

        PROTECTED = [relatedItemsField.relationship]

        set_protected_relationships(PROTECTED)
        self.assertEquals(get_protected_relationships(), PROTECTED)

    def test_context_manager(self):

        PROTECTED = [relatedItemsField.relationship]

        set_protected_relationships(PROTECTED)

        with DisabledProtection(PROTECTED):
            self.assertEquals(get_protected_relationships(), [])
        self.assertEquals(get_protected_relationships(), PROTECTED)
