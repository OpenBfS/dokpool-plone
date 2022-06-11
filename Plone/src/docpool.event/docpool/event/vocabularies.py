# -*- coding: utf-8 -*-
from AccessControl.SecurityInfo import allow_module
from docpool.base.utils import getDocumentPoolSite
from docpool.event import DocpoolMessageFactory as _
from plone.base.utils import safe_bytes
from Products.CMFCore.utils import getToolByName
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
class EventTypesVocabulary(object):

    def __call__(self, context):
        values = [
            (u'Emergency', _(u'Emergency')),
            (u'Routine', _(u'Routine')),
            (u'Exercise', _(u'Exercise')),
            (u'Test', _(u'Test')),
            ]
        # value, token, title
        return SimpleVocabulary([SimpleTerm(i[0], i[0], i[1]) for i in values])


EventTypesVocabularyFactory = EventTypesVocabulary()


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
class StatusVocabulary(object):
    """
    """

    def __call__(self, context):
        terms = [
            SimpleTerm('active', title=_('active')),
            SimpleTerm('inactive', title=_('inactive')),
        ]
        # When editing closed events, only show the "closed" state. When editing events in
        # other states or adding events (context isn't DPEvent), don't (re: #4634).
        if context.portal_type == "DPEvent" and context.Status == "closed":
            terms = [SimpleTerm('closed', title=_('closed'))]
        return SimpleVocabulary(terms)


StatusVocabularyFactory = StatusVocabulary()


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
class SampleType(object):

    def __call__(self, context=None):
        items = [
            (u'A', u'Abwasser, Reststoffe und Abfälle'),
            (u'A1', u'Kläranlage'),
            (u'A2', u'Verbrennungsanlage'),
            (u'A3', u'Mülldeponie'),
            (u'A4', u'Kompostierungsanlage'),
            (u'A5', u'Spezielle Reststoffe und Abfälle'),
            (u'B', u'Boden'),
            (u'B2', u'Boden in-situ (nuklidspezifische Dosisleistung)'),
            (u'B3', u'Weide-/ Acker-/ Wald-/ Freizeitflächen-/ Ödland- und Gartenböden'),
            (u'F', u'Futtermittel'),
            (u'F1', u'Grünfutter (einschl. Weide- und Wiesenbewuchs)'),
            (u'F2', u'Mais'),
            (u'F3', u'Futtergetreide'),
            (u'F4', u'Hackfrüchte'),
            (u'F5', u'Heu, Stroh, Cobs, Trockenmehle'),
            (u'F6', u'Mischfuttermittelrohstoffe'),
            (u'F7', u'Mischfuttermittel'),
            (u'G', u'Gewässer'),
            (u'G1', u'Fließgewässer'),
            (u'G2', u'Stehende Gewässer'),
            (u'G3', u'Meer'),
            (u'G4', u'Grundwasser'),
            (u'G5', u'Rohwasser zur Trinkwassergewinnung'),
            (u'GZ', u'Sonstige Wässer'),
            (u'I', u'Bio-Indikatoren, Tabak und Arzneimittel'),
            (u'I1', u'Pflanzliche Indikatoren'),
            (u'I2', u'Tabak'),
            (u'I3', u'Arzneimittel'),
            (u'L', u'Luft und Niederschlag'),
            (u'L1', u'Luft/Gammastrahlung'),
            (u'L2', u'Luft/Neutronenstrahlung'),
            (u'L3', u'Luft/Aerosole'),
            (u'L4', u'Luft/gasförmige Komponenten (einschl. Iod)'),
            (u'L5', u'Niederschlag'),
            (u'L6', u'Spurenmessung Luft'),
            (u'M', u'Meteo-Umweltbereich'),
            (u'N', u'Nahrungsmittel (einschl. Trinkwasser)'),
            (u'N1', u'Milch'),
            (u'N2', u'Frischgemüse (einschl. Kartoffeln und Pilze)'),
            (u'N3', u'Getreide'),
            (u'N4', u'Obst'),
            (u'N5', u'Fleisch'),
            (u'N6', u'Fisch und Meeresfrüchte'),
            (u'N7', u'Trinkwasser'),
            (u'N8', u'Gesamtnahrung, Fertiggerichte und Getränke'),
            (u'N9', u'Nahrungsmittelprodukte'),
            (u'NZ', u'Sonstige Nahrungsmittel'),
            (u'S', u'Umweltbereiche für Störfall'),
            (u'S1', u'Luft - Störfall'),
            (u'S2', u'Boden/-Oberfläche - Störfall'),
            (u'S3', u'Pflanzen/Bewuchs - Störfall'),
            (u'S4', u'Oberirdische Gewässer - Störfall'),
            (u'Z', u'Sonstige Mediengruppen'),
            (u'Z1', u'Baustoffe'),
            (u'Z2', u'Bodenschätze'),
            (u'Z3', u'Bedarfsgegenstände und Kosmetische Mittel'),
        ]
        terms = [SimpleTerm(value,
                            safe_bytes(value),
                            u'{} {}'.format(value, title))
                 for value, title in items]
        return SimpleVocabulary(terms)


SampleTypeVocabularyFactory = SampleType()


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


allow_module("docpool.event.vocabularies")
# allow_class(ELANESDVocabulary)


@implementer(IVocabularyFactory)
class AlertingStatusVocabulary(object):

    def __call__(self, context):
        values = [
            (u'none', u'keine'),
            (u'initialized', u'ausgelöst'),
            (u'alerted', u'durchgeführt'),
            ]
        # value, token, title
        return SimpleVocabulary([SimpleTerm(i[0], i[0], i[1]) for i in values])


AlertingStatusVocabularyFactory = AlertingStatusVocabulary()
