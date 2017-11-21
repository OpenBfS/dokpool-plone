from zope.interface import implements
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import SimpleTerm
from Products.CMFCore.utils import getToolByName
from elan.esd import DocpoolMessageFactory as _
from AccessControl.SecurityInfo import allow_module, allow_class
from docpool.base.utils import getDocumentPoolSite

def title_default(brain):
    return brain.Title

def _createVocab(context, raw, ptype, path="", sort_on="sortable_title", add_query={}, identifier=None,
                 title_method=title_default,
                 filter_method=None):
    esd = getDocumentPoolSite(context)        
    path = "/".join(esd.getPhysicalPath()) + path
    cat = getToolByName(esd, 'portal_catalog', None)

    if cat is None:
        if not raw:
            return SimpleVocabulary([])
        else:
            return []
    sort = (sort_on != "Title") and sort_on or "sortable_title"
    query = {"portal_type":ptype, "sort_on": sort , "path": path}
    query.update(add_query)
    types = cat(query)
    if identifier == "UID":
        types = [ (brain.UID, title_method(brain)) for brain in types if not filter_method or filter_method(context, brain)]
    elif identifier == "id": 
        types = [ (brain.getId, title_method(brain)) for brain in types if not filter_method or filter_method(context, brain)]
    else:
        types = [ (brain.getObject(), title_method(brain), brain.UID) for brain in types if not filter_method or filter_method(context, brain)]
    if sort_on=="Title":
        types = sorted(types,key=lambda x: x[1])
    if not raw:
        if identifier is None:
            items = [SimpleTerm(i[0], i[2], i[1]) for i in types]
        else:
            items = [SimpleTerm(i[0], i[0], i[1]) for i in types]
        return SimpleVocabulary(items)
    else:
        return types

def phase_title(brain):
    return brain.getObject().getPhaseTitle()

class PhasesVocabulary(object):
    """
    """
    implements(IVocabularyFactory)

    def __call__(self, context, raw=False):
        # print context
        return _createVocab(context, raw, "SRPhase", "/contentconfig", sort_on="Title", title_method=phase_title)
    
PhasesVocabularyFactory = PhasesVocabulary()

class CurrentReportsVocabulary(object):
    """
    """
    implements(IVocabularyFactory)

    def __call__(self, context, raw=False):
        # print context
        return _createVocab(context, raw, "SituationReport", "/content", add_query={'review_state': 'private'})
    
CurrentReportsVocabularyFactory = CurrentReportsVocabulary()

def module_title(brain):
    return brain.getObject().getModuleTitle()

class CurrentModulesVocabulary(object):
    """
    """
    implements(IVocabularyFactory)

    def __call__(self, context, raw=False):
        return _createVocab(context, raw, "SRModule", "/content", sort_on="changed",
                            add_query={'sort_order':'reverse',
                                        'review_state': 'published'},
                            title_method=module_title,
                            filter_method=moduleFilter)

def moduleFilter(context, brain):
    mObj = brain.getObject()
    if mObj:
        if mObj.currentReport: # if the module is assigned to a report
            return  mObj.currentReport.to_object == context # and if it is the same report
    return False

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
        return _createVocab(context, raw, "SRModuleType", "/config", sort_on="id", identifier="id")
    
ModuleTypesVocabularyFactory = ModuleTypesVocabulary()

class CollectionsVocabulary(object):
    """
    """
    implements(IVocabularyFactory)

    def __call__(self, context, raw=False):
        # print context
        return _createVocab(context, raw, "SRCollection", "/contentconfig")
    
CollectionsVocabularyFactory = CollectionsVocabulary()

class TextBlocksVocabulary(object):
    """
    """
    implements(IVocabularyFactory)

    def __call__(self, context, raw=False):
        # print context
        return _createVocab(context, raw, "SRTextBlock", "/contentconfig")
    
TextBlocksVocabularyFactory = TextBlocksVocabulary()


allow_module("elan.sitrep.vocabularies")
