#
# File: doctypeextension.py
#
# Copyright (c) 2016 by Bundesamt für Strahlenschutz
# Generator: ConPD2
#            http://www.condat.de
#

__author__ = ""
__docformat__ = "plaintext"

"""Definition of the DocTypeExtension content type. See doctypeextension.py for more
explanation on the statements below.
"""
from AccessControl import ClassSecurityInfo
from plone.dexterity.content import Item
from plone.supermodel import model
from zope.interface import implementer


class IDocTypeExtension(model.Schema):
    """ """


@implementer(IDocTypeExtension)
class DocTypeExtension(Item):
    """ """

    security = ClassSecurityInfo()
