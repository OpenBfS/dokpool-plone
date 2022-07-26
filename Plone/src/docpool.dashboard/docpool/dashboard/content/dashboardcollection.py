#
# File: dashboardcollection.py
#
# Copyright (c) 2016 by Bundesamt für Strahlenschutz
# Generator: ConPD2
#            http://www.condat.de
#

__author__ = ""
__docformat__ = "plaintext"

"""Definition of the DashboardCollection content type. See dashboardcollection.py for more
explanation on the statements below.
"""
from AccessControl import ClassSecurityInfo
from elan.esd.content.elandoccollection import ELANDocCollection, IELANDocCollection
from plone.supermodel import model
from zope.interface import implementer


class IDashboardCollection(model.Schema, IELANDocCollection):
    """ """


@implementer(IDashboardCollection)
class DashboardCollection(ELANDocCollection):
    """ """

    security = ClassSecurityInfo()
