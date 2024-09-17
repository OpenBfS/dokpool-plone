from docpool.config.utils import CHILDREN
from docpool.config.utils import createPloneObjects
from docpool.config.utils import ID
from docpool.config.utils import TITLE
from docpool.config.utils import TYPE
from plone import api
from Products.CMFCore.utils import getToolByName

import transaction


def install(plonesite):
    """ """
    fresh = True
    if plonesite.hasObject("potentially-affected-areas"):
        fresh = False  # It's a reinstall
    # configUsers(plonesite, fresh)
    createStructure(plonesite, fresh)


def configUsers(plonesite, fresh):
    """ """
    if fresh:
        mtool = getToolByName(plonesite, "portal_membership")
        mtool.addMember(
            "rodosadmin",
            "RODOS Administrator (global)",
            ["Site Administrator", "Member"],
            [],
        )
        rodosadmin = mtool.getMemberById("rodosadmin")
        rodosadmin.setMemberProperties({"fullname": "RODOS Administrator"})
        rodosadmin.setSecurityProfile(password="admin")
        mtool.addMember(
            "rodosmanager", "RODOS Manager (global)", ["Manager", "Member"], []
        )
        rodosmanager = mtool.getMemberById("rodosmanager")
        rodosmanager.setMemberProperties({"fullname": "RODOS Manager"})
        rodosmanager.setSecurityProfile(password="admin")
        # Role from rolemap.xml
        api.user.grant_roles(username="rodosmanager", roles=["RodosUser"])
        api.user.grant_roles(username="rodosadmin", roles=["RodosUser"])
        api.user.grant_roles(username="dpmanager", roles=["RodosUser"])
        api.user.grant_roles(username="dpadmin", roles=["RodosUser"])


def createStructure(plonesite, fresh):
    createRodosNavigation(plonesite, fresh)
    transaction.commit()
    createRodosDocTypes(plonesite, fresh)
    transaction.commit()


def createRodosNavigation(plonesite, fresh):
    createPloneObjects(plonesite, BASICSTRUCTURE, fresh)


def createRodosDocTypes(plonesite, fresh):
    createPloneObjects(plonesite.config.dtypes, DTYPES, fresh)


DOCTYPES = "ref_setDocTypesUpdateCollection"  # indicates that docTypes is referencing objects, which need to be queried by their id


dp_type_query = {
    "i": "dp_type",
    "o": "plone.app.querystring.operation.selection.is",
    "v": ["rodosprojection"],
}

prognosis_type_query = {
    "i": "PrognosisType",
    "o": "plone.app.querystring.operation.selection.is",
    "v": ["Potenziell betroffene Gebiete"],
}


def make_title_query(title):
    return {
        "i": "Title",
        "o": "plone.app.querystring.operation.string.contains",
        "v": title,
    }


AREAS = [
    "ISAR",
    "GUNDREMMINGEN",
    "PHILIPPSBURG",
    "NECKARWESTHEIM",
    "EMSLAND",
    "GROHNDE",
    "BROKDORF",
    "FR-MUENCHEN",
    "FR-BERLIN",
    "LEIBSTADT",
    "GOESGEN",
    "BEZNAU",
    "MUEHLEBERG",
    "CATTENOM",
    "FESSENHEIM",
    "CHOOZ",
    "TIHANGE",
    "TEMELIN",
    "mobiler Standort",
]


AREAS_COLLECTIONS = [
    {
        TYPE: "Collection",
        TITLE: area,
        ID: area.lower(),
        "local_behaviors": ["rodos"],
        "query": [
            dp_type_query,
            prognosis_type_query,
            make_title_query(area),
        ],
    }
    for area in AREAS
]


BASICSTRUCTURE = [
    {
        TYPE: "Folder",
        TITLE: "Potenziell betroffenen Gebiete",
        ID: "potentially-affected-areas",
        "local_behaviors": ["rodos"],
        CHILDREN: [
            {
                TYPE: "Collection",
                TITLE: "Alle",
                ID: "all",
                "local_behaviors": ["rodos"],
                "query": [dp_type_query, prognosis_type_query],
            }
        ]
        + AREAS_COLLECTIONS,
    },
    {
        TYPE: "Folder",
        TITLE: "Ausbreitungsrechnungen",
        ID: "projections",
        "local_behaviors": ["rodos"],
        CHILDREN: [
            {
                TYPE: "Collection",
                TITLE: "Alle",
                ID: "all",
                "local_behaviors": ["rodos"],
                "query": [
                    dp_type_query,
                    {
                        "i": "PrognosisType",
                        "o": "plone.app.querystring.operation.selection.any",
                        "v": [
                            "RODOS Prognose",
                            "DWD Ausbreitungsrechnung ab Quelle",
                            "LASAIR/LASAT",
                            "Sonstige Ausbreitungsrechnung",
                        ],
                    },
                ],
            },
            {
                TYPE: "Collection",
                TITLE: "RODOS-Prognosen",
                ID: "rodosprojection",
                "local_behaviors": ["rodos"],
                "query": [
                    dp_type_query,
                    {
                        "i": "PrognosisType",
                        "o": "plone.app.querystring.operation.selection.is",
                        "v": ["RODOS Prognose"],
                    },
                ],
            },
            {
                TYPE: "Collection",
                TITLE: "DWD-Ausbreitungsrechnungen ab Quelle",
                ID: "dwd-ausbreitungsrechnungen",
                "local_behaviors": ["rodos"],
                "query": [
                    dp_type_query,
                    {
                        "i": "PrognosisType",
                        "o": "plone.app.querystring.operation.selection.is",
                        "v": ["DWD Ausbreitungsrechnung ab Quelle"],
                    },
                ],
            },
            {
                TYPE: "Collection",
                TITLE: "LASAIR/LASAT",
                ID: "lasair-lasat",
                "local_behaviors": ["rodos"],
                "query": [
                    dp_type_query,
                    {
                        "i": "PrognosisType",
                        "o": "plone.app.querystring.operation.selection.is",
                        "v": ["LASAIR/LASAT"],
                    },
                ],
            },
            {
                TYPE: "Collection",
                TITLE: "Sonstige Ausbreitungsrechnungen",
                ID: "sonstige-ausbreitungsrechnungen",
                "local_behaviors": ["rodos"],
                "query": [
                    dp_type_query,
                    {
                        "i": "PrognosisType",
                        "o": "plone.app.querystring.operation.selection.is",
                        "v": ["Sonstige Ausbreitungsrechnung"],
                    },
                ],
            },
        ],
    },
]


DTYPES = [
    {
        TYPE: "DocType",
        TITLE: "RODOS Rechnung",
        ID: "rodosprojection",
        CHILDREN: [],
        "local_behaviors": ["rodos", "elan"],
        "ref_allowedDocTypes": [],
    },
]

# TODO: run this code...
# try:
#     self.config.dtypes.rodosprojection.type_extension(ELAN_APP).setCCategory(
#         "rodos-projections"
#     )
# except BaseException:
#     pass
