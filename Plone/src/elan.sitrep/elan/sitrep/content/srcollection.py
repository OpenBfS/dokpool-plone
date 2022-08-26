#
# File: srcollection.py
#
# Copyright (c) 2017 by Condat AG
# Generator: ConPD2
#            http://www.condat.de
#

__author__ = ""
__docformat__ = "plaintext"

"""Definition of the SRCollection content type. See srcollection.py for more
explanation on the statements below.
"""
from AccessControl import ClassSecurityInfo
from elan.esd.content.elandoccollection import ELANDocCollection
from elan.esd.content.elandoccollection import IELANDocCollection
from plone.supermodel import model
from zope.interface import implementer


class ISRCollection(model.Schema, IELANDocCollection):
    """ """


@implementer(ISRCollection)
class SRCollection(ELANDocCollection):
    """ """

    security = ClassSecurityInfo()
