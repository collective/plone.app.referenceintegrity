from Products.CMFCore.utils import getToolByName

from plone.app.linkintegrity.references import updateReferences

from plone.app.referenceintegrity.interfaces import IReferenceableVocabulary

vocabularyRelationship = "referenceableVocabularyTerm"


def modifiedArchetype(obj, event):
    """ an archetype based object was modified """
    rc = getToolByName(obj, 'reference_catalog', None)
    if rc is None:
        # `updateReferences` is not possible without access
        # to `reference_catalog`
        return
    refs = set()
    for field in obj.Schema().fields():
        if IReferenceableVocabulary.providedBy(field.vocabulary):
            accessor = field.getAccessor(obj)
            value = accessor()
            refs |= field.vocabulary.getObjectsSet(obj, value)
    updateReferences(obj, vocabularyRelationship, refs)
