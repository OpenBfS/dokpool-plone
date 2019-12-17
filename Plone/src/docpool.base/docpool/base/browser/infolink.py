# -*- coding: utf-8 -*-
#
# File: infolink.py
#
# Copyright (c) 2016 by Bundesamt für Strahlenschutz
# Generator: ConPD2
#            http://www.condat.de
#

"""Define a browser view for the content type. In the FTI
configured in profiles/default/types/*.xml, this is being set as the default
view of that content type.
"""


from docpool.base.utils import extendOptions
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class InfoLinklistitemView(BrowserView):
    """Additional View
    """

    __call__ = ViewPageTemplateFile('infolinklistitem.pt')

    def options(self):
        return extendOptions(self.context, self.request, {})
