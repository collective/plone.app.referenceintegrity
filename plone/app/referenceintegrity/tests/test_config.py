import unittest

from Products.ATContentTypes.content.schemata import relatedItemsField


from plone.app.referenceintegrity.testing import (
        INTEGRATION_REFERENCE_INTEGRITY)
from plone.app.referenceintegrity.config import set_protected_relationships
from plone.app.referenceintegrity.config import get_protected_relationships
from plone.app.referenceintegrity.config import (
        DisableRelationshipsProtectionTemporarily)


class DisableRelationshipsProtectionTestCase(unittest.TestCase):

    layer = INTEGRATION_REFERENCE_INTEGRITY

    def test_raise_ILinkIntegrityInfo(self):

        PROTECTED = [relatedItemsField.relationship]

        set_protected_relationships(PROTECTED)

        with DisableRelationshipsProtectionTemporarily(PROTECTED):
            self.assertEquals(get_protected_relationships(), [])
        self.assertEquals(get_protected_relationships(), PROTECTED)
