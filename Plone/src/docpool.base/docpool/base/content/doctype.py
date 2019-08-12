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

from plone.dexterity.content import Container
from docpool.base.content.extendable import Extendable, IExtendable

from Products.CMFCore.utils import getToolByName

from docpool.base.utils import queryForObjects, queryForObject, back_references
from Products.Archetypes.utils import DisplayList, shasattr
from z3c.relationfield.relation import RelationValue
from plone.formwidget.autocomplete.widget import AutocompleteFieldWidget
from zope.component import getUtility, adapter
from zope.intid.interfaces import IIntIds
from five import grok
from zope.schema.interfaces import IContextSourceBinder
from plone.dexterity.interfaces import IEditFinishedEvent

from docpool.base.config import PROJECTNAME

from docpool.base import DocpoolMessageFactory as _

class IDocType(form.Schema, IExtendable):
    """
    """

    allowUploads = schema.Bool(
                        title=_(u'label_doctype_allowuploads', default=u'Can contain documents and images'),
                        description=_(u'description_doctype_allowuploads', default=u''),
                        required=False,
                        default=True,
    )


    publishImmediately = schema.Bool(
                        title=_(u'label_doctype_publishimmediately', default=u'Publish immediately?'),
                        description=_(u'description_doctype_publishimmediately', default=u''),
                        required=False,
                        default=False,
    )


    globalAllow = schema.Bool(
                        title=_(u'label_doctype_globalallow', default=u'Can be used everywhere (not only as part of another type)'),
                        description=_(u'description_doctype_globalallow', default=u''),
                        required=False,
                        default=True,
    )


    allowedDocTypes = RelationList(
                        title=_(u'label_doctype_alloweddoctypes', default=u'Types are allowed as part of this type'),
                        description=_(u'description_doctype_alloweddoctypes', default=u''),
                        required=False,
                        value_type=RelationChoice(
                                                      title=_("Folder for Document Types"),
                                                    source = "docpool.base.vocabularies.DocType",

                                                     ),

    )


    partsPattern = schema.TextLine(
                        title=_(u'label_doctype_partspattern', default=u'Name pattern for files and images belonging to this type'),
                        description=_(u'description_doctype_partspattern', default=u'Used for automatically creating objects of this type from collections of files and images.'),
                        required=False,
    )


    pdfPattern = schema.TextLine(
                        title=_(u'label_doctype_pdfpattern', default=u'Name pattern for representative PDF'),
                        description=_(u'description_doctype_pdfpattern', default=u'If PDF exists, an image will be created from its first page as a visual representation for objects of this type.'),
                        required=False,
    )


    imgPattern = schema.TextLine(
                        title=_(u'label_doctype_imgpattern', default=u'Name pattern for representative image'),
                        description=_(u'description_doctype_imgpattern', default=u'If image exists, it will be used as a visual representation for objects of this type.'),
                        required=False,
    )


    customViewTemplate = schema.TextLine(
                        title=_(u'label_doctype_customviewtemplate', default=u'Custom View Template'),
                        description=_(u'description_doctype_customviewtemplate', default=u''),
                        required=False,
    )


    form.widget(allowedDocTypes='z3c.form.browser.select.CollectionSelectFieldWidget')


class DocType(Container, Extendable):
    """
    """
    security = ClassSecurityInfo()

    implements(IDocType)



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
        args = {'portal_type':'File'}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)]

    def getImages(self, **kwargs):
        """
        """
        args = {'portal_type':'Image'}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)]


@adapter(IDocType, IEditFinishedEvent)
def updated(obj, event=None):
    # Actually, a transfer folder should never allow a change of ESD.
    # But the permission level could have been changed. So we adapt
    # the read permissions for the sending ESD accordingly.
    log("DocType updated: %s" % str(obj))
    mpath = "/"
    if shasattr(obj, "dpSearchPath", acquire=True):
        mpath = obj.dpSearchPath()
    docs = queryForObjects(obj, path=mpath,docType=obj.getId())
    for doc in docs:
        try:
            doc.getObject().reindexObject()
        except:
            pass
