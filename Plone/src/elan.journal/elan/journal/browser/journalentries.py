# -*- coding: utf-8 -*-
from elan.journal import _
from elan.journal.adapters import IJournalEntryContainer
from elan.journal.adapters import JournalEntry
from elan.journal.browser.base import BaseView
from datetime import datetime
from plone import api
from Products.Five.browser import BrowserView
from time import time
from zExceptions import NotFound
from zope.event import notify
from zope.interface import implementer
from zope.lifecycleevent import ObjectModifiedEvent
from zope.publisher.interfaces import IPublishTraverse
from plone.protect.interfaces import IDisableCSRFProtection
from zope.interface import alsoProvides


@implementer(IPublishTraverse)
class JournalEntryView(BrowserView, BaseView):

    """Default view for a Journal's entry."""

    def __init__(self, context, request):
        # do not allow accessing the view without a timestamp
        if len(request.path) == 0:
            request.RESPONSE.setStatus(400)
        super(JournalEntryView, self).__init__(context, request)

    def __call__(self):
        # return an empty page on Bad Request
        if self.request.RESPONSE.getStatus() == 400:
            return ''
        return self.index()

    def publishTraverse(self, request, timestamp):
        """Get the selected journalentry."""
        journalentries = self.context.get_journalentries()
        update = [u for u in journalentries if u['timestamp'] == timestamp]
        assert len(update) in (0, 1)
        if len(update) == 0:
            raise NotFound

        self.update = update[0]
        return self


class BaseJournalEntryView(BrowserView):

    """Base view with helper methods for journal-entries."""

    def _redirect_with_status_message(self, msg, type='info'):
        api.portal.show_message(msg, self.request, type=type)
        update_url = self.context.absolute_url() + '/update'
        self.request.response.redirect(update_url)

    def _validate_journalentry_id(self):
        """Validate the journalentry id for the request."""
        id = self.request.form.get('id', None)
        if id is None:
            msg = _(u'No entry selected.')
            api.portal.show_message(msg, self.request, type='error')
            return False
        else:
            try:
                id = int(id)
            except ValueError:
                msg = _(u'Journalentry id is not an integer.')
                api.portal.show_message(msg, self.request, type='error')
                return False
            adapter = IJournalEntryContainer(self.context)
            if id >= len(adapter):
                msg = _(u'Journalentry id does not exist.')
                api.portal.show_message(msg, self.request, type='error')
                return False
        return True


class AddJournalEntryView(BaseJournalEntryView):

    """Add an entry to the Journal."""

    def __call__(self):
        return self.render()

    def render(self):
        title = self.request.form.get('title', '')
        text = self.request.form.get('text', None)

        if text is None:  # something went wrong
            msg = _(u'Required text input is missing.')
            self._redirect_with_status_message(msg, type='error')
            return

        adapter = IJournalEntryContainer(self.context)
        adapter.add(JournalEntry(title, text))
        # XXX: why do we need to handle this again here?
        #      we're already firing an event on the adapter
        # notify the Journal has a new entry
        notify(ObjectModifiedEvent(self.context))
        msg = _(u'Item published.')
        self._redirect_with_status_message(msg)


class EditJournalEntryView(BaseJournalEntryView):

    """Edit an entry in the Journal."""

    def __call__(self):

        if 'form.buttons.save' in self.request.form:  # Save changes
            return self.save()

        if 'form.buttons.cancel' in self.request.form:  # Cancel edit?
            return self.cancel()

        if self._validate_journalentry_id():
            return self.render()

    def render(self):
        id = self.request.form.get('id')
        adapter = IJournalEntryContainer(self.context)
        self._title = adapter[id].title
        self._text = adapter[id].text
        return self.index()

    def save(self):
        if self._validate_journalentry_id():
            id = self.request.form.get('id')
            title = self.request.form.get('title', '')
            text = self.request.form.get('text', None)

            if text is None:  # something went wrong
                msg = _(u'Required text input is missing.')
                self._redirect_with_status_message(msg, type='error')
                return

            # save the changes and return
            adapter = IJournalEntryContainer(self.context)
            adapter[id].title = title
            adapter[id].text = text
            adapter[id].modified = datetime.now()
            notify(ObjectModifiedEvent(self.context))
            # schedule a hard refresh
            self.context._last_journalentry_edition = str(time())
            msg = _(u'Item saved.')
            self._redirect_with_status_message(msg)

    def cancel(self):
        msg = _(u'Edit cancelled.')
        self._redirect_with_status_message(msg)

    @property
    def title(self):
        return self._title

    @property
    def text(self):
        return self._text


class DeleteJournalEntryView(BaseJournalEntryView):

    """Delete an entry from the Journal."""

    def __call__(self):
        if self._validate_journalentry_id():
            return self.render()

    def render(self):
        alsoProvides(self.request, IDisableCSRFProtection)
        id = self.request.form.get('id', None)
        adapter = IJournalEntryContainer(self.context)
        adapter.delete(id)
        # XXX: why do we need to handle this again here?
        #      we're already firing an event on the adapter
        notify(ObjectModifiedEvent(self.context))
        # schedule a hard refresh
        self.context._last_journalentry_deletion = str(time())
        msg = _(u'Item deleted.')
        self._redirect_with_status_message(msg)
