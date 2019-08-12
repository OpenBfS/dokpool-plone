# -*- coding: utf-8 -*-
#
# File: documentpool.py
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

from docpool.base.utils import execute_under_special_role
from Products.CMFPlone.log import log_exc
from Products.CMFCore.utils import getToolByName
from plone.subrequest import subrequest


class DocumentPoolView(BrowserView):
    """Default view
    """

    __call__ = ViewPageTemplateFile('documentpool.pt')


class HelpView(BrowserView):
    """Default view
    """

    __call__ = ViewPageTemplateFile('help.pt')


class HelpHelper(BrowserView):
    def __call__(self):
        """
        """

        def getHTML():
            urltool = getToolByName(self.context, "portal_url")
            portal = urltool.getPortalObject()
            view = portal.unrestrictedTraverse('contentconfig/help/@@view')
            return view()

        return execute_under_special_role(self.context, "Manager", getHTML)
