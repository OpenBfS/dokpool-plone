# -*- coding: utf-8 -*-
#
# File: folderbase.py
#
# Copyright (c) 2016 by Bundesamt für Strahlenschutz
# Generator: ConPD2
#            http://www.condat.de
#

"""Define a browser view for the content type. In the FTI
configured in profiles/default/types/*.xml, this is being set as the default
view of that content type.
"""


from Acquisition import aq_inner
from docpool.base.content.dpdocument import IDPDocument
from docpool.base.content.folderbase import IFolderBase
from docpool.base.content.infolink import IInfoLink
from docpool.base.utils import extendOptions
from plone import api
from plone.app.content.browser.interfaces import IFolderContentsView
from plone.app.contenttypes.interfaces import ICollection
from plone.memoize import view
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.interface import implementer


class FolderBaselistitemView(BrowserView):
    """Additional View
    """

    __call__ = ViewPageTemplateFile('folderbaselistitem.pt')

    def options(self):
        return extendOptions(self.context, self.request, {})


class FolderBaserpopupView(BrowserView):
    """Additional View
    """

    __call__ = ViewPageTemplateFile('folderbaserpopup.pt')


@implementer(IFolderContentsView)
class FolderBaseView(BrowserView):
    """Default view
    """

    def dp_buttons(self, items):
        """
        Determine the available buttons by calling the original method from the
        folder_contents view.
        """
        return self.buttons(items)

    def buttons(self, items):
        buttons = []
        context = aq_inner(self.context)
        portal_actions = getToolByName(context, 'portal_actions')
        button_actions = portal_actions.listActionInfos(
            object=context, categories=('folder_buttons',)
        )

        # Do not show buttons if there is no data, unless there is data to be
        # pasted
        if not len(items):
            if self.context.cb_dataValid():
                for button in button_actions:
                    if button['id'] == 'paste':
                        return [self.setbuttonclass(button)]
            else:
                return []

        for button in button_actions:
            # Make proper classes for our buttons
            buttons.append(self.setbuttonclass(button))
        return buttons

    def setbuttonclass(self, button):
        if button['id'] == 'paste':
            button['cssclass'] = 'standalone'
        else:
            button['cssclass'] = 'context'
        return button

    def getFolderContents(self, kwargs):
        """
        """
        contentlisting = self.context.restrictedTraverse('@@contentlisting')
        kwargs["object_provides"] = [
            IFolderBase.__identifier__,
            ICollection.__identifier__,
        ]
        res = [b for b in contentlisting(**kwargs)]
        apps = self.isFilteredBy()
        if apps:
            kwargs['apps_supported'] = apps[0]
        kwargs["object_provides"] = [
            IDPDocument.__identifier__,
            IInfoLink.__identifier__,
        ]
        res.extend([b for b in contentlisting(**kwargs)])
        return res

    @view.memoize
    def isFilteredBy(self):
        """

        @return:
        """
        user = api.user.get_current()
        res = user.getProperty("filter_active") or False
        if res:
            res = user.getProperty("apps") or []
        # print "filter_active ", res
        return res
