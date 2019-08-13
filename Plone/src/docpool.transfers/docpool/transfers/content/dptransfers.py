# -*- coding: utf-8 -*-
#
# File: dptransfers.py
#
# Copyright (c) 2016 by Bundesamt für Strahlenschutz
# Generator: ConPD2
#            http://www.condat.de
#

__author__ = ''
__docformat__ = 'plaintext'

"""Definition of the DPTransfers content type. See dptransfers.py for more
explanation on the statements below.
"""
from AccessControl import ClassSecurityInfo
from logging import getLogger
from plone.dexterity.content import Container
from plone.supermodel import model
from Products.CMFPlone.utils import parent
from zope.interface import implementer


logger = getLogger("dptransfers")


class IDPTransfers(model.Schema):
    """
    """


@implementer(IDPTransfers)
class DPTransfers(Container):
    """
    """

    security = ClassSecurityInfo()

    def migrate(self):
        f = parent(self)
        if hasattr(self, '_setPortalTypeName'):
            self._setPortalTypeName("DPTransfers")
        myid = self.getId()
        del f[myid]
        self.__class__ = DPTransfers
        f[myid] = self
        logger.info(self.__class__)
        logger.info(self.getPortalTypeName())

    def myDPTransfers(self):
        """
        """
        return self

    def getFirstChild(self):
        """
        """
        fc = self.getFolderContents()
        if len(fc) > 0:
            return fc[0].getObject()
        else:
            return None

    def getAllContentObjects(self):
        """
        """
        return [obj.getObject() for obj in self.getFolderContents()]

    def getDPTransferFolders(self, **kwargs):
        """
        """
        args = {'portal_type': 'DPTransferFolder'}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)]


class ELANTransfers(DPTransfers):
    pass
