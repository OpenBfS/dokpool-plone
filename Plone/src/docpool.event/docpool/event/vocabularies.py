from zope.interface import implements
from zope.schema.interfaces import IVocabularyFactory, IBaseVocabulary
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import SimpleTerm
from zope.site.hooks import getSite
from Products.CMFCore.utils import getToolByName
from docpool.event import DocpoolMessageFactory as _
from AccessControl.SecurityInfo import allow_module, allow_class
from Products.Archetypes.utils import shasattr
from docpool.base.utils import getDocumentPoolSite
from docpool.base.utils import getAllowedDocumentTypesForGroup

class EventVocabulary(object):
    """    
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        esd = getDocumentPoolSite(context)        
        path = "/".join(esd.getPhysicalPath()) + "/contentconfig"
        cat = getToolByName(esd, 'portal_catalog', None)
        if cat is None:
            return SimpleVocabulary([])

        items = [ (t.Title, t.id ) for t in cat({"portal_type": "DPEvent", "path":path, "dp_type":"active"})]
        items.sort()
        items = [SimpleTerm(i[1], i[1], i[0]) for i in items]
        return SimpleVocabulary(items)

EventVocabularyFactory = EventVocabulary()

class EventRefVocabulary(object):
    """    
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        esd = getDocumentPoolSite(context)        
        path = "/".join(esd.getPhysicalPath()) + "/contentconfig"
        cat = getToolByName(esd, 'portal_catalog', None)
        if cat is None:
            return SimpleVocabulary([])

        items = [ (t.Title, t.UID ) for t in cat({"portal_type": "DPEvent", "path":path})]
        items.sort()
        items = [SimpleTerm(i[1], i[1], i[0]) for i in items]
        return SimpleVocabulary(items)

EventRefVocabularyFactory = EventRefVocabulary()

class EventSubstituteVocabulary(object):
    """    
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        esd = getDocumentPoolSite(context)        
        path = "/".join(esd.getPhysicalPath()) + "/contentconfig"
        cat = getToolByName(esd, 'portal_catalog', None)
        if cat is None:
            return SimpleVocabulary([])

        items = [ (t.Title, t.getObject() ) for t in cat({"portal_type": "DPEvent", "path":path, "dp_type":"active"})]
        items.sort()
        items = [SimpleTerm(i[1], i[1], i[0]) for i in items]
        return SimpleVocabulary(items)

EventSubstituteVocabularyFactory = EventSubstituteVocabulary()


allow_module("docpool.event.vocabularies")
# allow_class(ELANESDVocabulary)