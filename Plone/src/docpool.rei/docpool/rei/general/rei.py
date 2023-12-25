from docpool.base.localbehavior.localbehavior import ILocalBehaviorSupport
from docpool.config.utils import CHILDREN
from docpool.config.utils import createPloneObjects
from docpool.config.utils import ID
from docpool.config.utils import TITLE
from docpool.config.utils import TYPE
from docpool.rei.config import REI_APP
from plone import api
from plone.app.textfield.value import RichTextValue
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import _createObjectByType

import transaction


def install(plonesite):
    """ """
    fresh = True
    if plonesite.hasObject("rei"):
        fresh = False  # It's a reinstall
    configUsers(plonesite, fresh)
    createStructure(plonesite, fresh)


def configUsers(plonesite, fresh):
    """ """
    if fresh:
        mtool = getToolByName(plonesite, "portal_membership")
        mtool.addMember(
            "reiadmin",
            "REI Administrator (global)",
            ["Site Administrator", "Member"],
            [],
        )
        reiadmin = mtool.getMemberById("reiadmin")
        reiadmin.setMemberProperties({"fullname": "REI Administrator"})
        reiadmin.setSecurityProfile(password="admin")
        mtool.addMember("reimanager", "REI Manager (global)", ["Manager", "Member"], [])
        reimanager = mtool.getMemberById("reimanager")
        reimanager.setMemberProperties({"fullname": "REI Manager"})
        reimanager.setSecurityProfile(password="admin")
        # Role from rolemap.xml
        api.user.grant_roles(username="reimanager", roles=["REIUser"])
        api.user.grant_roles(username="reiadmin", roles=["REIUser"])
        api.user.grant_roles(username="dpmanager", roles=["REIUser"])
        api.user.grant_roles(username="dpadmin", roles=["REIUser"])


def createStructure(plonesite, fresh):
    changeREINavigation(plonesite, fresh)
    s = api.content.get(path="/berichte")
    s.relatedItems = []
    s.manage_addProperty("text", "", "string")
    transaction.commit()
    create_all_collection(plonesite)
    create_all_private_collection(plonesite)
    transaction.commit()
    changeREIDocTypes(plonesite, fresh)
    transaction.commit()


def createREINavigation(plonesite, fresh):
    createPloneObjects(plonesite, BASICSTRUCTURE, fresh)
    #    create_all_private_collection(plonesite)
    create_all_collection(plonesite)
    print("struktur angelegt")


def createREIDocTypes(plonesite, fresh):
    createPloneObjects(plonesite.config.dtypes, DTYPES, fresh)
    print("REI Bericht angelegt")


def changeREINavigation(plonesite, fresh):
    createPloneObjects(plonesite, BASICSTRUCTURE, fresh)


def changeREIDocTypes(plonesite, fresh):
    createPloneObjects(plonesite.config.dtypes, DTYPES, fresh)


def create_all_collection(plonesite):
    container = api.content.get(path="/berichte")
    #    container.manage_addProperty('text', '', 'string')
    title = "Alle"
    description = "Alle REI Berichte"
    _createObjectByType(
        "Collection", container, id="all", title=title, description=description
    )
    new = container["all"]
    ILocalBehaviorSupport(new).local_behaviors = [REI_APP]

    # Set the Collection criteria.
    #: Sort on the Modification date
    new.sort_on = "modified"
    new.sort_reversed = True
    new.relatedItems = []
    #: Query by Type
    new.query = [
        {
            "i": "dp_type",
            "o": "plone.app.querystring.operation.selection.is",
            "v": ["reireport"],
        },
        {
            "i": "review_state",
            "o": "plone.app.querystring.operation.selection.any",
            "v": [
                "published",
                "pending_bmu",
                "pending_bfs",
                "pending_authority",
                "private",
            ],
        },
    ]
    new.text = RichTextValue("<p>Alle Reiberichte<p>", "text/html", "text/x-html-safe")

    new.setLayout("docpool_collection_view")

    print("Collection Alle angelegt")


def create_all_private_collection(plonesite):
    container = api.content.get(path="/berichte")

    title = "noch nicht freigegeben"
    description = "noch nicht freigegeben REI Berichte"
    _createObjectByType(
        "Collection", container, id="allprivate", title=title, description=description
    )
    new = container["allprivate"]
    ILocalBehaviorSupport(new).local_behaviors = [REI_APP]

    # Set the Collection criteria.
    #: Sort on the Modification date
    new.sort_on = "modified"
    new.sort_reversed = True
    new.relatedItems = []
    #: Query by Type and Review State
    new.query = [
        {
            "i": "dp_type",
            "o": "plone.app.querystring.operation.selection.is",
            "v": ["reireport"],
        },
        {
            "i": "review_state",
            "o": "plone.app.querystring.operation.selection.any",
            "v": ["pending_bfs", "pending_bmu", "pending_authority", "private"],
        },
    ]
    new.text = RichTextValue("<p>Noch freizugeben<p>", "text/html", "text/x-html-safe")

    new.setLayout("docpool_collection_view_with_actions")

    print("Collection Alle eingereicht angelegt")


BASICSTRUCTURE = [
    {
        TYPE: "Folder",
        TITLE: "REI Berichte",
        ID: "berichte",
        CHILDREN: [],  # TODO: further folders filled with REI Collections
    }
    # {
    #     TYPE: 'DPInfos', # when type is available
    #     TITLE: 'Infos',
    #     ID: 'rei-infos',
    #     CHILDREN: [
    #         {
    #             TYPE: 'InfoFolder',
    #             TITLE: 'Infos zu...',
    #             ID: 'info1'
    #         }
    #     ],
    # }
]

DTYPES = [
    {
        TYPE: "DocType",
        TITLE: "REI_Bericht",
        ID: "reireport",
        CHILDREN: [],
        "local_behaviors": ["rei"],
    }
]
