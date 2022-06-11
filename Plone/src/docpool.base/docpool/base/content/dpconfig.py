#
# File: dpconfig.py
#
# Copyright (c) 2016 by Bundesamt für Strahlenschutz
# Generator: ConPD2
#            http://www.condat.de
#

__author__ = ''
__docformat__ = 'plaintext'

"""Definition of the DPConfig content type. See dpconfig.py for more
explanation on the statements below.
"""
from AccessControl import ClassSecurityInfo
from plone.dexterity.content import Container
from plone.supermodel import model
from zope.interface import implementer


class IDPConfig(model.Schema):
    """
    """


@implementer(IDPConfig)
class DPConfig(Container):
    """
    """

    security = ClassSecurityInfo()

    def myDPConfig(self):
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

    def getDocTypess(self, **kwargs):
        """
        """
        args = {'portal_type': 'DocTypes'}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)]
