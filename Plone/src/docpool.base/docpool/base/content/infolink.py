#
# File: infolink.py
#
# Copyright (c) 2016 by Bundesamt für Strahlenschutz
# Generator: ConPD2
#            http://www.condat.de
#

__author__ = ""
__docformat__ = "plaintext"

"""Definition of the InfoLink content type. See infolink.py for more
explanation on the statements below.
"""
from docpool.base.content.contentbase import ContentBase
from plone.app.contenttypes.content import ILink, Link
from plone.dexterity.content import Item
from plone.supermodel import model
from zope import schema
from zope.interface import implementer


class IInfoLink(model.Schema, ILink):
    """ """

    remoteUrl = schema.TextLine(title="URL", default="http://")


@implementer(IInfoLink)
class InfoLink(ContentBase, Link):
    """ """
