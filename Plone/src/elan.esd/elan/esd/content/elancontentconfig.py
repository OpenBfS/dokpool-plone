# -*- coding: utf-8 -*-
#
# File: elancontentconfig.py
#
# Copyright (c) 2016 by Bundesamt für Strahlenschutz
# Generator: ConPD2
#            http://www.condat.de
#

__author__ = ''
__docformat__ = 'plaintext'

"""Definition of the ELANContentConfig content type. See elancontentconfig.py for more
explanation on the statements below.
"""
from AccessControl import ClassSecurityInfo
from docpool.elan.config import ELAN_APP
from plone.dexterity.content import Container
from plone.supermodel import model
from zope.interface import implementer


class IELANContentConfig(model.Schema):
    """
    """


@implementer(IELANContentConfig)
class ELANContentConfig(Container):
    """
    """

    security = ClassSecurityInfo()

    APP = ELAN_APP

    def myELANContentConfig(self):
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

    def getDPEvents(self, **kwargs):
        """
        """
        args = {'portal_type': 'DPEvents'}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)]

    def getTexts(self, **kwargs):
        """
        """
        args = {'portal_type': 'Text'}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)]
