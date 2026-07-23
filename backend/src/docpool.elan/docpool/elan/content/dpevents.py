from docpool.base.content.places import IPlaces
from docpool.elan import DocpoolMessageFactory as _
from docpool.elan.config import ELAN_APP
from logging import getLogger
from persistent.list import PersistentList
from plone import api
from plone.autoform import directives
from plone.dexterity.content import Container
from plone.supermodel import model
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from zope import schema
from zope.interface import implementer


logger = getLogger("dpevents")


class IDPEvents(model.Schema):
    """ """

    subscribed_events = schema.List(
        title=_("List of UIDs of events this Docpool subscribed to"),
        value_type=schema.Choice(source="docpool.elan.vocabularies.OpenEvents"),
    )
    directives.widget(subscribed_events=CheckBoxFieldWidget)


@implementer(IDPEvents)
class DPEvents(Container):
    """ """

    APP = ELAN_APP

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.subscribed_events = PersistentList()

    def getDPEvents(self):
        """ """
        events_by_uid = global_events_by_uid()
        if IPlaces(self).document_pool is None:
            events = events_by_uid.values()
        else:
            events = (event for uid in self.subscribed_events if (event := events_by_uid.get(uid)))
        return sorted(
            events,
            key=lambda event: event.modified(),
            reverse=True,
        )


def global_events_folder():
    return api.portal.get()["contentconfig"]["events"]


def global_events_by_uid():
    # This is used in an indexer, so we must not query events using the catalog, else index rebuilds might
    # break. But then, there's no reason to use the catalog in the first place.
    dpevents = global_events_folder()
    return {event.UID(): event for event in dpevents.contentValues({"portal_type": "DPEvent"})}
