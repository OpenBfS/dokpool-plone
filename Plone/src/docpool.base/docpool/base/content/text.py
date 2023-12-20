from docpool.base import DocpoolMessageFactory as _
from docpool.base.content.contentbase import ContentBase
from docpool.base.content.contentbase import IContentBase
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

    APP = "base"
