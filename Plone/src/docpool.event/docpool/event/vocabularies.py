from zope.component import queryUtility
from zope.interface import implements
from plone.registry.interfaces import IRegistry
from zope.schema.interfaces import IVocabularyFactory, IBaseVocabulary
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import SimpleTerm
from zope.site.hooks import getSite
from Products.CMFCore.utils import getToolByName
from docpool.event import DocpoolMessageFactory as _
from AccessControl.SecurityInfo import allow_module, allow_class
from docpool.base.utils import getDocumentPoolSite
from five import grok
from Products.CMFPlone.utils import parent

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



class PhasesVocabulary(object):
    grok.implements(IVocabularyFactory)

    def __call__(self, context):
        esd = getDocumentPoolSite(context)
        path = "/".join(esd.getPhysicalPath()) + "/contentconfig"
        cat = getToolByName(esd, 'portal_catalog', None)
        if cat is None:
            return SimpleVocabulary([])

        items = [ (t.getObject().getPhaseTitle(), t.getObject() ) for t in cat({"portal_type": "SRPhase", "path":path})]
        items.sort()
        items = [SimpleTerm(i[1], i[1].UID(), i[0]) for i in items]
        return SimpleVocabulary(items)

grok.global_utility(PhasesVocabulary, name=u"docpool.event.vocabularies.Phases")

class ModesVocabulary(object):
    grok.implements(IVocabularyFactory)

    def __call__(self, context):
        terms = []
        terms.append(SimpleVocabulary.createTerm("routine", "routine", _(u"Routine mode")))
        terms.append(SimpleVocabulary.createTerm("intensive", "intensive", _(u"Intensive mode")))
        return SimpleVocabulary(terms)

grok.global_utility(ModesVocabulary, name=u"docpool.event.vocabularies.Modes")

class NetworksVocabulary(object):
    grok.implements(IVocabularyFactory)

    def __call__(self, context):
        esd = getDocumentPoolSite(context)
        path = "/".join(esd.getPhysicalPath()) + "/contentconfig"
        cat = getToolByName(esd, 'portal_catalog', None)
        if cat is None:
            return SimpleVocabulary([])

        items = [ (t.Title, t.getObject() ) for t in cat({"portal_type": "DPNetwork", "path":path})]
        items.sort()
        items = [SimpleTerm(i[1], i[1].UID(), i[0]) for i in items]
        return SimpleVocabulary(items)

grok.global_utility(NetworksVocabulary, name=u"docpool.event.vocabularies.Networks")

class PowerStationsVocabulary(object):
    grok.implements(IVocabularyFactory)

    def __call__(self, context):
        esd = getDocumentPoolSite(context)
        path = "/".join(esd.getPhysicalPath()) + "/contentconfig"
        cat = getToolByName(esd, 'portal_catalog', None)
        if cat is None:
            return SimpleVocabulary([])

        items = [ (t.Title, t.getObject() ) for t in cat({"portal_type": "DPNuclearPowerStation", "path":path})]
        items.sort()
        items = [SimpleTerm(i[1], i[1].UID(), i[0]) for i in items]
        return SimpleVocabulary(items)

grok.global_utility(PowerStationsVocabulary, name=u"docpool.event.vocabularies.PowerStations")

class SampleTypesVocabulary(object):
    grok.implements(IVocabularyFactory)

    def __call__(self, context):
        registry = queryUtility(IRegistry)
        terms = []
        if registry is not None:
            for sType in registry.get('docpool.event.sampleTypes', ()):
                # create a term - the arguments are the value, the token, and
                # the title (optional)
                terms.append(SimpleVocabulary.createTerm(sType, sType, sType))
        return SimpleVocabulary(terms)

grok.global_utility(SampleTypesVocabulary, name=u"docpool.event.vocabularies.SampleTypes")

allow_module("docpool.event.vocabularies")
# allow_class(ELANESDVocabulary)