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
from collective import dexteritytextindexer
from docpool.base import DocpoolMessageFactory as _
from docpool.base.content.contentbase import ContentBase
from docpool.base.content.contentbase import IContentBase
from plone.app.textfield import RichText
from plone.dexterity.content import Item
from plone.directives import form
from zope.interface import implementer


class IText(form.Schema, IContentBase):
    """
    """

    dexteritytextindexer.searchable('text')
    text = RichText(
        title=_(u'label_text_text', default=u'Text'),
        description=_(u'description_text_text', default=u''),
        required=False,
    )


@implementer(IText)
class Text(Item, ContentBase):
    """
    """

    security = ClassSecurityInfo()
