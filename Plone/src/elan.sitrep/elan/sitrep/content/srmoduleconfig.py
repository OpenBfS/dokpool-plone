# -*- coding: utf-8 -*-
#
# File: srmoduleconfig.py
#
# Copyright (c) 2017 by Condat AG
# Generator: ConPD2
#            http://www.condat.de
#

__author__ = ''
__docformat__ = 'plaintext'

"""Definition of the SRModuleConfig content type. See srmoduleconfig.py for more
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

from Products.CMFCore.utils import getToolByName

from zope.component import adapter
from plone.dexterity.interfaces import IEditFinishedEvent

from elan.sitrep.config import PROJECTNAME

from elan.sitrep import DocpoolMessageFactory as _

class ISRModuleConfig(form.Schema):
    """
    """

    modType = schema.Choice(
                        title=_(u'label_srmoduleconfig_modtype', default=u'Module Type'),
                        description=_(u'description_srmoduleconfig_modtype', default=u''),
                        required=True,
                        source="elan.sitrep.vocabularies.ModuleTypes",
    )


    docSelection = RelationChoice(
                        title=_(u'label_srmoduleconfig_docselection', default=u'Collection for relevant documents'),
                        description=_(u'description_srmoduleconfig_docselection', default=u'This collection defines a pre-selection of possible documents to reference within this module.'),
                        required=False,
                        source = "elan.sitrep.vocabularies.Collections",
    )


    textBlocks = RelationList(
                        title=_(u'label_srmoduleconfig_textblocks', default=u'Text Blocks'),
                        description=_(u'description_srmoduleconfig_textblocks', default=u''),
                        required=False,
                        value_type=RelationChoice(
                                                      title=_("Text Blocks"),
                                                      source = "elan.sitrep.vocabularies.TextBlocks",

                                                     ),
    )

    defaultTextBlocks = RelationList(
                        title=_(u'label_srmoduletype_defaulttextblocks', default=u'Default Text (when freshly created)'),
                        description=_(u'description_srmoduletype_defaulttextblocks', default=u''),
                        required=False,
                        value_type=RelationChoice(
                            title=_("Default Text"),
                            source="elan.sitrep.vocabularies.TextBlocks",

                        ),
    )


    form.widget(docSelection='z3c.form.browser.select.SelectFieldWidget')
    form.widget(textBlocks='z3c.form.browser.select.CollectionSelectFieldWidget')
    form.widget(defaultTextBlocks='z3c.form.browser.select.CollectionSelectFieldWidget')



class SRModuleConfig(Item):
    """
    """
    security = ClassSecurityInfo()

    implements(ISRModuleConfig)

    def getSRModuleNames(self):
        """
        Index Method
        """
        return [ self.modType ]

    def getSRModuleRefs(self):
        """
        Index Method
        """
        return [ self.UID() ]

    def currentDocuments(self):
        """
        Return the documents from the referenced collection - if any.
        """
        if self.docSelection:
            coll = self.docSelection.to_object
            return coll.results(batch=False)
        else:
            return []

    def currentTextBlocks(self):
        """
        """
        return [ tb.to_object for tb in ( self.textBlocks or [] )]


@adapter(ISRModuleConfig, IEditFinishedEvent)
def updated(obj, event=None):
    log("SRModuleConfig updated: %s" % str(obj))
    sr_cat = getToolByName(obj, "sr_catalog")
    sr_cat._reindexObject(obj)
    if obj.textBlocks:
        for tb in obj.textBlocks:
            sr_cat._reindexObject(tb.to_object)

