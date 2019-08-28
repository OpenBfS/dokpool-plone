from AccessControl.SecurityInfo import allow_module
from docpool.base.utils import getDocumentPoolSite
from docpool.event import DocpoolMessageFactory as _
from plone.registry.interfaces import IRegistry
from Products.CMFCore.utils import getToolByName
from zope.component import queryUtility
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


@implementer(IVocabularyFactory)
class EventVocabulary(object):
    """
    """

    def __call__(self, context):
        esd = getDocumentPoolSite(context)
        path = "/".join(esd.getPhysicalPath()) + "/contentconfig"
        cat = getToolByName(esd, 'portal_catalog', None)
        if cat is None:
            return SimpleVocabulary([])

        items = sorted([
            (t.Title, t.id)
            for t in cat({"portal_type": "DPEvent", "path": path, "dp_type": "active"})
        ])
        items = [SimpleTerm(i[1], i[1], i[0]) for i in items]
        return SimpleVocabulary(items)


EventVocabularyFactory = EventVocabulary()


@implementer(IVocabularyFactory)
class EventRefVocabulary(object):
    """
    """

    def __call__(self, context):
        esd = getDocumentPoolSite(context)
        path = "/".join(esd.getPhysicalPath()) + "/contentconfig"
        cat = getToolByName(esd, 'portal_catalog', None)
        if cat is None:
            return SimpleVocabulary([])

        items = sorted([
            (t.Title, t.UID) for t in cat({"portal_type": "DPEvent", "path": path})
        ])
        items = [SimpleTerm(i[1], i[1], i[0]) for i in items]
        return SimpleVocabulary(items)


EventRefVocabularyFactory = EventRefVocabulary()


@implementer(IVocabularyFactory)
class EventSubstituteVocabulary(object):
    """
    """

    def __call__(self, context):
        esd = getDocumentPoolSite(context)
        path = "/".join(esd.getPhysicalPath()) + "/contentconfig"
        cat = getToolByName(esd, 'portal_catalog', None)
        if cat is None:
            return SimpleVocabulary([])

        items = sorted([
            (t.Title, t.getObject())
            for t in cat({"portal_type": "DPEvent", "path": path, "dp_type": "active"})
        ])
        items = [SimpleTerm(i[1], i[1], i[0]) for i in items]
        return SimpleVocabulary(items)


EventSubstituteVocabularyFactory = EventSubstituteVocabulary()


@implementer(IVocabularyFactory)
class PhasesVocabulary(object):

    def __call__(self, context):
        esd = getDocumentPoolSite(context)
        path = "/".join(esd.getPhysicalPath()) + "/contentconfig"
        cat = getToolByName(esd, 'portal_catalog', None)
        if cat is None:
            return SimpleVocabulary([])

        items = sorted([
            (t.getObject().getPhaseTitle(), t.getObject())
            for t in cat({"portal_type": "SRPhase", "path": path})
        ])
        items = [SimpleTerm(i[1], i[1].UID(), i[0]) for i in items]
        return SimpleVocabulary(items)


PhasesVocabularyFactory = PhasesVocabulary()


@implementer(IVocabularyFactory)
class ModesVocabulary(object):

    def __call__(self, context):
        terms = []
        terms.append(
            SimpleVocabulary.createTerm(
                "routine", "routine", _(u"Routine mode"))
        )
        terms.append(
            SimpleVocabulary.createTerm(
                "intensive", "intensive", _(u"Intensive mode"))
        )
        return SimpleVocabulary(terms)


ModesVocabularyFactory = ModesVocabulary()


@implementer(IVocabularyFactory)
class NetworksVocabulary(object):

    def __call__(self, context):
        esd = getDocumentPoolSite(context)
        path = "/".join(esd.getPhysicalPath()) + "/contentconfig"
        cat = getToolByName(esd, 'portal_catalog', None)
        if cat is None:
            return SimpleVocabulary([])

        items = sorted([
            (t.Title, t.getObject())
            for t in cat({"portal_type": "DPNetwork", "path": path})
        ])
        items = [SimpleTerm(i[1], i[1].UID(), i[0]) for i in items]
        return SimpleVocabulary(items)


NetworksVocabularyFactory = NetworksVocabulary()


@implementer(IVocabularyFactory)
class PowerStationsVocabulary(object):

    def __call__(self, context):
        esd = getDocumentPoolSite(context)
        path = "/".join(esd.getPhysicalPath()) + "/contentconfig"
        cat = getToolByName(esd, 'portal_catalog', None)
        if cat is None:
            return SimpleVocabulary([])

        items = sorted([
            (t.Title, t.getObject())
            for t in cat({"portal_type": "DPNuclearPowerStation", "path": path})
        ])
        items = [SimpleTerm(i[1], i[1].UID(), i[0]) for i in items]
        return SimpleVocabulary(items)


PowerStationsVocabularyFactory = PowerStationsVocabulary()


@implementer(IVocabularyFactory)
class SampleTypesVocabulary(object):

    def __call__(self, context):
        registry = queryUtility(IRegistry)
        terms = []
        if registry is not None:
            for sType in registry.get('docpool.event.sampleTypes', ()):
                # create a term - the arguments are the value, the token, and
                # the title (optional)
                terms.append(SimpleVocabulary.createTerm(sType, sType, sType))
        return SimpleVocabulary(terms)


SampleTypesVocabularyFactory = SampleTypesVocabulary()

allow_module("docpool.event.vocabularies")
# allow_class(ELANESDVocabulary)
