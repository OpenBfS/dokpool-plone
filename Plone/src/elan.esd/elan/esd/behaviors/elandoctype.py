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
from elan.esd import ELAN_EMessageFactory as _

from Acquisition import aq_inner

@grok.provider(IContextSourceBinder)
def availableCategories(context):
    if hasattr(context, "dpSearchPath"):
        path = context.dpSearchPath() + "/esd"
    else:
        path = "/Plone/esd"
    query = { "portal_type" : ["ELANDocCollection"],
              "path": {'query' :path } 
             }

    return ObjPathSourceBinder(navigation_tree_query = query,object_provides=IELANDocCollection.__identifier__).__call__(context)     

@provider(IFormFieldProvider)    
class IELANDocType(model.Schema):    
    contentCategory = RelationChoice(
                        title=_(u'label_doctype_contentcategory', default=u'Choose category for this type '),
                        description=_(u'description_doctype_contentcategory', default=u''),
                        required=False,
##code-section field_contentCategory
                        source = "elan.esd.vocabularies.Categories",
##/code-section field_contentCategory                           
    )

#    form.widget(contentCategory=SelectWidget)
    form.widget(contentCategory='z3c.form.browser.select.SelectFieldWidget')


        
    allowTransfer = schema.Bool(
                        title=_(u'label_doctype_allowtransfer', default=u'Can documents of this type be sent to other ESDs?'),
                        description=_(u'description_doctype_allowtransfer', default=u''),
                        required=False,
                        default=True,
##code-section field_allowTransfer
##/code-section field_allowTransfer                           
    )

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

    def _get_allowTransfer(self):
        return self.context.allowTransfer

    def _set_allowTransfer(self, value):
        if not value:
            return
        context = aq_inner(self.context)
        context.allowTransfer = value
    
    allowTransfer = property(_get_allowTransfer, _set_allowTransfer)

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
        return list(set([coll.title for coll in colls if coll and not coll.isArchive() and coll.getPortalTypeName() == 'ELANDocCollection']))
    
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
        if len(colls) == 1: # Only when unique
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
        o = queryForObject(self.context, path=mpath,portal_type="ELANDocCollection",id=id)
#         print "CCategory", o
        intids = getUtility(IIntIds)
        to_id = intids.getId(o)
        self.context.contentCategory = RelationValue(to_id)
    