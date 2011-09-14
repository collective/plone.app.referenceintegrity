import unittest
from zope.interface import implements

from Products.Archetypes.atapi import StringField
from Products.Archetypes.atapi import Schema
from Products.Archetypes.atapi import registerType
from Products.ATContentTypes.content.document import ATDocument

from plone.app.referenceintegrity.testing import (
        INTEGRATION_REFERENCE_INTEGRITY)

from plone.app.referenceintegrity.interfaces import IReferenceableVocabulary
from plone.app.referenceintegrity.vocabularies import vocabularyRelationship

from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_ID
from plone.app.testing import login
from plone.app.testing import setRoles


class ReferenceableVocabulary(object):

    implements(IReferenceableVocabulary)

    def __init__(self, item):
        self.item = item

    def getObjectsSet(self, obj, value):
        return set([self.item])


class VocabulariesTestCase(unittest.TestCase):

    layer = INTEGRATION_REFERENCE_INTEGRITY

    def test_handler(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)

        portal.invokeFactory('Document', 'referenced')
        vocabulary = ReferenceableVocabulary(portal.referenced)

        ref_schema = ATDocument.schema.copy() + \
            Schema(
                (StringField(
                    name='folderCategory',
                    enforceVocabulary=True,
                    vocabulary=vocabulary,
                    ),
                ))

        class WithReferencedField(ATDocument):
            schema = ref_schema

        registerType(WithReferencedField, 'p.a.referenceintegrity')

        from plone.app.referenceintegrity import vocabularies

        source = WithReferencedField('source')
        source = source.__of__(self.layer['portal'])
        source.initializeArchetype()

        vocabularies.modifiedArchetype(source, None)

        references = source.getReferences(relationship=vocabularyRelationship)
        self.assertEquals([portal.referenced], references)
