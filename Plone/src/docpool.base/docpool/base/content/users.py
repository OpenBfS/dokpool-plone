# -*- coding: utf-8 -*-
#
# File: users.py
#
# Copyright (c) 2016 by Bundesamt für Strahlenschutz
# Generator: ConPD2
#            http://www.condat.de
#

__author__ = ''
__docformat__ = 'plaintext'

"""Definition of the Users content type. See users.py for more
explanation on the statements below.
"""
from AccessControl import ClassSecurityInfo
from plone.dexterity.content import Container
from plone.supermodel import model
from zope.interface import implementer


class IUsers(model.Schema):
    """
    """


@implementer(IUsers)
class Users(Container):
    """
    """

    security = ClassSecurityInfo()

    def myUsers(self):
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

    def getUserFolders(self, **kwargs):
        """
        """
        args = {'portal_type': 'UserFolder'}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)]
