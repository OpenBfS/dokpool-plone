# -*- coding: utf-8 -*-
from elan.journal.adapters import IJournalEntryContainer
from elan.journal.interfaces import IJournal
from plone import api
from plone.dexterity.content import Container
from plone.protect.interfaces import IDisableCSRFProtection
from zope.interface import alsoProvides
from zope.interface import implementer


@implementer(IJournal)
class Journal(Container):

    """A journal is a blog post which is intended to provide a rolling
    textual coverage of an ongoing event.

    The _last_journalentry_edition and _last_journalentry_deletion attributes
    are used to detect if a hard refresh of the views is needed.
    """

    _last_journalentry_edition = '0.0'
    _last_journalentry_deletion = '0.0'

    def get_journalentries(self):
        """Return the list of journal-entries in the Journal in reverse order."""
        request = self.REQUEST
        alsoProvides(request, IDisableCSRFProtection)

        container = IJournalEntryContainer(self)
        updates = []
        for id, update in enumerate(container):
            if update is None:
                continue  # update has been removed

            # TODO: it would be better to initialize modified field as None
            if update.created == update.modified:
                modified = None
            else:
                modified = api.portal.get_localized_time(
                    update.modified, True
                )  # 28/08/2014 10h58

            updates.append(
                dict(
                    id=id,
                    creator=update.creator,
                    timestamp=update.timestamp,  # 1409223490.21,
                    datetime=api.portal.get_localized_time(
                        update.created, True
                    ),  # 28/08/2014 10h58
                    date=api.portal.get_localized_time(
                        update.created),  # 28/08/2014
                    time=api.portal.get_localized_time(
                        update.created, time_only=True
                    ),  # 10h58
                    isoformat=update.created.isoformat()[
                        :-3
                    ],  # 2014-08-28T10:58:10.209468
                    modified=modified,
                    title=update.title,
                    text=update.text,
                )
            )
        updates.reverse()  # show journal-entries in reverse order
        return updates
