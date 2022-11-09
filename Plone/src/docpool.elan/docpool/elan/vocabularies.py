from AccessControl.SecurityInfo import allow_module
from docpool.base.utils import getDocumentPoolSite
from docpool.elan import DocpoolMessageFactory as _
from plone.app.vocabularies.catalog import StaticCatalogVocabulary
from plone.base.utils import safe_bytes
from Products.CMFCore.utils import getToolByName
from zope.interface import implementer
from zope.interface import provider
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


@implementer(IVocabularyFactory)
class EventVocabulary:
    """ """

    def __call__(self, context):
        esd = getDocumentPoolSite(context)
        path = "/".join(esd.getPhysicalPath()) + "/contentconfig"
        cat = getToolByName(esd, "portal_catalog", None)
        if cat is None:
            return SimpleVocabulary([])

        items = sorted(
            (t.Title, t.id)
            for t in cat({"portal_type": "DPEvent", "path": path, "dp_type": "active"})
        )
        items = [SimpleTerm(i[1], i[1], i[0]) for i in items]
        return SimpleVocabulary(items)


EventVocabularyFactory = EventVocabulary()


@implementer(IVocabularyFactory)
class EventTypesVocabulary:
    def __call__(self, context):
        values = [
            ("Emergency", _("Emergency")),
            ("Routine", _("Routine")),
            ("Exercise", _("Exercise")),
            ("Test", _("Test")),
        ]
        # value, token, title
        return SimpleVocabulary([SimpleTerm(i[0], i[0], i[1]) for i in values])


EventTypesVocabularyFactory = EventTypesVocabulary()


@implementer(IVocabularyFactory)
class EventRefVocabulary:
    """ """

    def __call__(self, context):
        esd = getDocumentPoolSite(context)
        path = "/".join(esd.getPhysicalPath()) + "/contentconfig"
        cat = getToolByName(esd, "portal_catalog", None)
        if cat is None:
            return SimpleVocabulary([])

        items = sorted(
            (t.Title, t.UID) for t in cat({"portal_type": "DPEvent", "path": path})
        )
        items = [SimpleTerm(i[1], i[1], i[0]) for i in items]
        return SimpleVocabulary(items)


EventRefVocabularyFactory = EventRefVocabulary()


@implementer(IVocabularyFactory)
class EventSubstituteVocabulary:
    """ """

    def __call__(self, context):
        esd = getDocumentPoolSite(context)
        path = "/".join(esd.getPhysicalPath()) + "/contentconfig"
        cat = getToolByName(esd, "portal_catalog", None)
        if cat is None:
            return SimpleVocabulary([])

        items = sorted(
            (t.Title, t.getObject())
            for t in cat({"portal_type": "DPEvent", "path": path, "dp_type": "active"})
        )
        items = [SimpleTerm(i[1], i[1], i[0]) for i in items]
        return SimpleVocabulary(items)


EventSubstituteVocabularyFactory = EventSubstituteVocabulary()


@implementer(IVocabularyFactory)
class StatusVocabulary:
    """ """

    def __call__(self, context):
        terms = [
            SimpleTerm("active", title=_("active")),
            SimpleTerm("inactive", title=_("inactive")),
        ]
        # When editing closed events, only show the "closed" state. When editing events in
        # other states or adding events (context isn't DPEvent), don't (re: #4634).
        if context.portal_type == "DPEvent" and context.Status == "closed":
            terms = [SimpleTerm("closed", title=_("closed"))]
        return SimpleVocabulary(terms)


StatusVocabularyFactory = StatusVocabulary()


@implementer(IVocabularyFactory)
class ModesVocabulary:
    def __call__(self, context):
        terms = []
        terms.append(
            SimpleVocabulary.createTerm("routine", "routine", _("Routine mode"))
        )
        terms.append(
            SimpleVocabulary.createTerm("intensive", "intensive", _("Intensive mode"))
        )
        return SimpleVocabulary(terms)


ModesVocabularyFactory = ModesVocabulary()


@implementer(IVocabularyFactory)
class SampleType:
    def __call__(self, context=None):
        items = [
            ("A", "Abwasser, Reststoffe und Abfälle"),
            ("A1", "Kläranlage"),
            ("A2", "Verbrennungsanlage"),
            ("A3", "Mülldeponie"),
            ("A4", "Kompostierungsanlage"),
            ("A5", "Spezielle Reststoffe und Abfälle"),
            ("B", "Boden"),
            ("B2", "Boden in-situ (nuklidspezifische Dosisleistung)"),
            ("B3", "Weide-/ Acker-/ Wald-/ Freizeitflächen-/ Ödland- und Gartenböden"),
            ("F", "Futtermittel"),
            ("F1", "Grünfutter (einschl. Weide- und Wiesenbewuchs)"),
            ("F2", "Mais"),
            ("F3", "Futtergetreide"),
            ("F4", "Hackfrüchte"),
            ("F5", "Heu, Stroh, Cobs, Trockenmehle"),
            ("F6", "Mischfuttermittelrohstoffe"),
            ("F7", "Mischfuttermittel"),
            ("G", "Gewässer"),
            ("G1", "Fließgewässer"),
            ("G2", "Stehende Gewässer"),
            ("G3", "Meer"),
            ("G4", "Grundwasser"),
            ("G5", "Rohwasser zur Trinkwassergewinnung"),
            ("GZ", "Sonstige Wässer"),
            ("I", "Bio-Indikatoren, Tabak und Arzneimittel"),
            ("I1", "Pflanzliche Indikatoren"),
            ("I2", "Tabak"),
            ("I3", "Arzneimittel"),
            ("L", "Luft und Niederschlag"),
            ("L1", "Luft/Gammastrahlung"),
            ("L2", "Luft/Neutronenstrahlung"),
            ("L3", "Luft/Aerosole"),
            ("L4", "Luft/gasförmige Komponenten (einschl. Iod)"),
            ("L5", "Niederschlag"),
            ("L6", "Spurenmessung Luft"),
            ("M", "Meteo-Umweltbereich"),
            ("N", "Nahrungsmittel (einschl. Trinkwasser)"),
            ("N1", "Milch"),
            ("N2", "Frischgemüse (einschl. Kartoffeln und Pilze)"),
            ("N3", "Getreide"),
            ("N4", "Obst"),
            ("N5", "Fleisch"),
            ("N6", "Fisch und Meeresfrüchte"),
            ("N7", "Trinkwasser"),
            ("N8", "Gesamtnahrung, Fertiggerichte und Getränke"),
            ("N9", "Nahrungsmittelprodukte"),
            ("NZ", "Sonstige Nahrungsmittel"),
            ("S", "Umweltbereiche für Störfall"),
            ("S1", "Luft - Störfall"),
            ("S2", "Boden/-Oberfläche - Störfall"),
            ("S3", "Pflanzen/Bewuchs - Störfall"),
            ("S4", "Oberirdische Gewässer - Störfall"),
            ("Z", "Sonstige Mediengruppen"),
            ("Z1", "Baustoffe"),
            ("Z2", "Bodenschätze"),
            ("Z3", "Bedarfsgegenstände und Kosmetische Mittel"),
        ]
        terms = [
            SimpleTerm(value, safe_bytes(value), f"{value} {title}")
            for value, title in items
        ]
        return SimpleVocabulary(terms)


SampleTypeVocabularyFactory = SampleType()


@implementer(IVocabularyFactory)
class NetworksVocabulary:
    def __call__(self, context):
        esd = getDocumentPoolSite(context)
        path = "/".join(esd.getPhysicalPath()) + "/contentconfig"
        cat = getToolByName(esd, "portal_catalog", None)
        if cat is None:
            return SimpleVocabulary([])

        items = sorted(
            (t.Title, t.getObject())
            for t in cat({"portal_type": "DPNetwork", "path": path})
        )
        items = [SimpleTerm(i[1], i[1].UID(), i[0]) for i in items]
        return SimpleVocabulary(items)


NetworksVocabularyFactory = NetworksVocabulary()


@implementer(IVocabularyFactory)
class PowerStationsVocabulary:
    def __call__(self, context):
        esd = getDocumentPoolSite(context)
        path = "/".join(esd.getPhysicalPath()) + "/contentconfig"
        cat = getToolByName(esd, "portal_catalog", None)
        if cat is None:
            return SimpleVocabulary([])

        items = sorted(
            (t.Title, t.getObject())
            for t in cat({"portal_type": "DPNuclearPowerStation", "path": path})
        )
        items = [SimpleTerm(i[1], i[1].UID(), i[0]) for i in items]
        return SimpleVocabulary(items)


PowerStationsVocabularyFactory = PowerStationsVocabulary()


allow_module("docpool.elan.vocabularies")
# allow_class(ELANESDVocabulary)


@implementer(IVocabularyFactory)
class AlertingStatusVocabulary:
    def __call__(self, context):
        values = [
            ("none", "keine"),
            ("initialized", "ausgelöst"),
            ("alerted", "durchgeführt"),
        ]
        # value, token, title
        return SimpleVocabulary([SimpleTerm(i[0], i[0], i[1]) for i in values])


AlertingStatusVocabularyFactory = AlertingStatusVocabulary()


@provider(IVocabularyFactory)
def CategoryVocabularyFactory(context=None):
    """Used for Relationfield docpool.elan.behaviors.elandoctype.IELANDocType.contentCategory
    and docpool.elan.portlets.collection.ICollectionPortlet.collection
    """
    esd = getDocumentPoolSite(context)
    path = "/".join(esd.getPhysicalPath()) + "/esd"
    return StaticCatalogVocabulary(
        {
            "portal_type": "ELANDocCollection",
            "sort_on": "sortable_title",
            "path": path,
        },
        title_template="{brain.Title}",
    )


@implementer(IVocabularyFactory)
class CategoriesVocabulary:
    """ """

    def __call__(self, context):
        # print context
        esd = getDocumentPoolSite(context)
        path = "/".join(esd.getPhysicalPath()) + "/esd"
        cat = getToolByName(esd, "portal_catalog", None)
        if cat is None:
            return SimpleVocabulary([])

        items = sorted(
            (t.Title, t.getId)
            for t in cat({"portal_type": "ELANDocCollection", "path": path})
        )
        items = [SimpleTerm(i[1], i[1], i[0]) for i in items]
        return SimpleVocabulary(items)


CategoriesVocabularyFactory = CategoriesVocabulary()
