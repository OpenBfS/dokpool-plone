from zope.interface import implements
from zope.schema.interfaces import IVocabularyFactory, IBaseVocabulary
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import SimpleTerm
from zope.site.hooks import getSite
from Products.CMFCore.utils import getToolByName
from elan.esd import ELAN_EMessageFactory as _
from AccessControl.SecurityInfo import allow_module, allow_class
from Products.Archetypes.utils import shasattr
from docpool.base.utils import getDocumentPoolSite
from docpool.base.utils import getAllowedDocumentTypesForGroup

class StatusVocabulary(object):
    """
    """
    implements(IVocabularyFactory)
    
    def __call__(self, context):
        return SimpleVocabulary([SimpleTerm('active', title=_('active')),SimpleTerm('inactive', title=_('inactive')),SimpleTerm('closed', title=_('closed'))])
    
StatusVocabularyFactory = StatusVocabulary()


class DTOptionsVocabulary(object):
    """
    """
    implements(IVocabularyFactory)
    
    def __call__(self, context):
        # print context
        if not context:
            return []
        return SimpleVocabulary([SimpleTerm(dt[0], title=dt[1]) for dt in context.getMatchingDocTypes()])
    
DTOptionsVocabularyFactory = DTOptionsVocabulary()

class DocumentTypesVocabulary(object):
    """    
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        esd = getDocumentPoolSite(context)        
        path = "/".join(esd.getPhysicalPath()) + "/config"
        cat = getToolByName(esd, 'portal_catalog', None)
        if cat is None:
            return SimpleVocabulary([])

        items = [ (t.Title, t.id ) for t in cat({"portal_type": "DocType", "path":path})]
        items.extend([('active', 'active'), ('inactive','inactive'), ('closed','closed')])
        items.sort()
        items = [SimpleTerm(i[1], i[1], i[0]) for i in items]
        return SimpleVocabulary(items)

DocumentTypesVocabularyFactory = DocumentTypesVocabulary()




class DocTypeVocabulary(object):
    """
    """
    implements(IVocabularyFactory)
    
    def __call__(self, context, raw=False, filtered=False):
        # print context
        esd = getDocumentPoolSite(context)        
        path = "/".join(esd.getPhysicalPath()) + "/config"
        cat = getToolByName(esd, 'portal_catalog', None)
        if cat is None:
            if not raw:
                return SimpleVocabulary([])
            else:
                return []
        types = cat({"portal_type":"DocType", "sort_on": "sortable_title", "path": path})
        # print len(types)
        if filtered:
            if not raw:
                types = [ (brain.getObject(), brain.Title) for brain in types ] 
            else:
                types = [ (brain.getId, brain.Title) for brain in types ] 
        else:
            if not raw:
                types = [ (brain.getObject(), brain.Title) for brain in types ] 
            else:
                types = [ (brain.getId, brain.Title) for brain in types ] 
            
        # print types
        if not raw:
            items = [SimpleTerm(i[0], i[0], i[1]) for i in types]
            return SimpleVocabulary(items)
        else:
            return types
        
DocTypeVocabularyFactory = DocTypeVocabulary()

class GroupDocTypeVocabulary(object):
    """
    """
    implements(IVocabularyFactory)
    
    def __call__(self, context):
        types = getAllowedDocumentTypesForGroup(context)
        # print len(types)
        types = [ (brain.getId, brain.Title) for brain in types] 
        # print types
        items = [SimpleTerm(i[0], i[0], i[1]) for i in types]
        return SimpleVocabulary(items)
   
GroupDocTypeVocabularyFactory = GroupDocTypeVocabulary()
        
class DocumentPoolVocabulary(object):
    """
    """
    implements(IVocabularyFactory)
    
    def __call__(self, context, raw=False):
        my_uid = None
        if shasattr(context, "myDocumentPool", True):
            my_uid = context.myDocumentPool().UID()
                
        site = getSite()
        cat = getToolByName(site, 'portal_catalog', None)
        if cat is None:
            if not raw:
                return SimpleVocabulary([])
            else:
                return []
        esds = cat.unrestrictedSearchResults({"portal_type":"DocumentPool", "sort_on": "sortable_title"})
        # print len(esds)
        esds = [ (brain.UID, brain.Title) for brain in esds if brain.UID != my_uid] 
        # print esds
        if not raw:
            items = [SimpleTerm(i[0], i[0], i[1]) for i in esds]
            return SimpleVocabulary(items)
        else:
            return esds
        
DocumentPoolVocabularyFactory = DocumentPoolVocabulary()

class UserDocumentPoolVocabulary(object):
    """
    """
    implements(IVocabularyFactory)
    
    def __call__(self, context, raw=False):
                
        site = getSite()
        cat = getToolByName(site, 'portal_catalog', None)
        if cat is None:
            if not raw:
                return SimpleVocabulary([])
            else:
                return []
        esds = cat.unrestrictedSearchResults({"portal_type":"DocumentPool", "sort_on": "sortable_title"})
        # print len(esds)
        esds = [ (brain.UID, brain.Title) for brain in esds] 
        # print esds
        if not raw:
            items = [SimpleTerm(i[0], i[0], i[1]) for i in esds]
            return SimpleVocabulary(items)
        else:
            return esds
        
UserDocumentPoolVocabularyFactory = UserDocumentPoolVocabulary()

allow_module("docpool.base.vocabularies")
allow_class(DocumentPoolVocabulary)