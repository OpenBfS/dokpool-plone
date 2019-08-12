# -*- coding: utf-8 -*-
#
# File: dpapplication.py
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


class DPApplicationView(BrowserView):
    """Default view
    """

    __call__ = ViewPageTemplateFile('dpapplication.pt')
