# -*- coding: utf-8 -*-
from five import grok
from zope.schema.interfaces import IContextSourceBinder
from plone.formwidget.contenttree import ObjPathSourceBinder
from elan.esd.interfaces import IELANDocCollection
from zope.interface import provider, implementer
from zope.component import adapter
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from plone.directives import form
from z3c.relationfield.schema import RelationChoice, RelationList
from plone.formwidget.autocomplete.widget import AutocompleteFieldWidget
from zope import schema

from docpool.base.utils import queryForObjects, queryForObject, back_references
from Products.Archetypes.utils import DisplayList, shasattr
from z3c.relationfield.relation import RelationValue
from plone.formwidget.autocomplete.widget import AutocompleteFieldWidget
from zope.component import getUtility, adapter
from zope.intid.interfaces import IIntIds
from five import grok
from zope.schema.interfaces import IContextSourceBinder

from plone import api
from elan.esd import DocpoolMessageFactory as _

from Acquisition import aq_inner
from docpool.base.interfaces import IDocTypeExtension

@provider(IFormFieldProvider)    
class IELANDocType(IDocTypeExtension):
    contentCategory = RelationChoice(
                        title=_(u'label_doctype_contentcategory', default=u'Choose category for this type '),
                        description=_(u'description_doctype_contentcategory', default=u''),
                        required=False,
##code-section field_contentCategory
                        source = "elan.esd.vocabularies.Category",
##/code-section field_contentCategory                           
    )

#    form.widget(contentCategory=SelectWidget)
    form.widget(contentCategory='z3c.form.browser.select.SelectFieldWidget')



@form.default_value(field=IELANDocType['contentCategory']) 
def getDefaultCategory(data):
    """
    """
    if hasattr(data.context, "getDefaultCategory"):
        return data.context.getDefaultCategory()
    else:
        return None
    
class ELANDocType(object):
    
    def __init__(self, context):
        self.context = context

    def _get_contentCategory(self):
        return self.context.contentCategory

    def _set_contentCategory(self, value):
        if not value:
            return
        context = aq_inner(self.context)
        context.contentCategory = value
    
    contentCategory = property(_get_contentCategory, _set_contentCategory)

    def category(self):
        """
        The primary category that the documents of this type belong to.
        """
        cc = self.context.contentCategory
        res = cc and cc.to_object.title or ""
        return res

    def categories(self):
        """
        All categories, the document belongs to.
        """
        #         colls = self.getBackReferences(relationship='doctypes')
        colls = back_references(self.context, "docTypes")
        return list(set([coll.title for coll in colls if
                         coll and not coll.isArchive() and coll.getPortalTypeName() == 'ELANDocCollection']))

    def getCategories(self):
        """
        """
        mpath = "/"
        if shasattr(self.context, "dpSearchPath", acquire=True):
            mpath = self.context.dpSearchPath()
        ecs = queryForObjects(self.context, path=mpath, portal_type="ELANDocCollection", sort_on="sortable_title")
        return DisplayList([(ec.UID, ec.Title) for ec in ecs])

    def getDefaultCategory(self):
        """
        """
        #         colls = self.getBackReferences(relationship='doctypes')
        colls = self.context.back_references("docTypes")
        res = None
        if len(colls) == 1:  # Only when unique
            if colls[0]:
                intids = getUtility(IIntIds)
                to_id = intids.getId(colls[0])
                res = RelationValue(to_id)
                #         print 'getDefaultCategory ', res
        return res

    def setCCategory(self, id):
        """
        """
        mpath = "/"
        if shasattr(self.context, "dpSearchPath", acquire=True):
            mpath = self.context.dpSearchPath()
        o = queryForObject(self.context, path=mpath, portal_type="ELANDocCollection", id=id)
        #         print "CCategory", o
        intids = getUtility(IIntIds)
        to_id = intids.getId(o)
        self.context.contentCategory = RelationValue(to_id)