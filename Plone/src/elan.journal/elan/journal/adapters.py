"""Adapt a Journal with a container of journal-entries.

"""
from datetime import datetime
from elan.journal.interfaces import IJournal
from persistent import Persistent
from persistent.list import PersistentList
from plone import api
from time import time
from zope.annotation.interfaces import IAnnotations
from zope.component import adapter
from zope.container.contained import ObjectAddedEvent
from zope.container.contained import ObjectRemovedEvent
from zope.event import notify
from zope.interface import Attribute
from zope.interface import implementer
from zope.interface import Interface


class IJournalEntryContainer(Interface):
    pass


class IJournalEntry(Interface):

    """An entry to a Journal."""

    creator = Attribute("Id of user creating the journalentry.")
    created = Attribute("Date and time when this journalentry was created.")
    modified = Attribute("Date and time when this journalentry was modified.")
    timestamp = Attribute("Timestamp of the journalentry.")
    title = Attribute("Title of the jounalentry.")
    text = Attribute("Text of the journalentry.")


@implementer(IJournalEntryContainer)
@adapter(IJournal)
class JournalEntryContainer(Persistent):

    ANNO_KEY = "journal.journalentries"

    def __init__(self, context):
        self.context = context
        annotations = IAnnotations(self.context)
        self.__mapping = annotations.get(self.ANNO_KEY, None)
        if self.__mapping is None:
            self.__mapping = PersistentList()
            annotations[self.ANNO_KEY] = self.__mapping

    def __contains__(self, key):
        return key in self.__mapping

    def __getitem__(self, i):
        i = int(i)
        return self.__mapping.__getitem__(i)

    def __delitem__(self, item):
        self.__mapping.__delitem__(item)

    def __len__(self):
        return self.__mapping.__len__()

    def __setitem__(self, i, y):
        self.__mapping.__setitem__(i, y)

    def append(self, item):
        self.__mapping.append(item)

    def remove(self, id):
        id = int(id)
        self[id] = None

    def add(self, item):
        self.append(item)
        id = str(len(self))
        event = ObjectAddedEvent(item, newParent=self.context, newName=id)
        notify(event)

    def delete(self, id):
        event = ObjectRemovedEvent(self[id], oldParent=self.context, oldName=id)
        self.remove(id)
        notify(event)


@implementer(IJournalEntry)
class JournalEntry(Persistent):
    """An entry to a Journal."""

    def __init__(self, title, text):
        self.__parent__ = self.__name__ = None
        self.creator = api.user.get_current().id
        self.modified = self.created = datetime.now()
        self.timestamp = str(time())
        self.title = title
        self.text = text
