# -*- coding: utf-8 -*-
#
# File: elandoccollection.py
#
# Copyright (c) 2015 by Condat AG
# Generator: ConPD2
#            http://www.condat.de
#

__author__ = ''
__docformat__ = 'plaintext'

"""Definition of the ELANDocCollection content type. See elandoccollection.py for more
explanation on the statements below.
"""
from AccessControl import ClassSecurityInfo
from zope.interface import implements
from zope.component import adapts
from zope import schema
from plone.directives import form, dexterity
from plone.app.textfield import RichText
from collective import dexteritytextindexer
from z3c.relationfield.schema import RelationChoice, RelationList
from plone.formwidget.contenttree import ObjPathSourceBinder
from Products.CMFPlone.utils import log, log_exc

from plone.dexterity.content import Item
from plone.app.contenttypes.content import Collection,ICollection

from Products.CMFCore.utils import getToolByName

##code-section imports
from elan.esd.utils import getScenariosForCurrentUser, getCategoriesForCurrentUser
from Products.CMFCore.permissions import View
from plone.formwidget.autocomplete.widget import AutocompleteFieldWidget,\
    AutocompleteMultiFieldWidget
from zope.lifecycleevent.interfaces import IObjectModifiedEvent,\
    IObjectAddedEvent
from zope.component import adapter
from five import grok
from zope.schema.interfaces import IContextSourceBinder
from zope.component import getUtility
from zope.intid.interfaces import IIntIds
from z3c.relationfield.relation import RelationValue
from z3c.relationfield.event import updateRelations
from docpool.base.content.doctype import IDocType

@grok.provider(IContextSourceBinder)
def availableTypes(context):
    if hasattr(context, "myDocumentPool"):
        path = '/'.join(context.myDocumentPool().getPhysicalPath()) + "/config"
    else:
        path = "/Plone/config"
    query = { "portal_type" : ["DocType"],
              "path": {'query' :path } 
             }

    return ObjPathSourceBinder(navigation_tree_query = query,object_provides=IDocType.__identifier__).__call__(context) 
##/code-section imports 

from elan.esd.config import PROJECTNAME

from elan.esd import ELAN_EMessageFactory as _

class IELANDocCollection(form.Schema, ICollection):
    """
    """
        
    docTypes = RelationList(
                        title=_(u'label_elandoccollection_doctypes', default=u'Document Types'),
                        description=_(u'description_elandoccollection_doctypes', default=u''),
                        required=False,
##code-section field_docTypes
                        value_type=RelationChoice(
                                                      title=_("Document Types"),
                                                    source = "docpool.base.vocabularies.DocType",

                                                     ),
##/code-section field_docTypes                           
    )
    

##code-section interface
    form.widget(docTypes='z3c.form.browser.select.CollectionSelectFieldWidget')
#    form.widget(docTypes=AutocompleteMultiFieldWidget)
##/code-section interface


class ELANDocCollection(Item, Collection):
    """
    """
    security = ClassSecurityInfo()
    
    implements(IELANDocCollection)
    
##code-section methods
#     def initializeArchetype(self, **kwargs):
#         # Should enable syndication for this collection
#         #TODO: Achtung umstellen bzw. verahlten pruefen!!!
#         ret_val = Collection.initializeArchetype(self, **kwargs)
#         return ret_val     


    def testSearch(self):
        """
        """
        kw = {'portal_type': {'query': ['DPDocument']}, 'sort_on': 'mdate', 'dp_type': {'query': ['eventinformation', 'nppinformation']}, 'scenarios': {'query': ['scenario2', 'scenario1']}, 'sort_order': 'reverse', 'path': {'query': '/Plone/Members'}}       
        res = self.portal_catalog(**kw)
        # print len(res)
        for r in res:
            print r.Title
        
    def getUserSelectedScenarios(self):
        """
        """
        uss = getScenariosForCurrentUser(self)
        #print usc
        return uss

    def getUserSelectedCategories(self):
        """
        """
        usc = getCategoriesForCurrentUser(self)
        #print usc
        return usc

    def results(self, batch=True, b_start=0, b_size=10, sort_on=None, brains=False):
        """Get results override, implicit = True"""
        if sort_on is None:
            sort_on = self.sort_on
        return self.getQuery(implicit = True, batch=batch, b_start=b_start, b_size=b_size, sort_on=sort_on, brains=brains)    
    
    def correctDocTypes(self):
        """
        Replace references to global doc types with references to local doc types.
        """
        dts = self.docTypes
        res = []
        intids = getUtility(IIntIds)
        if dts:
            for dt in dts:
                t = dt.to_object
                new = None
                if t:
                    tid = t.getId()
                    try:
                        new = self.config.dtypes[tid]
                    except:
                        pass
                    if new:
                        to_id = intids.getId(new)                    
                        res.append(RelationValue(to_id))
                    
            self.docTypes = res
            updateRelations(self, None)
            self.setDocTypesUpdateCollection()
            self.reindexObject()
    
    def setDocTypesUpdateCollection(self, values=None):
        """
        Update the criteria for the underlying collection.
        """
        if values:
            self.docTypes = values
            
        # We always search for ELAN content
        params = [{'i': 'portal_type', 'o': 'plone.app.querystring.operation.selection.is', 'v': ['DPDocument']}]
        # We usually also have document types configured
        # This returns the corresponding Type Object(s)
        types = self.docTypes
        if types:
            params.append({'i': 'dp_type', 'o': 'plone.app.querystring.operation.selection.is', 'v': [t.to_object.getId() for t in types if t.to_object]}) #getId() vorher
     
        self.query = params
        self.sort_on = 'changed'
        self.sort_reversed = True
        
    def isOverview(self):
        """
        Is this an overview collection?
        """
        return self.getId().find('overview') > -1
    
    def dp_type(self):
        """
        We use this index to mark those collections which actually serve as categories.
        """
        #print self
        if self.docTypes:
        #    print "active"
            return "active"
        else:
        #    print "inactive"
            return "inactive"
    
    security.declareProtected(View, 'synContentValues')
    def synContentValues(self):
        """Getter for syndycation support
        """
        syn_tool = getToolByName(self, 'portal_syndication')
        limit = int(syn_tool.getMaxItems(self))
        return self.getQuery(batch=False, brains=True, limit=limit)[:limit]
    
    def getQuery(self, **kwargs):
        """Get the query dict from the request or from the object"""
        from zope.site.hooks import getSite
        from plone.app.querystring.querybuilder import QueryBuilder
        from elan.esd.utils import getRelativePath
        #print "modified get"
        raw = kwargs.get('raw', None)
        implicit_filter = kwargs.get('implicit', False)
        value = self.query#.raw #TODO: raw-Attribut gibt es nicht, Entsprechung?
        if not value:
            self.setDocTypesUpdateCollection() # Not yet initialized
            value = self.query
        #print value
        if raw == True:
            # We actually wanted the raw value, should have called getRaw
            return value
        querybuilder = QueryBuilder(self, getSite().REQUEST)
 
        if implicit_filter:
            # Not in the archive:
            value = list(value[:]) # Otherwise we change the stored query!
            if not self.isArchive():
                # First implicit filter: the user has select scenario(s) as a filter
                uss = self.getUserSelectedScenarios()
                if uss:
                    # This is THE modification: append the implicit criterion for the scenario(s)
                    value.append({'i': 'scenarios', 'o': 'plone.app.querystring.operation.selection.is', 'v': uss})
                else: # If nothing selected, don't show results!
                    value.append({'i': 'scenarios', 'o': 'plone.app.querystring.operation.selection.is', 'v': ["dontfindanything"]})    
                    # print value
            # Second implicit filter: the user has selected categories as a filter
            # Used for the chronological overview
            if self.isOverview():
                usc = self.getUserSelectedCategories()
                if usc:
                    value.append({'i': 'category', 'o': 'plone.app.querystring.operation.selection.is', 'v': usc})
               
            # Now we restrict the search to the paths to Members and Groups.
            # This ensures that in case of archives we only get results from the correct subset.
            #m = self.content
                           
            #mpath = getRelativePath(m)
            mpath = "content"
            # Just one path allowed in the path criterion. Must be the part after the portal root, e.g. '/Members'
            value.append({'i': 'path', 'o': 'plone.app.querystring.operation.string.path', 'v': "/%s" % mpath})
             
        sort_on = kwargs.get('sort_on', self.sort_on)
        sort_order = 'reverse' if self.sort_reversed else 'ascending'
        limit = kwargs.get('limit', self.limit)
        #print value
        res = querybuilder(query=value, batch=kwargs.get('batch', False),
            b_start=kwargs.get('b_start', 0), b_size=kwargs.get('b_size', 30),
            sort_on=sort_on, sort_order=sort_order,
            limit=limit, brains=kwargs.get('brains', False))
        #print len(res)
        return res
    
##/code-section methods 


##code-section bottom
@adapter(IELANDocCollection, IObjectModifiedEvent)    
def update_docTypes(obj, event=None):
    """
    """
    if obj:
        #print "update_docTypes", obj.docTypes
        obj.setDocTypesUpdateCollection()
        obj.reindexObject()
        
@adapter(IELANDocCollection, IObjectAddedEvent)    
def enableSyndication(obj, event=None):
    syn_tool = getToolByName(obj, 'portal_syndication', None)
    if syn_tool is not None:
        if (syn_tool.isSiteSyndicationAllowed() and
                                not syn_tool.isSyndicationAllowed(obj)):
            syn_tool.enableSyndication(obj)

##/code-section bottom 
