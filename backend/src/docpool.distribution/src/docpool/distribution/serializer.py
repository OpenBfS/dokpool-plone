from copy import copy
from eea.facetednavigation.widgets.interfaces import ICriterion
from elan.journal.adapters import JournalEntry
from plone.restapi.interfaces import IJsonCompatible
from plone.restapi.serializer.converters import json_compatible
from zope.component import adapter
from zope.interface import implementer


@adapter(JournalEntry)
@implementer(IJsonCompatible)
def convert_journalentry(value):
    """creator, modified, created, timestamp, title, text"""
    data = copy(value.__dict__)
    data.pop("__name__", None)
    data.pop("__parent__", None)
    data["modified"] = json_compatible(data["modified"])
    data["created"] = json_compatible(data["created"])
    return data


@adapter(ICriterion)
@implementer(IJsonCompatible)
def convert_criterion(value):
    return value.__dict__
