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
from zope.interface import implements
from zope.component import adapts
from zope import schema
from plone.directives import form, dexterity
from plone.app.textfield import RichText
from plone.namedfile.field import NamedBlobImage
from collective import dexteritytextindexer
from z3c.relationfield.schema import RelationChoice, RelationList
from plone.formwidget.contenttree import ObjPathSourceBinder
from Products.CMFPlone.utils import log, log_exc

from plone.dexterity.content import Item
from plone.app.contenttypes.content import Link, ILink

from Products.CMFCore.utils import getToolByName


from docpool.base.config import PROJECTNAME

from docpool.base import DocpoolMessageFactory as _


class IInfoLink(form.Schema, ILink):
    """
    """

    remoteUrl = schema.TextLine(title=u"URL", default=u"http://")


class InfoLink(Item, Link):
    """
    """

    security = ClassSecurityInfo()

    implements(IInfoLink)
