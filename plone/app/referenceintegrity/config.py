from zope.component import queryUtility
from zope.component import getUtility

from plone.registry.interfaces import IRegistry

from plone.app.referenceintegrity.interfaces import ISettings


def get_protected_relationships():
    registry = queryUtility(IRegistry)
    if registry is None:
        return []
    settings = registry.forInterface(ISettings, check=False)
    return settings.reference_types


def set_protected_relationships(reference_types):
    registry = getUtility(IRegistry)
    settings = registry.forInterface(ISettings, check=False)
    encoded = [ref_type if isinstance(ref_type, unicode)
            else unicode(ref_type, 'utf8')
            for ref_type in reference_types]
    settings.reference_types = encoded


class DisabledProtection(object):

    def __init__(self, reference_types):
        self.reference_types = reference_types

    def __enter__(self):
        self.existing = get_protected_relationships()
        updated = set(self.existing) - set(self.reference_types)
        set_protected_relationships(list(updated))

    def __exit__(self, exc_type, exc_val, exc_tb):
        set_protected_relationships(self.existing)
        return False
