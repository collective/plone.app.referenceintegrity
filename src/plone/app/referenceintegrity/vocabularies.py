from plone.app.linkintegrity.references import updateReferences

from plone.app.referenceintegrity.interfaces import IReferenceableVocabulary

vocabularyRelationship = "referenceableVocabularyTerm"


def modifiedArchetype(obj, event):
    """ an archetype based object was modified """
    refs = set()
    for field in obj.Schema().fields():
        if IReferenceableVocabulary.providedBy(field.vocabulary):
            accessor = field.getAccessor(obj)
            value = accessor()
            refs |= field.vocabulary.getObjectsSet(obj, value)
    updateReferences(obj, vocabularyRelationship, refs)
