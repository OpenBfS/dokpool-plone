# -*- coding: utf-8 -*-
#
"""Define a browser view for the content type. In the FTI
configured in profiles/default/types/*.xml, this is being set as the default
view of that content type.
"""


from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class DPEventsView(BrowserView):
    """Default view
    """

    __call__ = ViewPageTemplateFile('dpevents.pt')
