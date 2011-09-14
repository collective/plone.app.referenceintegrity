import unittest2 as unittest

from Products.ATContentTypes.content.schemata import relatedItemsField

from plone.app.linkintegrity.exceptions import (
    LinkIntegrityNotificationException)

from plone.app.referenceintegrity.testing import (
        INTEGRATION_REFERENCE_INTEGRITY)
from plone.app.referenceintegrity.config import set_protected_relationships

from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_ID
from plone.app.testing import login
from plone.app.testing import setRoles


class ReferenceIntegrityHandlersTestCase(unittest.TestCase):

    layer = INTEGRATION_REFERENCE_INTEGRITY

    def test_raise_ILinkIntegrityInfo(self):

        set_protected_relationships([relatedItemsField.relationship])

        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)

        PAGE_ID = 'a_page'
        portal.invokeFactory('Document', PAGE_ID)
        page = getattr(portal, PAGE_ID)

        OTHER_PAGE_ID = 'other_page'
        portal.invokeFactory('Document', OTHER_PAGE_ID)
        other_page = getattr(portal, OTHER_PAGE_ID)

        page.setRelatedItems(other_page)

        with self.assertRaises(LinkIntegrityNotificationException):
            other_page.delete_confirmation()

    def test_do_not_raise_ILinkIntegrityInfo(self):

        set_protected_relationships([])

        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)

        PAGE_ID = 'a_page'
        portal.invokeFactory('Document', PAGE_ID)
        page = getattr(portal, PAGE_ID)

        OTHER_PAGE_ID = 'other_page'
        portal.invokeFactory('Document', OTHER_PAGE_ID)
        other_page = getattr(portal, OTHER_PAGE_ID)

        page.setRelatedItems(other_page)

        other_page.delete_confirmation()
