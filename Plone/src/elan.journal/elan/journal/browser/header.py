# -*- coding: utf-8 -*-
from plone.app.layout.viewlets.common import ViewletBase


class Header(ViewletBase):

    """A viewlet to include a header in the Journal."""

    def available(self):
        """Check if the viewlet must be displayed; that is, if an image
        is been used and the context is not a journalentry.
        """
        is_journalentry = self.request['PARENTS'][0].__name__ == 'journalentry'
        try:
            image = self.context.image
        except:
            image = None

        return image is not None and not is_journalentry
