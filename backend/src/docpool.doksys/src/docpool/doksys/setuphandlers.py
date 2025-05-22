from docpool.base.localbehavior.localbehavior import ILocalBehaviorSupport
from docpool.base.marker import IImportingMarker
from docpool.config.utils import CHILDREN
from docpool.config.utils import createPloneObjects
from docpool.config.utils import ID
from docpool.config.utils import TITLE
from docpool.config.utils import TYPE
from docpool.doksys.config import DOKSYS_APP
from plone import api
from plone.app.textfield.value import RichTextValue
from Products.CMFPlone.interfaces import INonInstallable
from Products.CMFPlone.utils import _createObjectByType
from zope.component.hooks import getSite
from zope.globalrequest import getRequest
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
    if IImportingMarker.providedBy(getRequest()):
        return
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
    _createObjectByType("Collection", container, id="today", title=title, description=description)
    new = container["today"]
    ILocalBehaviorSupport(new).local_behaviors = [DOKSYS_APP]

    # Set the Collection criteria.
    #: Sort on the Effective date
    new.sort_on = "changed"
    new.sort_reversed = True
    new.relatedItems = []
    #: Query by Type and Review State
    new.query = [
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
    new.text = RichTextValue("", "text/html", "text/x-html-safe")
    new.setLayout("docpool_collection_view")
    log.info('Collection "Dokumente von Heute" angelegt')
    return new


def create_since_yesterday_collection(plonesite):
    container = api.content.get(path="/searches")
    if "yesterday" in container:
        return

    title = "Dokumente seit Gestern"
    description = "Dokumente der letzten 24 Stunden"
    _createObjectByType("Collection", container, id="yesterday", title=title, description=description)
    new = container["yesterday"]
    ILocalBehaviorSupport(new).local_behaviors = [DOKSYS_APP]

    # Set the Collection criteria.
    #: Sort on the Effective date
    new.sort_on = "changed"
    new.sort_reversed = True
    new.relatedItems = []
    #: Query by Type and Review State
    new.query = [
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
    new.text = RichTextValue("", "text/html", "text/x-html-safe")
    new.setLayout("docpool_collection_view")
    log.info('Collection "Dokumente seit Gestern" angelegt')
    return new


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
    new = container["bundesmessnetze"]
    ILocalBehaviorSupport(new).local_behaviors = [DOKSYS_APP]

    # Set the Collection criteria.
    #: Sort on the Effective date
    new.sort_on = "effective"
    new.sort_reversed = True
    new.relatedItems = []
    #: Query by Type and Review State
    new.query = [
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
    new.text = RichTextValue("<p>Standard-Info Bundesmessnetze<p>", "text/html", "text/x-html-safe")
    new.setLayout("docpool_collection_view")

    title = "Standard-Info DWD"
    description = "Standard-Info DWD"
    _createObjectByType("Collection", container, id="dwd", title=title, description=description)
    new = container["dwd"]
    ILocalBehaviorSupport(new).local_behaviors = [DOKSYS_APP]

    # Set the Collection criteria.
    #: Sort on the Effective date
    new.sort_on = "effective"
    new.sort_reversed = True
    new.relatedItems = []
    #: Query by Type and Review State
    new.query = [
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
    new.text = RichTextValue("<p>Standard-Info DWD<p>", "text/html", "text/x-html-safe")
    new.setLayout("docpool_collection_view")
    #

    print("Purpose Collection angelegt")


def create_sample_collections(plonesite):
    container = api.content.get(path="/searches")
    if "boden" in container:
        return
    title = "Ergebnisse Boden"
    description = "Ergebnisse Boden"
    _createObjectByType("Collection", container, id="boden", title=title, description=description)
    new = container["boden"]
    ILocalBehaviorSupport(new).local_behaviors = [DOKSYS_APP]

    # Set the Collection criteria.
    #: Sort on the Effective date
    new.sort_on = "effective"
    new.sort_reversed = True
    new.relatedItems = []
    #: Query by Type and Review State
    new.query = [
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
    new.text = RichTextValue("<p>Ergebnisse Boden<p>", "text/html", "text/x-html-safe")
    new.setLayout("docpool_collection_view")

    title = "Ergebnisse Futtermittel"
    description = "Ergebnisse Futtermittel"
    _createObjectByType("Collection", container, id="futter", title=title, description=description)
    new = container["futter"]
    ILocalBehaviorSupport(new).local_behaviors = [DOKSYS_APP]

    # Set the Collection criteria.
    #: Sort on the Effective date
    new.sort_on = "effective"
    new.sort_reversed = True
    new.relatedItems = []
    #: Query by Type and Review State
    new.query = [
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
    new.text = RichTextValue("<p>Ergebnisse Futtermittel<p>", "text/html", "text/x-html-safe")
    new.setLayout("docpool_collection_view")

    title = "Ergebnisse Gewaesser"
    description = "Ergebnisse Gewaesser"
    _createObjectByType("Collection", container, id="wasser", title=title, description=description)
    new = container["wasser"]
    ILocalBehaviorSupport(new).local_behaviors = [DOKSYS_APP]

    # Set the Collection criteria.
    #: Sort on the Effective date
    new.sort_on = "effective"
    new.sort_reversed = True
    new.relatedItems = []
    #: Query by Type and Review State
    new.query = [
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
    new.text = RichTextValue("<p>Ergebnisse Gewaesser<p>", "text/html", "text/x-html-safe")
    new.setLayout("docpool_collection_view")

    title = "Ergebnisse Luft"
    description = "Ergebnisse Luft"
    _createObjectByType("Collection", container, id="luft", title=title, description=description)
    new = container["luft"]
    ILocalBehaviorSupport(new).local_behaviors = [DOKSYS_APP]

    # Set the Collection criteria.
    #: Sort on the Effective date
    new.sort_on = "effective"
    new.sort_reversed = True
    new.relatedItems = []
    #: Query by Type and Review State
    new.query = [
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
    new.text = RichTextValue("<p>Ergebnisse Luft<p>", "text/html", "text/x-html-safe")
    new.setLayout("docpool_collection_view")

    title = "Ergebnisse Nahrungsmittel"
    description = "Ergebnisse Nahrungsmittel"
    _createObjectByType("Collection", container, id="nahrung", title=title, description=description)
    new = container["nahrung"]
    ILocalBehaviorSupport(new).local_behaviors = [DOKSYS_APP]

    # Set the Collection criteria.
    #: Sort on the Effective date
    new.sort_on = "effective"
    new.sort_reversed = True
    new.relatedItems = []
    #: Query by Type and Review State
    new.query = [
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
    new.text = RichTextValue("<p>Ergebnisse Nahrungsmittel<p>", "text/html", "text/x-html-safe")
    new.setLayout("docpool_collection_view")

    title = "Ergebnisse Stoerfall"
    description = "Ergebnisse Stoerfall"
    _createObjectByType("Collection", container, id="stoer", title=title, description=description)
    new = container["stoer"]
    ILocalBehaviorSupport(new).local_behaviors = [DOKSYS_APP]

    # Set the Collection criteria.
    #: Sort on the Effective date
    new.sort_on = "effective"
    new.sort_reversed = True
    new.relatedItems = []
    #: Query by Type and Review State
    new.query = [
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
    new.text = RichTextValue("<p>Ergebnisse Stoerfall<p>", "text/html", "text/x-html-safe")
    new.setLayout("docpool_collection_view")

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
]
