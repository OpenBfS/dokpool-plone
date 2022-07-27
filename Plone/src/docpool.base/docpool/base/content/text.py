#
# File: text.py
#
# Copyright (c) 2016 by Bundesamt für Strahlenschutz
# Generator: ConPD2
#            http://www.condat.de
#

__author__ = ""
__docformat__ = "plaintext"

"""Definition of the Text content type. See text.py for more
explanation on the statements below.
"""
from AccessControl import ClassSecurityInfo
from docpool.base import DocpoolMessageFactory as _
from docpool.base.content.contentbase import ContentBase, IContentBase
from plone.app.dexterity.textindexer.directives import searchable
from plone.app.textfield import RichText
from plone.dexterity.content import Item
from zope.interface import implementer


class IText(IContentBase):
    """ """

    searchable("text")
    text = RichText(
        title=_("label_text_text", default="Text"),
        description=_("description_text_text", default=""),
        required=False,
    )


@implementer(IText)
class Text(Item, ContentBase):
    """ """

    security = ClassSecurityInfo()
