# -*- coding: utf-8 -*-
#
# File: dpdocument.py
#
# Copyright (c) 2016 by Bundesamt für Strahlenschutz
# Generator: ConPD2
#            http://www.condat.de
#

"""Define a browser view for the content type. In the FTI
configured in profiles/default/types/*.xml, this is being set as the default
view of that content type.
"""


from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone.memoize.instance import memoize

from docpool.base.browser.flexible_view import FlexibleView


class DPDocumentdashboardView(FlexibleView):
    """Additional View
    """

    __allow_access_to_unprotected_subobjects__ = 1
    __call__ = ViewPageTemplateFile('dpdocumentdashboard.pt')
