# -*- coding: utf-8 -*-
#
# File: simplefolder.py
#
# Copyright (c) 2016 by Bundesamt für Strahlenschutz
# Generator: ConPD2
#            http://www.condat.de
#

__author__ = ''
__docformat__ = 'plaintext'

"""Definition of the SimpleFolder content type. See simplefolder.py for more
explanation on the statements below.
"""
from AccessControl import ClassSecurityInfo
from docpool.base import DocpoolMessageFactory as _
from docpool.base.content.folderbase import FolderBase
from docpool.base.content.folderbase import IFolderBase
from docpool.base.utils import getAllowedDocumentTypes
from docpool.base.utils import portalMessage
from docpool.base.utils import queryForObjects
from plone.dexterity.content import Container
from plone.directives import form
from plone.protect.interfaces import IDisableCSRFProtection
from Products.CMFCore.utils import getToolByName
from zope import schema
from zope.interface import alsoProvides
from zope.interface import implements


class ISimpleFolder(form.Schema, IFolderBase):
    """
    """

    allowedDocTypes = schema.List(
        title=_(
            u'label_simplefolder_alloweddoctypes',
            default=u'Document types allowed in this folder',
        ),
        description=_(
            u'description_simplefolder_alloweddoctypes',
            default=u'Leave blank to enable all types configured for the group.',
        ),
        required=False,
        value_type=schema.Choice(source="docpool.base.vocabularies.GroupDocType"),
    )


class SimpleFolder(Container, FolderBase):
    """
    """

    security = ClassSecurityInfo()

    implements(ISimpleFolder)

    def customMenu(self, menu_items):
        """
        """
        dts = getAllowedDocumentTypes(self)
        filter = False
        if self.allowedDocTypes:
            filter = True
        res = []
        for menu_item in menu_items:
            if menu_item.get('id') == 'DPDocument':
                for dt in dts:
                    if (
                        not dt.getObject().globalAllow
                    ):  # only generally allowed doctypes
                        continue
                    if not filter or dt.id in self.allowedDocTypes:
                        res.append(
                            {
                                'extra': {
                                    'separator': None,
                                    'id': dt.id,
                                    'class': 'contenttype-%s' % dt.id,
                                },
                                'submenu': None,
                                'description': '',
                                'title': dt.Title,
                                'action': '%s/++add++DPDocument?form.widgets.docType:list=%s'
                                % (self.absolute_url(), dt.id),
                                'selected': False,
                                'id': dt.id,
                                'icon': None,
                            }
                        )
            else:
                res.append(menu_item)
        return res

    def isPrincipalFolder(self):
        """
        """
        return self.getPortalTypeName() in ['UserFolder', 'GroupFolder']

    def canBeDeleted(self, principal_deleted=False):
        """
        A folder can be deleted, if
        - it does not contain published Documents somewhere below AND
        - it is not a member or group root folder,
              unless principal_deleted = True
        """
        mtool = getToolByName(self, "portal_membership")
        if not mtool.checkPermission("Delete objects", self):
            return False
        if self.containsPublishedDocuments():
            return False
        if self.isPrincipalFolder():
            if principal_deleted:
                return True
            else:
                return False
        return True

    def containsPublishedDocuments(self):
        """
        """
        return (
            len(
                queryForObjects(
                    self,
                    path="/".join(self.getPhysicalPath()),
                    portal_type="DPDocument",
                    review_state="published",
                )
            )
            > 0
        )

    def publish_doc(self, id, REQUEST=None):
        """
        """
        if REQUEST:
            alsoProvides(REQUEST, IDisableCSRFProtection)
        doc = None
        try:
            doc = self._getOb(id)
        except:
            pass
        if doc:
            wftool = getToolByName(self, 'portal_workflow')
            wftool.doActionFor(doc, 'publish')
            if REQUEST:
                portalMessage(self, _("The document has been published."), "info")
                return self.restrictedTraverse("@@view")()

    def mySimpleFolder(self):
        """
        """
        return self

    def getFirstChild(self):
        """
        """
        fc = self.getFolderContents()
        if len(fc) > 0:
            return fc[0].getObject()
        else:
            return None

    def getAllContentObjects(self):
        """
        """
        return [obj.getObject() for obj in self.getFolderContents()]

    def getDPDocuments(self, **kwargs):
        """
        """
        args = {'portal_type': 'DPDocument'}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)]

    def getSimpleFolders(self, **kwargs):
        """
        """
        args = {'portal_type': 'SimpleFolder'}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)]
