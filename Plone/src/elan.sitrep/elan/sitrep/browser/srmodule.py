# -*- coding: utf-8 -*-
#
# File: srmodule.py
#
# Copyright (c) 2017 by Condat AG
# Generator: ConPD2
#            http://www.condat.de
#

"""Define a browser view for the content type. In the FTI
configured in profiles/default/types/*.xml, this is being set as the default
view of that content type.
"""


from docpool.elan.config import ELAN_APP
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class SRModuleView(BrowserView):
    """Default view
    """

    __call__ = ViewPageTemplateFile('srmodule.pt')

    def elanobject(self):
        return self.context.doc_extension(ELAN_APP)


class SRModulematerialView(BrowserView):
    """Additional View
    """

    __call__ = ViewPageTemplateFile('srmodulematerial.pt')

    def elanobject(self):
        return self.context.doc_extension(ELAN_APP)


class SRModuleinfoView(BrowserView):
    """Additional View
    """

    __call__ = ViewPageTemplateFile('srmoduleinfo.pt')

    def elanobject(self):
        return self.context.doc_extension(ELAN_APP)
