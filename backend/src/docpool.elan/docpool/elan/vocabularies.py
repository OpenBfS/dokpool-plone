from AccessControl.SecurityInfo import allow_module
from docpool.base.content.archiving import IArchiving
from docpool.base.content.places import IPlaces
from docpool.elan import DocpoolMessageFactory as _
from plone import api
from plone.base.utils import safe_bytes
from zope.interface import implementer
from zope.interface import provider
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


@implementer(IVocabularyFactory)
class EventVocabulary:
    """ """

    def __call__(self, context):
        query = {
            "portal_type": "DPEvent",
            "dp_type": "active",
        }
        if (dp := IPlaces(context).document_pool) is not None:
            scen = dp["contentconfig"]["scen"]
            query.update(UID=tuple(scen.subscribed_events))
        items = sorted((t.Title, t.UID) for t in api.content.find(**query))
        items = [SimpleTerm(i[1], i[1], i[0]) for i in items]
        return SimpleVocabulary(items)


EventVocabularyFactory = EventVocabulary()


@implementer(IVocabularyFactory)
class OpenEventsVocabulary:
    """ """

    def __call__(self, context):
        items = sorted(
            (
                (t.getObject().dp_type(), t.Title, t.UID)
                for t in api.content.find(portal_type="DPEvent")
                if not IArchiving(t).is_archive
            ),
            key=lambda i: (("active", "inactive", "closed").index(i[0]), i[1]),
        )
        terms = [SimpleTerm(i[2], i[2], f"{i[1]} ({i[0]})") for i in items]
        return SimpleVocabulary(terms)


OpenEventsVocabularyFactory = OpenEventsVocabulary()


@implementer(IVocabularyFactory)
class EventTypesVocabulary:
    def __call__(self, context):
        values = [
            ("Emergency", _("Emergency")),
            ("Exercise", _("Exercise")),
            ("Test", _("Test")),
            ("Routine", _("Routine")),
            ("Minor Situation", _("Minor Situation")),
        ]
        # value, token, title
        return SimpleVocabulary([SimpleTerm(i[0], i[0], i[1]) for i in values])


EventTypesVocabularyFactory = EventTypesVocabulary()


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
    def __call__(self, context=None):
        terms = []
        terms.append(SimpleVocabulary.createTerm("routine", "routine", _("Routine mode")))
        terms.append(SimpleVocabulary.createTerm("intensive", "intensive", _("Intensive mode")))
        return SimpleVocabulary(terms)


ModesVocabularyFactory = ModesVocabulary()


@provider(IVocabularyFactory)
def NetworksVocabularyFactory(context=None):
    items = [
        "Alle",
        "Alle Bundesmessnetze",
        "Alle Länder",
        "auslaendische Messnetze",
        "Baden-Wuerttemberg",
        "Bayern",
        "Berlin",
        "BfE",
        "BfS (ABI)",
        "BfS (Spuren)",
        "BfS / ZdB",
        "BMUKN",
        "Brandenburg",
        "Bremen",
        "Bundeswehr",
        "Endlager (Bundesaufsicht)",
        "FhG",
        "Hamburg",
        "Hessen",
        "Leitstelle BfG",
        "Leitstelle BfS H (u.a. Trinkwasser)",
        "Leitstelle BfS in-situ-G.",
        "Leitstelle MRI",
        "Leitstelle Thuenen-Institut",
        "Mecklenburg-Vorpommern",
        "Messnetz BfG",
        "Messnetz BfS in-situ-G.",
        "Messnetz BfS ODL",
        "Messnetz BSH",
        "Messnetz DWD",
        "Niedersachsen",
        "Nordrhein-Westfalen",
        "PTB",
        "Rheinland-Pfalz",
        "Saarland",
        "Sachsen",
        "Sachsen-Anhalt",
        "Schleswig-Holstein",
        "Sonstige",
        "Thueringen",
        "ZdB-Testnetz",
    ]
    terms = [SimpleTerm(value, safe_bytes(value), value) for value in items]
    return SimpleVocabulary(terms)


allow_module("docpool.elan.vocabularies")
# allow_class(ELANESDVocabulary)


@implementer(IVocabularyFactory)
class AlertingStatusVocabulary:
    def __call__(self, context=None):
        values = [
            ("none", "keine"),
            ("initialized", "ausgelöst"),
            ("alerted", "durchgeführt"),
        ]
        # value, token, title
        return SimpleVocabulary([SimpleTerm(i[0], i[0], i[1]) for i in values])


AlertingStatusVocabularyFactory = AlertingStatusVocabulary()
