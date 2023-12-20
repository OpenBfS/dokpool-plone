from docpool.base.content.contentbase import ContentBase
from plone.app.contenttypes.content import ILink
from plone.app.contenttypes.content import Link
from plone.supermodel import model
from zope import schema
from zope.interface import implementer


class IInfoLink(model.Schema, ILink):
    """ """

    remoteUrl = schema.TextLine(title="URL", default="http://")


@implementer(IInfoLink)
class InfoLink(Link, ContentBase):
    """ """

    APP = "base"
