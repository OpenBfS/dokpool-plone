# -*- coding: utf-8 -*-
from elan.journal.adapters import IJournalEntryContainer
from elan.journal.adapters import JournalEntry
from time import sleep
from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent
from six.moves import range


def _create_journalentries(context, count):
    """Create 10 journal-entries. Note the use of the sleep method to avoid
    doing this so fast that we ended with the same timestamp on different
    updates."""
    adapter = IJournalEntryContainer(context)
    for index in range(1, count + 1):
        sleep(0.05)
        adapter.add(
            JournalEntry('', u'<p>This is demo journal entry {}</p>'.format(index)))

    # wait and update Journal modification time to invalidate the cache
    sleep(1)
    notify(ObjectModifiedEvent(context))
