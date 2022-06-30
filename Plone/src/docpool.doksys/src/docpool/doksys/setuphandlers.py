from docpool.config.utils import CHILDREN
from docpool.config.utils import createPloneObjects
from docpool.config.utils import ID
from docpool.config.utils import TITLE
from docpool.config.utils import TYPE
from persistent.list import PersistentList
from plone import api
from plone.app.textfield.value import RichTextValue
from Products.CMFPlone.interfaces import INonInstallable
from Products.CMFPlone.utils import _createObjectByType
from zope.component.hooks import getSite
from zope.interface import implementer

import logging
import transaction


log = logging.getLogger(__name__)


@implementer(INonInstallable)
class HiddenProfiles:
    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller."""
        return ["docpool.doksys:uninstall"]


def post_install(context):
    """Post install script"""
    # Do something at the end of the installation of this package.
    fresh = True
    createStructure(context, getSite(), fresh)


def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.


def createStructure(context, plonesite, fresh):
    changedoksysNavigation(plonesite, fresh)
    searches = context.restrictedTraverse("searches")
    if searches.getProperty("text") is None:
        searches.manage_addProperty("text", "", "string")
        transaction.commit()
    create_today_collection(plonesite)
    transaction.commit()
    create_since_yesterday_collection(plonesite)
    transaction.commit()
    create_purpose_collections(plonesite)
    transaction.commit()
    create_sample_collections(plonesite)
    transaction.commit()
    changedoksysDocTypes(plonesite, fresh)
    transaction.commit()


def changedoksysNavigation(plonesite, fresh):
    createPloneObjects(plonesite, BASICSTRUCTURE, fresh)


def changedoksysDocTypes(plonesite, fresh):
    createPloneObjects(plonesite.config.dtypes, DTYPES, fresh)


def create_today_collection(plonesite):
    container = api.content.get(path="/searches")
    if "today" in container:
        return

    title = "Dokumente von Heute"
    description = "Dokumente seit heute 0:00 Uhr"
    _createObjectByType(
        "Collection", container, id="today", title=title, description=description
    )
    today = container["today"]

    # Set the Collection criteria.
    #: Sort on the Effective date
    today.sort_on = "changed"
    today.sort_reversed = True
    today.relatedItems = []
    #: Query by Type and Review State
    today.query = [
        {
            "i": "portal_type",
            "o": "plone.app.querystring.operation.selection.any",
            "v": ["DPDocument"],
        },
        {
            "i": "created",
            "o": "plone.app.querystring.operation.date.today",
            "v": "",
        },
        {
            "i": "OperationMode",
            "o": "plone.app.querystring.operation.selection.any",
            "v": ["Intensiv", "Routine"],
        },
    ]
    today.text = RichTextValue("", "text/html", "text/x-html-safe")
    today.setLayout("docpool_collection_view")
    log.info('Collection "Dokumente von Heute" angelegt')
    return today


def create_since_yesterday_collection(plonesite):
    container = api.content.get(path="/searches")
    if "yesterday" in container:
        return

    title = "Dokumente seit Gestern"
    description = "Dokumente der letzten 24 Stunden"
    _createObjectByType(
        "Collection", container, id="yesterday", title=title, description=description
    )
    yesterday = container["yesterday"]

    # Set the Collection criteria.
    #: Sort on the Effective date
    yesterday.sort_on = "changed"
    yesterday.sort_reversed = True
    yesterday.relatedItems = []
    #: Query by Type and Review State
    yesterday.query = [
        {
            "i": "portal_type",
            "o": "plone.app.querystring.operation.selection.any",
            "v": ["DPDocument"],
        },
        {
            "i": "creationDate",
            "o": "plone.app.querystring.operation.date.largerThanRelativeDate",
            "v": "-1",
        },
        {
            "i": "OperationMode",
            "o": "plone.app.querystring.operation.selection.any",
            "v": ["Intensiv", "Routine"],
        },
    ]
    yesterday.text = RichTextValue("", "text/html", "text/x-html-safe")
    yesterday.setLayout("docpool_collection_view")
    log.info('Collection "Dokumente seit Gestern" angelegt')
    return yesterday


def create_purpose_collections(plonesite):
    container = api.content.get(path="/searches")
    if "bundesmessnetze" in container:
        return
    title = "Standard-Info Bundesmessnetze"
    description = "Standard-Info Bundesmessnetze"
    _createObjectByType(
        "Collection",
        container,
        id="bundesmessnetze",
        title=title,
        description=description,
    )
    iwas = container["bundesmessnetze"]

    # Set the Collection criteria.
    #: Sort on the Effective date
    iwas.sort_on = "effective"
    iwas.sort_reversed = True
    iwas.relatedItems = []
    #: Query by Type and Review State
    iwas.query = [
        {
            "i": "portal_type",
            "o": "plone.app.querystring.operation.selection.any",
            "v": ["DPDocument"],
        },
        {
            "i": "Purpose",
            "o": "plone.app.querystring.operation.string.is",
            "v": "Standard-Info Bundesmessnetze",
        },
    ]
    iwas.text = RichTextValue(
        "<p>Standard-Info Bundesmessnetze<p>", "text/html", "text/x-html-safe"
    )
    iwas.setLayout("docpool_collection_view")

    title = "Standard-Info DWD"
    description = "Standard-Info DWD"
    _createObjectByType(
        "Collection", container, id="dwd", title=title, description=description
    )
    iwas = container["dwd"]

    # Set the Collection criteria.
    #: Sort on the Effective date
    iwas.sort_on = "effective"
    iwas.sort_reversed = True
    iwas.relatedItems = []
    #: Query by Type and Review State
    iwas.query = [
        {
            "i": "portal_type",
            "o": "plone.app.querystring.operation.selection.any",
            "v": ["DPDocument"],
        },
        {
            "i": "Purpose",
            "o": "plone.app.querystring.operation.string.is",
            "v": "Standard-Info Bundesmessnetze",
        },
    ]
    iwas.text = RichTextValue(
        "<p>Standard-Info DWD<p>", "text/html", "text/x-html-safe"
    )
    iwas.setLayout("docpool_collection_view")
    #

    print("Purpose Collection angelegt")


def create_sample_collections(plonesite):
    container = api.content.get(path="/searches")
    if "boden" in container:
        return
    title = "Ergebnisse Boden"
    description = "Ergebnisse Boden"
    _createObjectByType(
        "Collection", container, id="boden", title=title, description=description
    )
    iwas = container["boden"]

    # Set the Collection criteria.
    #: Sort on the Effective date
    iwas.sort_on = "effective"
    iwas.sort_reversed = True
    iwas.relatedItems = []
    #: Query by Type and Review State
    iwas.query = [
        {
            "i": "portal_type",
            "o": "plone.app.querystring.operation.selection.any",
            "v": ["DPDocument"],
        },
        {
            "i": "SampleTypeId",
            "o": "plone.app.querystring.operation.string.contains",
            "v": "B*",
        },
    ]
    iwas.text = RichTextValue("<p>Ergebnisse Boden<p>", "text/html", "text/x-html-safe")
    iwas.setLayout("docpool_collection_view")

    title = "Ergebnisse Futtermittel"
    description = "Ergebnisse Futtermittel"
    _createObjectByType(
        "Collection", container, id="futter", title=title, description=description
    )
    iwas = container["futter"]

    # Set the Collection criteria.
    #: Sort on the Effective date
    iwas.sort_on = "effective"
    iwas.sort_reversed = True
    iwas.relatedItems = []
    #: Query by Type and Review State
    iwas.query = [
        {
            "i": "portal_type",
            "o": "plone.app.querystring.operation.selection.any",
            "v": ["DPDocument"],
        },
        {
            "i": "SampleTypeId",
            "o": "plone.app.querystring.operation.string.contains",
            "v": "F*",
        },
    ]
    iwas.text = RichTextValue(
        "<p>Ergebnisse Futtermittel<p>", "text/html", "text/x-html-safe"
    )
    iwas.setLayout("docpool_collection_view")

    title = "Ergebnisse Gewaesser"
    description = "Ergebnisse Gewaesser"
    _createObjectByType(
        "Collection", container, id="wasser", title=title, description=description
    )
    iwas = container["wasser"]

    # Set the Collection criteria.
    #: Sort on the Effective date
    iwas.sort_on = "effective"
    iwas.sort_reversed = True
    iwas.relatedItems = []
    #: Query by Type and Review State
    iwas.query = [
        {
            "i": "portal_type",
            "o": "plone.app.querystring.operation.selection.any",
            "v": ["DPDocument"],
        },
        {
            "i": "SampleTypeId",
            "o": "plone.app.querystring.operation.string.contains",
            "v": "G*",
        },
    ]
    iwas.text = RichTextValue(
        "<p>Ergebnisse Gewaesser<p>", "text/html", "text/x-html-safe"
    )
    iwas.setLayout("docpool_collection_view")

    title = "Ergebnisse Luft"
    description = "Ergebnisse Luft"
    _createObjectByType(
        "Collection", container, id="luft", title=title, description=description
    )
    iwas = container["luft"]

    # Set the Collection criteria.
    #: Sort on the Effective date
    iwas.sort_on = "effective"
    iwas.sort_reversed = True
    iwas.relatedItems = []
    #: Query by Type and Review State
    iwas.query = [
        {
            "i": "portal_type",
            "o": "plone.app.querystring.operation.selection.any",
            "v": ["DPDocument"],
        },
        {
            "i": "SampleTypeId",
            "o": "plone.app.querystring.operation.string.contains",
            "v": "L*",
        },
    ]
    iwas.text = RichTextValue("<p>Ergebnisse Luft<p>", "text/html", "text/x-html-safe")
    iwas.setLayout("docpool_collection_view")

    title = "Ergebnisse Nahrungsmittel"
    description = "Ergebnisse Nahrungsmittel"
    _createObjectByType(
        "Collection", container, id="nahrung", title=title, description=description
    )
    iwas = container["nahrung"]

    # Set the Collection criteria.
    #: Sort on the Effective date
    iwas.sort_on = "effective"
    iwas.sort_reversed = True
    iwas.relatedItems = []
    #: Query by Type and Review State
    iwas.query = [
        {
            "i": "portal_type",
            "o": "plone.app.querystring.operation.selection.any",
            "v": ["DPDocument"],
        },
        {
            "i": "SampleTypeId",
            "o": "plone.app.querystring.operation.string.contains",
            "v": "N*",
        },
    ]
    iwas.text = RichTextValue(
        "<p>Ergebnisse Nahrungsmittel<p>", "text/html", "text/x-html-safe"
    )
    iwas.setLayout("docpool_collection_view")

    title = "Ergebnisse Stoerfall"
    description = "Ergebnisse Stoerfall"
    _createObjectByType(
        "Collection", container, id="stoer", title=title, description=description
    )
    iwas = container["stoer"]

    # Set the Collection criteria.
    #: Sort on the Effective date
    iwas.sort_on = "effective"
    iwas.sort_reversed = True
    iwas.relatedItems = []
    #: Query by Type and Review State
    iwas.query = [
        {
            "i": "portal_type",
            "o": "plone.app.querystring.operation.selection.any",
            "v": ["DPDocument"],
        },
        {
            "i": "SampleTypeId",
            "o": "plone.app.querystring.operation.string.contains",
            "v": "S*",
        },
    ]
    iwas.text = RichTextValue(
        "<p>Ergebnisse Stoerfall<p>", "text/html", "text/x-html-safe"
    )
    iwas.setLayout("docpool_collection_view")

    print("Sample Type Collection angelegt")


BASICSTRUCTURE = [
    {
        TYPE: "Folder",
        TITLE: "Predefined Searches",
        ID: "searches",
        # TODO: relatedItems broken when creating a doksys docpool.
        # See https://redmine-koala.bfs.de/issues/3291
        # and https://redmine-koala.bfs.de/issues/3350
        # 'relatedItems': PersistentList(),
        CHILDREN: [
            #            {
            #                TYPE: 'Folder',
            #                TITLE: 'Ordner',
            #                ID: 'lastday'
            #            }
        ],  # TODO: further folders filled with Doksys Collections
    }
    # {
    #    TYPE: 'DPInfos', # when type is available
    #     TITLE: 'Infos',
    #     ID: 'doksys-infos',
    #     CHILDREN: [
    #         {
    #             TYPE: 'InfoFolder',
    #             TITLE: 'Infos zu...',
    #             ID: 'info1'
    #         }
    #     ],
    # }
]

# doctypes definitions
# uncomment when when elan.py is removed from dokpool.config.general
# CHANGE HERE. DocTypes, DocCollections and their connections must match.
# Not all DocTypes have doksys behavior

DTYPES = [
    {
        TYPE: "DocType",
        TITLE: "DoksysDokument",
        ID: "doksysdok",
        CHILDREN: [],
        "local_behaviors": ["doksys"],
    },
    #         {TYPE: 'DocType', TITLE: u'Meldung', ID: 'notification',
    #           CHILDREN: [], 'local_behaviors': ['elan']},
    #         {TYPE: 'DocType', TITLE: u'Mitteilung', ID: 'note',
    #           CHILDREN: [], 'local_behaviors': ['elan']},
    #         {TYPE: 'DocType', TITLE: u'Ereignisinformation', ID: 'eventinformation',
    #           CHILDREN: [], 'local_behaviors': ['elan']},
    #         {TYPE: 'DocType', TITLE: u'Anlageninformation', ID: 'nppinformation',
    #           CHILDREN: [], 'local_behaviors': ['elan']},
    #         {TYPE: 'DocType', TITLE: u'Wetterinformation', ID: 'weatherinformation',
    #           CHILDREN: [], 'local_behaviors': ['elan']},
    #         {TYPE: 'DocType', TITLE: u'Trajektorie', ID: 'trajectory',
    #           CHILDREN: [], 'local_behaviors': ['elan', 'doksys']},
    #         {TYPE: 'DocType', TITLE: u'RODOS_Prognose', ID: 'rodosprojection',
    #           CHILDREN: [], 'local_behaviors': ['elan']},
    #         {TYPE: 'DocType', TITLE: u'Andere_Prognose', ID: 'otherprojection',
    #           CHILDREN: [], 'local_behaviors': ['elan']},
    #         {TYPE: 'DocType', TITLE: u'Messergebnis_ODL', ID: 'gammadoserate',
    #           CHILDREN: [], 'local_behaviors': ['elan', 'doksys']},
    #         {TYPE: 'DocType', TITLE: u'Messergebnis_ODL_Zeitreihe', ID: 'gammadoserate_timeseries',
    #           CHILDREN: [], 'local_behaviors': ['elan', 'doksys']},
    #         {TYPE: 'DocType', TITLE: u'Messergebnis_ODL_Messspur', ID: 'gammadoserate_mobile',
    #           CHILDREN: [], 'local_behaviors': ['elan', 'doksys']},
    #         {TYPE: 'DocType', TITLE: u'Messergebnis_Luftaktivität', ID: 'airactivity',
    #           CHILDREN: [], 'local_behaviors': ['elan', 'doksys']},
    #         {TYPE: 'DocType', TITLE: u'Messergebnis_insitu', ID: 'mresult_insitu',
    #           CHILDREN: [], 'local_behaviors': ['elan', 'doksys']},
    #         {TYPE: 'DocType', TITLE: u'Messergebnis_Bodenkontamination', ID: 'groundcontamination',
    #           CHILDREN: [], 'local_behaviors': ['elan', 'doksys']},
    #         {TYPE: 'DocType', TITLE: u'Messergebnis_Futtermittel', ID: 'mresult_feed',
    #           CHILDREN: [], 'local_behaviors': ['elan', 'doksys']},
    #         {TYPE: 'DocType', TITLE: u'Messergebnis_Lebensmittel', ID: 'mresult_food',
    #           CHILDREN: [], 'local_behaviors': ['elan', 'doksys']},
    #         {TYPE: 'DocType', TITLE: u'Messergebnis_Gewässer', ID: 'mresult_water',
    #           CHILDREN: [], 'local_behaviors': ['elan', 'doksys']},
    #         {TYPE: 'DocType', TITLE: u'Messergebnis_Sonstige', ID: 'mresult_other',
    #           CHILDREN: [], 'local_behaviors': ['elan', 'doksys']},
    #         {TYPE: 'DocType', TITLE: u'Messergebnis_Aerogamma', ID: 'mresult_flight',
    #           CHILDREN: [], 'local_behaviors': ['elan', 'doksys']},
    #         {TYPE: 'DocType', TITLE: u'Lageinformation', ID: 'situationreport',
    #           CHILDREN: [], 'local_behaviors': ['elan']},
    #         {TYPE: 'DocType', TITLE: u'Lagebericht', ID: 'sitrep',
    #           CHILDREN: [], 'local_behaviors': ['elan']},
    #         {TYPE: 'DocType', TITLE: u'Bewertung', ID: 'estimation',
    #           CHILDREN: [], 'local_behaviors': ['elan']},
    #         {TYPE: 'DocType', TITLE: u'Maßnahmeninformation', ID: 'instructions',
    #           CHILDREN: [], 'local_behaviors': ['elan'},
    #         {TYPE: 'DocType', TITLE: u'Maßnahmenempfehlungen', ID: 'protectiveactions',
    #           CHILDREN: [], 'local_behaviors': ['elan']},
    #         {TYPE: 'DocType', TITLE: u'Medieninformation', ID: 'mediarelease',
    #           CHILDREN: [], 'local_behaviors': ['elan']},
    #         {TYPE: 'DocType', TITLE: u'FBE_Information', ID: 'information_expert_advisor',
    #           CHILDREN: [], 'local_behaviors': ['elan']},
    #         {TYPE: 'DocType', TITLE: u'Messauftrag', ID: 'measurement_order',
    #           CHILDREN: [], 'local_behaviors': ['elan']},
    #         {TYPE: 'DocType', TITLE: u'Einsatzkarte', ID: 'operation_map',
    #           CHILDREN: [], 'local_behaviors': ['elan'},
    #         {TYPE: 'DocType', TITLE: u'Spezielle_Messanforderungen', ID: 'measurement_requirements',
    #           CHILDREN: [], 'local_behaviors': ['elan']},
    #         {TYPE: 'DocType', TITLE: u'Mitteilung_Messdienste', ID: 'note_measurement_teams',
    #           CHILDREN: [], 'local_behaviors': ['elan']},
    #         {TYPE: 'DocType', TITLE: u'Rückfrage_Messauftrag', ID: 'inquiry_measurement_order',
    #           CHILDREN: [], 'local_behaviors': ['elan']},
    #         {TYPE: 'DocType', TITLE: u'Information_Notfallstationen', ID: 'info_ecc',
    #           CHILDREN: [], 'local_behaviors': ['elan']},
    #         {TYPE: 'DocType', TITLE: u'Information_Bevölkerung', ID: 'info_public',
    #           CHILDREN: [], 'local_behaviors': ['elan']},
    #         {TYPE: 'DocType', TITLE: u'Medienbericht', ID: 'mediareport',
    #           CHILDREN: [], 'local_behaviors': ['elan']},
    #         {TYPE: 'DocType', TITLE: u'Prognose_LASAIR_LASAT', ID: 'lasair_lasat_projection',
    #           CHILDREN: [], 'local_behaviors': ['elan']},
    #         {TYPE: 'DocType', TITLE: u'RODOS Lauf', ID: 'rodosrun_elan',
    #           CHILDREN: [], 'local_behaviors': ['elan']}
]
