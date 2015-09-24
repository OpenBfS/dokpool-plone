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


def _createVocab(context, raw, ptype, path="", sort_on="sortable_title", add_query={}, identifier=None):
    esd = getDocumentPoolSite(context)        
    path = "/".join(esd.getPhysicalPath()) + path
    cat = getToolByName(esd, 'portal_catalog', None)
    if cat is None:
        if not raw:
            return SimpleVocabulary([])
        else:
            return []
    query = {"portal_type":ptype, "sort_on": sort_on , "path": path}
    query.update(add_query)
    types = cat(query)

    if identifier == "UID":
        types = [ (brain.UID, brain.Title) for brain in types ]
    elif identifier == "id": 
        types = [ (brain.getId, brain.Title) for brain in types ]  
    else:
        types = [ (brain.getObject(), brain.Title) for brain in types ]  
    if not raw:
        items = [SimpleTerm(i[0], i[0], i[1]) for i in types]
        return SimpleVocabulary(items)
    else:
        return types


class PhasesVocabulary(object):
    """
    """
    implements(IVocabularyFactory)

    def __call__(self, context, raw=False):
        # print context
        return _createVocab(context, raw, "SRPhase", "/config")
    
PhasesVocabularyFactory = PhasesVocabulary()

class CurrentReportsVocabulary(object):
    """
    """
    implements(IVocabularyFactory)

    def __call__(self, context, raw=False):
        # print context
        return _createVocab(context, raw, "SituationReport", "/content", add_query={'review_state': 'private'})
    
CurrentReportsVocabularyFactory = CurrentReportsVocabulary()

class CurrentModulesVocabulary(object):
    """
    """
    implements(IVocabularyFactory)

    def __call__(self, context, raw=False):
        # print context
        return _createVocab(context, raw, "SRModule", "/content", sort_on="changed", add_query={'sort_order':'reverse', 'review_state': 'published'})
    
CurrentModulesVocabularyFactory = CurrentModulesVocabulary()

class PastReportsVocabulary(object):
    """
    """
    implements(IVocabularyFactory)

    def __call__(self, context, raw=False):
        # print context
        return _createVocab(context, raw, "SituationReport", "/content", add_query={'review_state': 'published'})
    
PastReportsVocabularyFactory = PastReportsVocabulary()

class ModuleTypesVocabulary(object):
    """
    """
    implements(IVocabularyFactory)

    def __call__(self, context, raw=False):
        # print context
        return _createVocab(context, raw, "SRModuleType", "/config", identifier="id")
    
ModuleTypesVocabularyFactory = ModuleTypesVocabulary()

class CollectionsVocabulary(object):
    """
    """
    implements(IVocabularyFactory)

    def __call__(self, context, raw=False):
        # print context
        return _createVocab(context, raw, "SRCollection", "/config")
    
CollectionsVocabularyFactory = CollectionsVocabulary()

class TextBlocksVocabulary(object):
    """
    """
    implements(IVocabularyFactory)

    def __call__(self, context, raw=False):
        # print context
        return _createVocab(context, raw, "SRTextBlock", "/config")
    
TextBlocksVocabularyFactory = TextBlocksVocabulary()


allow_module("elan.sitrep.vocabularies")
