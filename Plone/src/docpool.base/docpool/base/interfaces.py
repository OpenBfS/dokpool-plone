from zope.interface import Interface, Attribute
from docpool.base.content.infofolder import IInfoFolder
from docpool.base.content.infodocument import IInfoDocument
from docpool.base.content.infolink import IInfoLink
from docpool.base.content.extendable import IExtendable
from docpool.base.content.dpdocument import IDPDocument
from docpool.base.content.doctype import IDocType
from docpool.base.content.simplefolder import ISimpleFolder
from docpool.base.content.contentbase import IContentBase
from docpool.base.content.doctypes import IDocTypes
from docpool.base.content.text import IText
from docpool.base.content.folderbase import IFolderBase
from docpool.base.content.groupfolder import IGroupFolder
from docpool.base.content.userfolder import IUserFolder
from docpool.base.content.groups import IGroups
from docpool.base.content.users import IUsers
from docpool.base.content.reviewfolder import IReviewFolder
from docpool.base.content.collaborationfolder import ICollaborationFolder
from docpool.base.content.privatefolder import IPrivateFolder
from docpool.base.content.documentpool import IDocumentPool
from docpool.base.content.contentarea import IContentArea
from docpool.base.content.dpapplication import IDPApplication
from docpool.base.content.dpconfig import IDPConfig
from plone.supermodel import model


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
