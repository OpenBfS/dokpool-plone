# -*- coding: utf-8 -*-
#
# File: dptransferfolder.py
#
# Copyright (c) 2014 by Bundesamt für Strahlenschutz
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

from docpool.dbaccess.dbinit import __session__, __metadata__
from formalchemy import Grid
from docpool.transfers.db.model import ChannelPermissions, DocTypePermission
from docpool.transfers import DocpoolMessageFactory as _
from docpool.base.browser.folderbase import FolderBaseView

class DPTransferFolderView(FolderBaseView):
    """Default view
    """

    __call__ = ViewPageTemplateFile('dptransferfolder.pt')
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


