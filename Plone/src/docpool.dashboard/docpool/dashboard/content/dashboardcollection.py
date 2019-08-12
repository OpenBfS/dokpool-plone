# -*- coding: utf-8 -*-
#
# File: dashboardcollection.py
#
# Copyright (c) 2016 by Bundesamt für Strahlenschutz
# Generator: ConPD2
#            http://www.condat.de
#

__author__ = ''
__docformat__ = 'plaintext'

"""Definition of the DashboardCollection content type. See dashboardcollection.py for more
explanation on the statements below.
"""
from AccessControl import ClassSecurityInfo
from elan.esd.content.elandoccollection import ELANDocCollection
from elan.esd.content.elandoccollection import IELANDocCollection
from plone.dexterity.content import Item
from plone.directives import form
from zope.interface import implements


class IDashboardCollection(form.Schema, IELANDocCollection):
    """
    """


class DashboardCollection(Item, ELANDocCollection):
    """
    """

    security = ClassSecurityInfo()

    implements(IDashboardCollection)
