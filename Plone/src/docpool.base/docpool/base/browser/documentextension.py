# -*- coding: utf-8 -*-
#
# File: dpdocument.py
#
# Copyright (c) 2015 by Bundesamt für Strahlenschutz
# Generator: ConPD2
#            http://www.condat.de
#

"""Define a browser view for the content type. In the FTI
configured in profiles/default/types/*.xml, this is being set as the default
view of that content type.
"""


from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class DocMetaView(BrowserView):
    """Default view
    """

    __call__ = ViewPageTemplateFile('doc_meta.pt')


class DocActionsView(BrowserView):
    """Default view
    """

    __call__ = ViewPageTemplateFile('doc_actions.pt')
