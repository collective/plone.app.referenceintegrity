from zope.component import getUtility
from plone.registry.interfaces import IRegistry

from Acquisition import aq_get
from Products.Archetypes.interfaces import IReference
from plone.app.linkintegrity.exceptions import (
    LinkIntegrityNotificationException)
from plone.app.linkintegrity.interfaces import ILinkIntegrityInfo
from plone.app.referenceintegrity.interfaces import ISettings


def get_protected_relationships():
    registry = getUtility(IRegistry)
    settings = registry.forInterface(ISettings, check=False)
    return settings.reference_types


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


def referencedObjectRemoved(obj, event):
    """ check if the removal was already confirmed or redirect to the form """
    # if the object the event was fired on doesn't have a `REQUEST` attribute
    # we can safely assume no direct user action was involved and therefore
    # never raise a link integrity exception...
    request = aq_get(obj, 'REQUEST', None)
    if not request:
        return
    info = ILinkIntegrityInfo(request)
    # first we check if link integrity checking was enabled
    if not info.integrityCheckingEnabled():
        return

    # since the event gets called for every subobject before it's
    # called for the item deleted directly via _delObject (event.object)
    # itself, but we do not want to present the user with a confirmation
    # form for every (referred) subobject, so we remember and skip them...
    info.addDeletedItem(obj)
    if obj is not event.object:
        return

    # if the number of expected events has been stored to help us prevent
    # multiple forms (i.e. in folder_delete), we wait for the next event
    # if we know there will be another...
    if info.moreEventsToExpect():
        return

    # at this point all subobjects have been removed already, so all
    # link integrity breaches caused by that have been collected as well;
    # if there aren't any (after things have been cleaned up),
    # we keep lurking in the shadows...
    if not info.getIntegrityBreaches():
        return

    # if the user has confirmed to remove the currently handled item in a
    # previous confirmation form we won't need it anymore this time around...
    if info.isConfirmedItem(obj):
        return

    # otherwise we raise an exception and pass the object that is supposed
    # to be removed as the exception value so we can use it as the context
    # for the view triggered by the exception;  this is needed since the
    # view is an adapter for the exception and a request, so it gets the
    # exception object as the context, which is not very useful...
    raise LinkIntegrityNotificationException(obj)
