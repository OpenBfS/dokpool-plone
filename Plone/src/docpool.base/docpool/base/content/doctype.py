# -*- coding: utf-8 -*-
#
# File: doctype.py
#
# Copyright (c) 2016 by Bundesamt für Strahlenschutz
# Generator: ConPD2
#            http://www.condat.de
#

__author__ = ''
__docformat__ = 'plaintext'

"""Definition of the DocType content type. See doctype.py for more
explanation on the statements below.
"""
from AccessControl import ClassSecurityInfo
from docpool.base import DocpoolMessageFactory as _
from docpool.base.content.extendable import Extendable
from docpool.base.content.extendable import IExtendable
from docpool.base.utils import queryForObjects
from plone import api
from plone.autoform import directives
from plone.dexterity.content import Container
from plone.dexterity.interfaces import IEditFinishedEvent
from Products.CMFPlone.utils import safe_hasattr
from plone.supermodel import model
from Products.CMFPlone.utils import log
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zope import schema
from zope.component import adapter
from zope.interface import implementer


class IDocType(model.Schema, IExtendable):
    """
    """

    allowUploads = schema.Bool(
        title=_(
            u'label_doctype_allowuploads', default=u'Can contain documents and images'
        ),
        description=_(u'description_doctype_allowuploads', default=u''),
        required=False,
        default=True,
    )

    publishImmediately = schema.Bool(
        title=_(
            u'label_doctype_publishimmediately',
            default=u'Publish immediately?'),
        description=_(u'description_doctype_publishimmediately', default=u''),
        required=False,
        default=False,
    )

    globalAllow = schema.Bool(
        title=_(
            u'label_doctype_globalallow',
            default=u'Can be used everywhere (not only as part of another type)',
        ),
        description=_(u'description_doctype_globalallow', default=u''),
        required=False,
        default=True,
    )

    allowedDocTypes = RelationList(
        title=_(
            u'label_doctype_alloweddoctypes',
            default=u'Types are allowed as part of this type',
        ),
        description=_(u'description_doctype_alloweddoctypes', default=u''),
        required=False,
        value_type=RelationChoice(
            title=_("Folder for Document Types"),
            source="docpool.base.vocabularies.DocType",
        ),
    )

    partsPattern = schema.TextLine(
        title=_(
            u'label_doctype_partspattern',
            default=u'Name pattern for files and images belonging to this type',
        ),
        description=_(
            u'description_doctype_partspattern',
            default=u'Used for automatically creating objects of this type from collections of files and images.',
        ),
        required=False,
    )

    pdfPattern = schema.TextLine(
        title=_(
            u'label_doctype_pdfpattern', default=u'Name pattern for representative PDF'
        ),
        description=_(
            u'description_doctype_pdfpattern',
            default=u'If PDF exists, an image will be created from its first page as a visual representation for objects of this type.',
        ),
        required=False,
    )

    imgPattern = schema.TextLine(
        title=_(
            u'label_doctype_imgpattern',
            default=u'Name pattern for representative image',
        ),
        description=_(
            u'description_doctype_imgpattern',
            default=u'If image exists, it will be used as a visual representation for objects of this type.',
        ),
        required=False,
    )

    customViewTemplate = schema.TextLine(
        title=_(
            u'label_doctype_customviewtemplate',
            default=u'Custom View Template'),
        description=_(u'description_doctype_customviewtemplate', default=u''),
        required=False,
    )

    directives.widget(
        allowedDocTypes='z3c.form.browser.select.CollectionSelectFieldWidget')


@implementer(IDocType)
class DocType(Container, Extendable):
    """
    """

    security = ClassSecurityInfo()

    def myDocType(self):
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

    def getFiles(self, **kwargs):
        """
        """
        args = {'portal_type': 'File'}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)]

    def getImages(self, **kwargs):
        """
        """
        args = {'portal_type': 'Image'}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)]


@adapter(IDocType, IEditFinishedEvent)
def updated(obj, event=None):
    log("DocType updated: %s" % str(obj))
    catalog = api.portal.get_tool('portal_catalog')
    mpath = "/"
    if safe_hasattr(obj, "dpSearchPath"):
        mpath = obj.dpSearchPath()
    brains = queryForObjects(
        obj,
        portal_type='DPDocument',
        path=mpath,
        dp_type=obj.getId(),
        )
    for brain in brains:
        try:
            # reindex object without changing the modification-date.
            log('Reindexing ' + brain.getPath())
            catalog._reindexObject(brain.getObject())
        except BaseException as e:
            log(e)
