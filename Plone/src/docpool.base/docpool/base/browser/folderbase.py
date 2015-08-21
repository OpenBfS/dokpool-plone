# -*- coding: utf-8 -*-
#
# File: folderbase.py
#
# Copyright (c) 2015 by Condat AG
# Generator: ConPD2
#            http://www.condat.de
#

"""Define a browser view for the content type. In the FTI 
configured in profiles/default/types/*.xml, this is being set as the default
view of that content type.
"""


from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone.memoize.instance import memoize

##code-section imports
from Acquisition import aq_inner
from docpool.base.content.dpdocument import IDPDocument
from docpool.base.content.folderbase import IFolderBase
from docpool.base.content.infolink import IInfoLink
from Products.CMFCore.utils import getToolByName
from plone.app.content.browser.contents import FolderContentsView, TUS_ENABLED
from plone.app.content.browser.interfaces import IFolderContentsView
from zope.interface import implementer
##/code-section imports

@implementer(IFolderContentsView)
class FolderBaseView(BrowserView):
    """Default view
    """
    
    ##code-section methods1
    def dp_buttons(self, items):
        """
        Determine the available buttons by calling the original method from the 
        folder_contents view. We only accept cut & paste, though.
        """
        res = []
        for b in self.buttons(items):
            if (b['id'] in ['cut','paste']):
                res.append(b)
        return res
    
    def buttons(self, items):
        buttons = []
        context = aq_inner(self.context)
        portal_actions = getToolByName(context, 'portal_actions')
        button_actions = portal_actions.listActionInfos(object=context, categories=('folder_buttons', ))

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
            if button['id'] != 'paste' or context.cb_dataValid():
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
        # print "getFolderContents"
        kwargs["object_provides"] = IFolderBase.__identifier__
        res = [ b for b in self.context.getFolderContents(kwargs)]
        # print res
        kwargs["object_provides"] = [IDPDocument.__identifier__, IInfoLink.__identifier__]
        res.extend([b for b in self.context.getFolderContents(kwargs)])
        # print res
        return res
    ##/code-section methods1     

class FolderBaselistitemView(BrowserView):
    """Additional View
    """
    
    __call__ = ViewPageTemplateFile('folderbaselistitem.pt')
    
    ##code-section methodslistitem
    ##/code-section methodslistitem     

class FolderBaserpopupView(BrowserView):
    """Additional View
    """
    
    __call__ = ViewPageTemplateFile('folderbaserpopup.pt')
    
    ##code-section methodsrpopup
    ##/code-section methodsrpopup     



##code-section bottom
##/code-section bottom