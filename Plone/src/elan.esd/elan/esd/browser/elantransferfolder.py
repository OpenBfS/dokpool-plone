# -*- coding: utf-8 -*-
#
# File: elantransferfolder.py
#
# Copyright (c) 2014 by Condat AG
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
from docpool.dbaccess.dbinit import __session__, __metadata__
from formalchemy import Grid
from elan.esd.db.model import ChannelPermissions, DocTypePermission
from elan.esd import DocpoolMessageFactory as _
from docpool.base.browser.folderbase import FolderBaseView
##/code-section imports

class ELANTransferFolderView(FolderBaseView):
    """Default view
    """
 
    __call__ = ViewPageTemplateFile('elantransferfolder.pt')
   
    ##code-section methods1
    def gridHTML(self):
        """
        """
        g = Grid(DocTypePermission, session=__session__)
        g.configure(include=[g.doc_type.label(_(u"Document Type")).readonly(),g.perm.label(_("Permission"))])
        permissions = self.context.permissions()
        #permissions = DocTypePermission.query.all()
        # print len(permissions)
        g = g.bind(permissions)
        # print g.render()
        return g.render()
    ##/code-section methods1     



##code-section bottom
##/code-section bottom