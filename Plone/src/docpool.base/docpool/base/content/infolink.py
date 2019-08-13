# -*- coding: utf-8 -*-
#
# File: infolink.py
#
# Copyright (c) 2016 by Bundesamt für Strahlenschutz
# Generator: ConPD2
#            http://www.condat.de
#

__author__ = ''
__docformat__ = 'plaintext'

"""Definition of the InfoLink content type. See infolink.py for more
explanation on the statements below.
"""
from AccessControl import ClassSecurityInfo
from plone.app.contenttypes.content import ILink
from plone.app.contenttypes.content import Link
from plone.dexterity.content import Item
from plone.supermodel import model
from zope import schema
from zope.interface import implementer


class IInfoLink(model.Schema, ILink):
    """
    """

    remoteUrl = schema.TextLine(title=u"URL", default=u"http://")


@implementer(IInfoLink)
class InfoLink(Item, Link):
    """
    """

    security = ClassSecurityInfo()
