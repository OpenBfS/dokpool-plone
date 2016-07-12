# -*- coding: utf-8 -*-
#
# File: dpdocument.py
#
# Copyright (c) 2015 by Condat AG
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

##code-section imports
from Acquisition import aq_inner, aq_base, ImplicitAcquisitionWrapper
import urllib
from plone.app.layout.globals.interfaces import IViewView
from zope.interface import implements
from zope.interface import alsoProvides
from plone.protect.authenticator import createToken
from Products.Archetypes.utils import shasattr, contentDispositionHeader
from plone.protect.interfaces import IDisableCSRFProtection
from docpool.base.utils import execute_under_special_role
from docpool.base.content.dpdocument import DPDocument
from plone.app.content.browser.file import FileUploadView as BaseFileUploadView
import json
from plone.app.dexterity.interfaces import IDXFileFactory
from plone.uuid.interfaces import IUUID
import mimetypes
from plone import api
##/code-section imports



class DocMetaView(BrowserView):
    """Default view
    """
 
    __call__ = ViewPageTemplateFile('doc_meta.pt')
   
    ##code-section methods1
    ##/code-section methods1


class DocActionsView(BrowserView):
    """Default view
    """

    __call__ = ViewPageTemplateFile('doc_actions.pt')

    ##code-section methods1
    ##/code-section methods1
