# -*- coding: utf-8 -*-
#
# File: text.py
#
# Copyright (c) 2016 by Bundesamt für Strahlenschutz
# Generator: ConPD2
#            http://www.condat.de
#

__author__ = ''
__docformat__ = 'plaintext'

"""Definition of the Text content type. See text.py for more
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
from docpool.base.content.contentbase import ContentBase, IContentBase

from Products.CMFCore.utils import getToolByName


from docpool.base.config import PROJECTNAME

from docpool.base import DocpoolMessageFactory as _


class IText(form.Schema, IContentBase):
    """
    """

    dexteritytextindexer.searchable('text')
    text = RichText(
        title=_(u'label_text_text', default=u'Text'),
        description=_(u'description_text_text', default=u''),
        required=False,
    )


class Text(Item, ContentBase):
    """
    """

    security = ClassSecurityInfo()

    implements(IText)
