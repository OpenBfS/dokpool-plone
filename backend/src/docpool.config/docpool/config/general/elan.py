from docpool.config.utils import CHILDREN
from docpool.config.utils import createPloneObjects
from docpool.config.utils import ID
from docpool.config.utils import TITLE
from docpool.config.utils import TYPE
from plone import api
from Products.CMFCore.utils import getToolByName

import transaction


def install(self):
    """ """
    fresh = True
    if self.hasObject("contentconfig"):
        fresh = False  # It's a reinstall
    configUsers(self, fresh)
    createStructure(self, fresh)


def configUsers(self, fresh):
    """ """
    if fresh:
        mtool = getToolByName(self, "portal_membership")
        mtool.addMember(
            "elanadmin",
            "ELAN Administrator (global)",
            ["Site Administrator", "Member"],
            [],
        )
        elanadmin = mtool.getMemberById("elanadmin")
        elanadmin.setMemberProperties({"fullname": "ELAN Administrator"})
        elanadmin.setSecurityProfile(password="admin")
        mtool.addMember("elanmanager", "ELAN Manager (global)", ["Manager", "Member"], [])
        elanmanager = mtool.getMemberById("elanmanager")
        elanmanager.setMemberProperties({"fullname": "ELAN Manager"})
        elanmanager.setSecurityProfile(password="admin")
        api.user.grant_roles(username="elanmanager", roles=["ELANUser"])
        api.user.grant_roles(username="elanadmin", roles=["ELANUser"])
        api.user.grant_roles(username="dpmanager", roles=["ELANUser"])
        api.user.grant_roles(username="dpadmin", roles=["ELANUser"])


def createStructure(self, fresh):
    createBasicPortalStructure(self, fresh)
    transaction.commit()
    createDocTypes(self, fresh)
    transaction.commit()


def createDocTypes(plonesite, fresh):
    """ """
    createPloneObjects(plonesite.config.dtypes, DTYPES, fresh)


def createBasicPortalStructure(plonesite, fresh):
    """ """
    createPloneObjects(plonesite, BASICSTRUCTURE, fresh)


BASICSTRUCTURE = [
    {
        TYPE: "ELANContentConfig",
        TITLE: "Konfiguration Inhalte",
        ID: "contentconfig",
        CHILDREN: [
            {TYPE: "Text", TITLE: "Impressum", ID: "impressum", CHILDREN: []},
        ],
    },
]

# Structure definitions

DTYPES = [
    {
        TYPE: "DocType",
        TITLE: "Meldung",
        ID: "notification",
        CHILDREN: [],
        "local_behaviors": ["elan"],
    },
    {
        TYPE: "DocType",
        TITLE: "Mitteilung",
        ID: "note",
        CHILDREN: [],
        "local_behaviors": ["elan"],
    },
    {
        TYPE: "DocType",
        TITLE: "Ereignisinformation",
        ID: "eventinformation",
        CHILDREN: [],
        "local_behaviors": ["elan"],
    },
    {
        TYPE: "DocType",
        TITLE: "Anlageninformation",
        ID: "nppinformation",
        CHILDREN: [],
        "local_behaviors": ["elan"],
    },
    {
        TYPE: "DocType",
        TITLE: "Wetterinformation",
        ID: "weatherinformation",
        CHILDREN: [],
        "local_behaviors": ["elan"],
    },
    {
        TYPE: "DocType",
        TITLE: "Trajektorie",
        ID: "trajectory",
        CHILDREN: [],
        "local_behaviors": ["elan", "doksys"],
    },
    # {
    #     TYPE: "DocType",
    #     TITLE: "RODOS Rechnung",
    #     ID: "rodosprojection",
    #     CHILDREN: [],
    #     "local_behaviors": ["elan"],
    # },
    {
        TYPE: "DocType",
        TITLE: "Andere_Prognose",
        ID: "otherprojection",
        CHILDREN: [],
        "local_behaviors": ["elan"],
    },
    {
        TYPE: "DocType",
        TITLE: "Messergebnis_ODL",
        ID: "gammadoserate",
        CHILDREN: [],
        "local_behaviors": ["elan", "doksys"],
    },
    {
        TYPE: "DocType",
        TITLE: "Messergebnis_ODL_Zeitreihe",
        ID: "gammadoserate_timeseries",
        CHILDREN: [],
        "local_behaviors": ["elan", "doksys"],
    },
    {
        TYPE: "DocType",
        TITLE: "Messergebnis_ODL_Messspur",
        ID: "gammadoserate_mobile",
        CHILDREN: [],
        "local_behaviors": ["elan", "doksys"],
    },
    {
        TYPE: "DocType",
        TITLE: "Messergebnis_Luftaktivität",
        ID: "airactivity",
        CHILDREN: [],
        "local_behaviors": ["elan", "doksys"],
    },
    {
        TYPE: "DocType",
        TITLE: "Messergebnis_insitu",
        ID: "mresult_insitu",
        CHILDREN: [],
        "local_behaviors": ["elan", "doksys"],
    },
    {
        TYPE: "DocType",
        TITLE: "Messergebnis_Bodenkontamination",
        ID: "groundcontamination",
        CHILDREN: [],
        "local_behaviors": ["elan", "doksys"],
    },
    {
        TYPE: "DocType",
        TITLE: "Messergebnis_Futtermittel",
        ID: "mresult_feed",
        CHILDREN: [],
        "local_behaviors": ["elan", "doksys"],
    },
    {
        TYPE: "DocType",
        TITLE: "Messergebnis_Lebensmittel",
        ID: "mresult_food",
        CHILDREN: [],
        "local_behaviors": ["elan", "doksys"],
    },
    {
        TYPE: "DocType",
        TITLE: "Messergebnis_Gewässer",
        ID: "mresult_water",
        CHILDREN: [],
        "local_behaviors": ["elan", "doksys"],
    },
    {
        TYPE: "DocType",
        TITLE: "Messergebnis_Sonstige",
        ID: "mresult_other",
        CHILDREN: [],
        "local_behaviors": ["elan", "doksys"],
    },
    {
        TYPE: "DocType",
        TITLE: "Messergebnis_Aerogamma",
        ID: "mresult_flight",
        CHILDREN: [],
        "local_behaviors": ["elan", "doksys"],
    },
    {
        TYPE: "DocType",
        TITLE: "Radiologisches Lagebild",
        ID: "situationreport",
        CHILDREN: [],
        "local_behaviors": ["elan"],
    },
    {
        TYPE: "DocType",
        TITLE: "Bewertung",
        ID: "estimation",
        CHILDREN: [],
        "local_behaviors": ["elan"],
    },
    {
        TYPE: "DocType",
        TITLE: "Maßnahmeninformation",
        ID: "instructions",
        CHILDREN: [],
        "local_behaviors": ["elan"],
    },
    {
        TYPE: "DocType",
        TITLE: "Maßnahmenempfehlungen",
        ID: "protectiveactions",
        CHILDREN: [],
        "local_behaviors": ["elan"],
    },
    {
        TYPE: "DocType",
        TITLE: "Medieninformation",
        ID: "mediarelease",
        CHILDREN: [],
        "local_behaviors": ["elan"],
    },
    {
        TYPE: "DocType",
        TITLE: "FBE_Information",
        ID: "information_expert_advisor",
        CHILDREN: [],
        "local_behaviors": ["elan"],
    },
    {
        TYPE: "DocType",
        TITLE: "Messauftrag",
        ID: "measurement_order",
        CHILDREN: [],
        "local_behaviors": ["elan"],
    },
    {
        TYPE: "DocType",
        TITLE: "Einsatzkarte",
        ID: "operation_map",
        CHILDREN: [],
        "local_behaviors": ["elan"],
    },
    {
        TYPE: "DocType",
        TITLE: "Spezielle_Messanforderungen",
        ID: "measurement_requirements",
        CHILDREN: [],
        "local_behaviors": ["elan"],
    },
    {
        TYPE: "DocType",
        TITLE: "Mitteilung_Messdienste",
        ID: "note_measurement_teams",
        CHILDREN: [],
        "local_behaviors": ["elan"],
    },
    {
        TYPE: "DocType",
        TITLE: "Rückfrage_Messauftrag",
        ID: "inquiry_measurement_order",
        CHILDREN: [],
        "local_behaviors": ["elan"],
    },
    {
        TYPE: "DocType",
        TITLE: "Information_Notfallstationen",
        ID: "info_ecc",
        CHILDREN: [],
        "local_behaviors": ["elan"],
    },
    {
        TYPE: "DocType",
        TITLE: "Information_Bevölkerung",
        ID: "info_public",
        CHILDREN: [],
        "local_behaviors": ["elan"],
    },
    {
        TYPE: "DocType",
        TITLE: "Medienbericht",
        ID: "mediareport",
        CHILDREN: [],
        "local_behaviors": ["elan"],
    },
    {
        TYPE: "DocType",
        TITLE: "Prognose_LASAIR_LASAT",
        ID: "lasair_lasat_projection",
        CHILDREN: [],
        "local_behaviors": ["elan"],
    },
    {
        TYPE: "DocType",
        TITLE: "Sonstiges Dokument",
        ID: "other_document",
        CHILDREN: [],
        "local_behaviors": ["elan"],
    },
]
