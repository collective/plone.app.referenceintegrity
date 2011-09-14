from zope.interface import Interface
from zope.schema import List
from zope.schema import TextLine

from Products.Archetypes.interfaces import IVocabulary


class ISettings(Interface):

    reference_types = List(
        title=u"Reference types",
        description=u"Reference types that should be protected",
        required=False,
        value_type=TextLine())


class IReferenceableVocabulary(IVocabulary):
    """vocabulary used in referenceintegrity"""

    def getObjectsSet(content_instance, values):
        """returns the set of objects corresponding to the values"""
