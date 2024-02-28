from docpool.base.content.doctype import IDocType  # noqa: F401
from docpool.base.content.documentpool import IDocumentPool  # noqa: F401
from docpool.base.content.dpdocument import IDPDocument  # noqa: F401
from docpool.base.content.folderbase import IFolderBase  # noqa: F401
from docpool.base.content.infodocument import IInfoDocument  # noqa: F401
from docpool.base.content.infolink import IInfoLink  # noqa: F401
from plone.supermodel import model
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class IDocpoolBaseLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IExtension(model.Schema):
    """
    Marker for extension behaviors
    """


class IDocumentExtension(IExtension):
    """
    Marker for behaviors for document extensions
    """


class IDocTypeExtension(IExtension):
    """
    Marker for behaviors for doc type extensions
    """
