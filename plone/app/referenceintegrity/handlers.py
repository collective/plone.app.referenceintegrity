from Acquisition import aq_get
from Products.Archetypes.interfaces import IReference

from plone.app.linkintegrity.interfaces import ILinkIntegrityInfo
from plone.app.referenceintegrity.config import get_protected_relationships


def referenceRemoved(obj, event):
    """ store information about the removed link integrity reference """
    assert IReference.providedBy(obj)
    assert obj is event.object          # just making sure...
    if not obj.relationship in get_protected_relationships():
        return                          # skip for other removed references
    # if the object the event was fired on doesn't have a `REQUEST` attribute
    # we can safely assume no direct user action was involved and therefore
    # never raise a link integrity exception...
    request = aq_get(obj, 'REQUEST', None)
    if not request:
        return
    storage = ILinkIntegrityInfo(request)
    breaches = storage.getIntegrityBreaches()
    breaches.setdefault(obj.getTargetObject(),
        set()).add(obj.getSourceObject())
    storage.setIntegrityBreaches(breaches)
