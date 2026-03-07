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
    doctypes_container = plonesite.config.dtypes
    assert doctypes_container.portal_type == "DocTypes"

    # Create main categories
    for info in DOCTYPES:
        if category_id := info.get("category_id"):
            if category_id in doctypes_container:
                continue
            api.content.create(
                container=doctypes_container,
                type="DocTypeCategory",
                id=category_id,
                title=info["category"],
                icon_name=info["icon"] or "radioactive",
            )
    # Create subcategories
    for info in DOCTYPES:
        if subcategory_id := info.get("subcategory_id"):
            category_container = doctypes_container[info["category_id"]]
            if subcategory_id in category_container:
                continue
            api.content.create(
                container=category_container,
                type="DocTypeSubCategory",
                id=subcategory_id,
                title=info["subcategory"],
                icon_name=info["subcategory_icon"] or "file-richtext",
            )

    # Create DocTypes
    for info in DOCTYPES:
        # Special case Bayern
        # only_bayern = ["radiological_situation_report_draft", "situation_overview_draft"]
        # if info["id"] in only_bayern and dp.id != "bayern":
        #     continue

        # The default doctypes content gets all types
        # TODO: Maybe we need to filter behaviors when moving default types to a docpool
        local_behaviors = info["behaviors"]

        container = doctypes_container
        if category_id := info.get("category_id"):
            container = doctypes_container[info["category_id"]]
            if subcategory_id := info.get("subcategory_id"):
                container = container[subcategory_id]

        if info["id"] in container:
            # Unused case where a doctype already exists
            continue

        # This is new!
        api.content.create(
            container=container,
            type="DocType",
            id=info["id"],
            title=info["title"],
            description=info["description"],
            local_behaviors=local_behaviors,
        )


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

DOCTYPES = [
    {
        "title": "Ergänzende Ereignisinformation",
        "id": "additional_event_information",
        "old_ids": [
            "estimation",
            "eventinformation",
            "info_authorities",
            "information_expert_advisor",
            "nppinformation",
        ],
        "behaviors": ["elan"],
        "description": "Informationen nach § 152 StrlSchV z.B. Daten, Abschätzungen und Bewertungen über die Anlage oder Strahlungsquelle, zum radiologischen Inventar und zu Freisetzungen sowie Freisetzungsabschätzungen und ‑prognosen",
        "icon": "",
        "subcategory": "Ergänzende Ereignisinformationen",
        "subcategory_id": "additional_event_information",
        "subcategory_icon": "",
        "category": "Ereignis",
        "category_id": "incident",
    },
    {
        "title": "DOKSYS-Eintrag",
        "id": "doksys_entry",
        "old_ids": ["doksysdok"],
        "behaviors": ["doksys"],
        "description": "Eintragsart für die DOKSYS-Applikation",
        "icon": "",
        "subcategory": "DOKSYS",
        "subcategory_id": "doksys",
        "subcategory_icon": "",
        "category": "DOKSYS",
        "category_id": "doksys",
    },
    {
        "title": "Prognose über Ausbreitung, Dosis und Kontamination",
        "id": "forecast_spread_dose_contamination",
        "old_ids": ["lasair_lasat_projection", "otherprojection", "rodosprojection"],
        "behaviors": ["elan", "rodos"],
        "description": "(RODOS-) Ausbreitungsrechnung über die prognostizierte Ankunftszeit radioaktiver Luftmassen, die zu erwartende Kontamination der Umwelt oder die zu erwartende Dosis der Bevölkerung unter Berücksichtigung der aktuellen und prognostizierten Wetterbedingungen.",
        "icon": "",
        "subcategory": "Prognosen über Ausbreitung, Dosis und Kontamination",
        "subcategory_id": "forecasts_spread_dose_contamination",
        "subcategory_icon": "",
        "category": "Lagebewältigung",
        "category_id": "incident_management",
    },
    {
        "title": "Information an Bevölkerung",
        "id": "information_for_the_public",
        "old_ids": ["info_public", "mediarelease"],
        "behaviors": ["elan"],
        "description": "Abgestimmte Kommunikationsempfehlung zur Information der Bevölkerung, inklusive eigene Pressemitteilungen",
        "icon": "",
        "subcategory": "Informationen an Bevölkerung",
        "subcategory_id": "information_for_the_public",
        "subcategory_icon": "",
        "category": "Lagebewältigung",
        "category_id": "incident_management",
    },
    {
        "title": "Messempfehlung",
        "id": "measurement_recommendation",
        "old_ids": ["measurement_order"],
        "behaviors": ["elan"],
        "description": "Messempfehlung an Einsatzkräfte des Bundes und der Länder, sowie KHG",
        "icon": "",
        "subcategory": "Messempfehlungen",
        "subcategory_id": "measurement_recommendations",
        "subcategory_icon": "",
        "category": "Lagebewältigung",
        "category_id": "incident_management",
    },
    {
        "title": "Messstrategie",
        "id": "measurement_strategy",
        "old_ids": ["messstrategie"],
        "behaviors": ["elan"],
        "description": "Messstrategie zu einem Radiologischen Lagebild gemäß ANoPl Bund.",
        "icon": "",
        "subcategory": "Messstrategien",
        "subcategory_id": "measurement_strategies",
        "subcategory_icon": "",
        "category": "Lagebewältigung",
        "category_id": "incident_management",
    },
    {
        "title": "Medienbericht",
        "id": "media_report",
        "old_ids": ["mediareport"],
        "behaviors": ["elan"],
        "description": "Mediale Berichterstattung zum Ereignis",
        "icon": "",
        "subcategory": "Medienberichte",
        "subcategory_id": "media_reports",
        "subcategory_icon": "",
        "category": "Ereignis",
        "category_id": "incident",
    },
    {
        "title": "Messergebnis Luft/externe Strahlung (Gamma-ODL)",
        "id": "mresult_air_external_radiation",
        "old_ids": ["gammadoserate_mobile", "gammadoserate_timeseries", "gammadoserate"],
        "behaviors": ["elan"],
        "description": "Messergebnis Luft/externe Strahlung",
        "icon": "",
        "subcategory": "Luft (inklusive Gamma-ODL)",
        "subcategory_id": "mresults_air",
        "subcategory_icon": "",
        "category": "Messergebnisse",
        "category_id": "measurement_results",
    },
    {
        "title": "Messergebnis Luft/freie Atmosphäre",
        "id": "mresult_air_free_atmosphere",
        "old_ids": [],
        "behaviors": ["elan"],
        "description": "Messergebnis Luft/freie AtmosphäreAtmosphäre",
        "icon": "",
        "subcategory": "Luft (inklusive Gamma-ODL)",
        "subcategory_id": "mresults_air",
        "subcategory_icon": "",
        "category": "Messergebnisse",
        "category_id": "measurement_results",
    },
    {
        "title": "Messergebnis Luft/bodennah",
        "id": "mresult_air_near_ground",
        "old_ids": ["airactivity", "mresult_emission", "mresult_flight"],
        "behaviors": ["elan"],
        "description": "Messergebnis Luft/bodennah",
        "icon": "",
        "subcategory": "Luft (inklusive Gamma-ODL)",
        "subcategory_id": "mresults_air",
        "subcategory_icon": "",
        "category": "Messergebnisse",
        "category_id": "measurement_results",
    },
    {
        "title": "Messergebnis Luft/bodennah (Spurenanalyse)",
        "id": "mresult_air_traceanalysis",
        "old_ids": ["mresult_traceanalysis"],
        "behaviors": ["elan"],
        "description": "Messergebnis Luft/Spurenanalyse einschließlich Edelgase",
        "icon": "",
        "subcategory": "Luft (inklusive Gamma-ODL)",
        "subcategory_id": "mresults_air",
        "subcategory_icon": "",
        "category": "Messergebnisse",
        "category_id": "measurement_results",
    },
    {
        "title": "Messergebnis Niederschlag",
        "id": "mresult_precipitation",
        "old_ids": ["mresult_precipitation"],
        "behaviors": ["elan"],
        "description": "Messergebnis Niederschlag",
        "icon": "",
        "subcategory": "Bodenoberfläche und Niederschlag",
        "subcategory_id": "mresults_soil_surface_and_precipitation",
        "subcategory_icon": "",
        "category": "Messergebnisse",
        "category_id": "measurement_results",
    },
    {
        "title": "Messergebnis Biologische Dosimetrie",
        "id": "mresult_biological_dosimetry",
        "old_ids": [],
        "behaviors": ["elan"],
        "description": "Messergebnis Biologische Dosimetrie",
        "icon": "",
        "subcategory": "Inkorporationsüberwachung und biologische Dosimetrie",
        "subcategory_id": "mresults_incorporation_and_biological_dosimetry",
        "subcategory_icon": "",
        "category": "Messergebnisse",
        "category_id": "measurement_results",
    },
    {
        "title": "Messergebnis Grenzüberschreitender Verkehr",
        "id": "mresult_crossborder_traffic",
        "old_ids": [],
        "behaviors": ["elan"],
        "description": "Messergebnis Grenzüberschreitender Verkehr von Personen, Fahrzeugen, Gütern und Gepäck",
        "icon": "",
        "subcategory": "Beförderung von Gütern und grenzüberschreitender Verkehr",
        "subcategory_id": "mresults_transport_of_goods_and_crossborder_traffic",
        "subcategory_icon": "",
        "category": "Messergebnisse",
        "category_id": "measurement_results",
    },
    {
        "title": "Messergebnis Trinkwasser",
        "id": "mresult_drinking_water",
        "old_ids": ["messergebnis_trinkwasser"],
        "behaviors": ["elan"],
        "description": "Messergebnis Trinkwasser",
        "icon": "cup-straw",
        "subcategory": "Trinkwasser und Inverkehrbringen von Lebensmittel, Futtermitteln etc.",
        "subcategory_id": "mresults_drinking_water_and_placing_on_market",
        "subcategory_icon": "cup-straw",
        "category": "Messergebnisse",
        "category_id": "measurement_results",
    },
    {
        "title": "Messergebnis Fisch und Fischereierzeugnisse",
        "id": "mresult_fish",
        "old_ids": [],
        "behaviors": ["elan"],
        "description": "Messergebnis Fisch und Fischereierzeugnisse, Krustentiere, Schalentiere, Meereswasserpflanzen",
        "icon": "water",
        "subcategory": "Gewässer, Fisch und Fischereierzeugnisse",
        "subcategory_id": "mresults_water_bodies_and_fish",
        "subcategory_icon": "water",
        "category": "Messergebnisse",
        "category_id": "measurement_results",
    },
    {
        "title": "Messergebnis Inkorporationsüberwachung",
        "id": "mresult_incorporation_monitoring",
        "old_ids": [],
        "behaviors": ["elan"],
        "description": "Messergebnis Inkorporationsüberwachung",
        "icon": "",
        "subcategory": "Inkorporationsüberwachung und biologische Dosimetrie",
        "subcategory_id": "mresults_incorporation_and_biological_dosimetry",
        "subcategory_icon": "",
        "category": "Messergebnisse",
        "category_id": "measurement_results",
    },
    {
        "title": "Messergebnis Nord- und Ostsee",
        "id": "mresult_north_and_baltic_sea",
        "old_ids": [],
        "behaviors": ["elan"],
        "description": "Messergebnis Nord- und Ostsee einschließlich Küstengewässer",
        "icon": "",
        "subcategory": "Gewässer, Fisch und Fischereierzeugnisse",
        "subcategory_id": "mresults_water_bodies_and_fish",
        "subcategory_icon": "",
        "category": "Messergebnisse",
        "category_id": "measurement_results",
    },
    {
        "title": "Messergebnis Sonstige Oberflächengewässer",
        "id": "mresult_other_surface_waters",
        "old_ids": ["mresult_water"],
        "behaviors": ["elan"],
        "description": "Messergebnis Sonstige Oberflächengewässer",
        "icon": "",
        "subcategory": "Gewässer, Fisch und Fischereierzeugnisse",
        "subcategory_id": "mresults_water_bodies_and_fish",
        "subcategory_icon": "",
        "category": "Messergebnisse",
        "category_id": "measurement_results",
    },
    {
        "title": "Messergebnis Arzneimittel",
        "id": "mresult_pharmaceuticals",
        "old_ids": [],
        "behaviors": ["elan"],
        "description": "Messergebnis Arzneimittel und deren Ausgangsstoffe",
        "icon": "",
        "subcategory": "Arzneimittel",
        "subcategory_id": "mresults_pharmaceuticals",
        "subcategory_icon": "",
        "category": "Messergebnisse",
        "category_id": "measurement_results",
    },
    {
        "title": "Messergebnis Inverkehrbringen",
        "id": "mresult_placing_on_market",
        "old_ids": [],
        "behaviors": ["elan"],
        "description": "Messergebnis Inverkehrbringen von Lebensmitteln, Bedarfsgegenständen, Mitteln zum Tätowieren, kosmetischen Mitteln, Verfüttern oder Inverkehrbringen von Futtermitteln",
        "icon": "",
        "subcategory": "Trinkwasser und Inverkehrbringen von Lebensmittel, Futtermitteln etc.",
        "subcategory_id": "mresults_drinking_water_and_placing_on_market",
        "subcategory_icon": "",
        "category": "Messergebnisse",
        "category_id": "measurement_results",
    },
    {
        "title": "Messergebnis Pflanzliche und tierische Erzeugnisse",
        "id": "mresult_plant_and_animal_products",
        "old_ids": ["mresult_feed", "mresult_food"],
        "behaviors": ["elan"],
        "description": "Messergebnis Produktion pflanzlicher und tierischer Erzeugnisse",
        "icon": "",
        "subcategory": "Boden, repräsentative Medien, pflanzliche und tierische Erzeugnisse",
        "subcategory_id": "mresults_representive_media_and_plant_animal_procucts",
        "subcategory_icon": "",
        "category": "Messergebnisse",
        "category_id": "measurement_results",
    },
    {
        "title": "Messergebnis Repräsentative Medien",
        "id": "mresult_representative_media",
        "old_ids": [],
        "behaviors": ["elan"],
        "description": "Messergebnis Repräsentative Medien",
        "icon": "",
        "subcategory": "Boden, repräsentative Medien, pflanzliche und tierische Erzeugnisse",
        "subcategory_id": "mresults_representive_media_and_plant_animal_procucts",
        "subcategory_icon": "",
        "category": "Messergebnisse",
        "category_id": "measurement_results",
    },
    {
        "title": "Messergebnis Boden",
        "id": "mresult_soil",
        "old_ids": ["groundcontamination"],
        "behaviors": ["elan"],
        "description": "Messergebnis Boden",
        "icon": "",
        "subcategory": "Boden, repräsentative Medien, pflanzliche und tierische Erzeugnisse",
        "subcategory_id": "mresults_representive_media_and_plant_animal_procucts",
        "subcategory_icon": "",
        "category": "Messergebnisse",
        "category_id": "measurement_results",
    },
    {
        "title": "Messergebnis Bodenoberfläche",
        "id": "mresult_soil_surface",
        "old_ids": ["mresult_insitu"],
        "behaviors": ["elan"],
        "description": "Messergebnis Bodenoberfläche",
        "icon": "",
        "subcategory": "Bodenoberfläche und Niederschlag",
        "subcategory_id": "mresults_soil_surface_and_precipitation",
        "subcategory_icon": "",
        "category": "Messergebnisse",
        "category_id": "measurement_results",
    },
    {
        "title": "Messergebnis Beförderung von Gütern",
        "id": "mresult_transport_of_goods",
        "old_ids": [],
        "behaviors": ["elan"],
        "description": "Messergebnis Beförderung von Gütern",
        "icon": "",
        "subcategory": "Beförderung von Gütern und grenzüberschreitender Verkehr",
        "subcategory_id": "mresults_transport_of_goods_and_crossborder_traffic",
        "subcategory_icon": "",
        "category": "Messergebnisse",
        "category_id": "measurement_results",
    },
    {
        "title": "Messergebnis Abfälle",
        "id": "mresult_waste",
        "old_ids": [],
        "behaviors": ["elan"],
        "description": "Messergebnis Abfälle",
        "icon": "",
        "subcategory": "Abfälle, Abwasser und Klärschlamm",
        "subcategory_id": "mresults_waste_and_wastewater",
        "subcategory_icon": "",
        "category": "Messergebnisse",
        "category_id": "measurement_results",
    },
    {
        "title": "Messergebnis Abwasser und Klärschlamm",
        "id": "mresult_wastewater",
        "old_ids": [],
        "behaviors": ["elan"],
        "description": "Messergebnis Abwasser und Klärschlamm",
        "icon": "",
        "subcategory": "Abfälle, Abwasser und Klärschlamm",
        "subcategory_id": "mresults_waste_and_wastewater",
        "subcategory_icon": "",
        "category": "Messergebnisse",
        "category_id": "measurement_results",
    },
    {
        "title": "Messergebnis Bundeswasserstraßen",
        "id": "mresult_waterways",
        "old_ids": [],
        "behaviors": ["elan"],
        "description": "Messergebnis Bundeswasserstraßen, außer Küstengewässer",
        "icon": "",
        "subcategory": "Gewässer, Fisch und Fischereierzeugnisse",
        "subcategory_id": "mresults_water_bodies_and_fish",
        "subcategory_icon": "",
        "category": "Messergebnisse",
        "category_id": "measurement_results",
    },
    {
        "title": "Offizielle Meldung",
        "id": "official_notification",
        "old_ids": ["notification"],
        "behaviors": ["elan"],
        "description": "Meldung über den Eintritt eines überregionalen oder regionalen Notfalls oder eines Ereignisses, das zu einem solchen Notfall führen kann, im Rahmen der gesetzlichen Alarmierungspflicht; sowie Folgemeldungen.",
        "icon": "official_notification",
        "subcategory": "Offizielle Meldungen",
        "subcategory_id": "official_notifications",
        "subcategory_icon": "official_notification",
        "category": "Ereignis",
        "category_id": "incident",
    },
    {
        "title": "Sonstiger Eintrag",
        "id": "other_entry",
        "old_ids": ["mresult_other", "other_document", "kfue-dokument", "probenahmeplan"],
        "behaviors": ["elan"],
        "description": "Wählen Sie diese Eintragsart, wenn keine der anderen zutreffend erscheint.",
        "icon": "",
        "subcategory": "Sonstige Einträge",
        "subcategory_id": "other_entries",
        "subcategory_icon": "",
        "category": "Sonstige Einträge",
        "category_id": "other_entries",
    },
    {
        "title": "Radiologisches Lagebild",
        "id": "radiological_situation_report",
        "old_ids": ["situationreport", "sitrep"],
        "behaviors": ["elan"],
        "description": "Radiologisches Lagebild (RLB) gemäß ANoPl Bund.",
        "icon": "radiological_situation_report",
        "subcategory": "Radiologische Lagebilder / Situationsdarstellungen",
        "subcategory_id": "situation_reports_and_overviews",
        "subcategory_icon": "",
        "category": "Lagebewältigung",
        "category_id": "incident_management",
    },
    {
        "title": "REI-Bericht",
        "id": "rei_report",
        "old_ids": ["reireport"],
        "behaviors": ["rei"],
        "description": "REI-Bericht",
        "icon": "",
        "subcategory": "REI",
        "subcategory_id": "rei",
        "subcategory_icon": "",
        "category": "REI",
        "category_id": "rei",
    },
    {
        "title": "Maßnahmen",
        "id": "response_action",
        "old_ids": ["protectiveactions"],
        "behaviors": ["elan"],
        "description": "Ausweisung der Gebiete, in denen aus radiologischer Sicht Maßnahmen angemessen sind, und empfohlene Maßnahmen.",
        "icon": "",
        "subcategory": "Maßnahmen",
        "subcategory_id": "response_actions",
        "subcategory_icon": "",
        "category": "Lagebewältigung",
        "category_id": "incident_management",
    },
    {
        "title": "Durchgeführte Maßnahme",
        "id": "response_action_taken",
        "old_ids": ["instructions"],
        "behaviors": ["elan"],
        "description": "Rückmeldung über den Umfang und Erfolg der durchgeführten Maßnahmen",
        "icon": "",
        "subcategory": "Durchgeführte Maßnahmen",
        "subcategory_id": "response_actions_taken",
        "subcategory_icon": "",
        "category": "Lagebewältigung",
        "category_id": "incident_management",
    },
    {
        "title": "Situationsdarstellung",
        "id": "situation_overview",
        "old_ids": ["situationsbericht"],
        "behaviors": ["elan"],
        "description": "Darstellung der radiologischen Lage für ein Ereignis, dass nicht als Notfall eingestuft wurde und daher kein Radiologisches Lagebild hat.",
        "icon": "",
        "subcategory": "Radiologische Lagebilder / Situationsdarstellungen",
        "subcategory_id": "situation_reports_and_overviews",
        "subcategory_icon": "",
        "category": "Lagebewältigung",
        "category_id": "incident_management",
    },
    {
        "title": "Stabsmitteilung",
        "id": "staff_note",
        "old_ids": [
            "insituinformation",
            "note_measurement_teams",
            "note",
            "inquiry_measurement_order",
            "measurement_requirements",
        ],
        "behaviors": ["elan"],
        "description": "Mitteilung eines Stabes an alle ELAN-Nutzer, die für die Zusammenarbeit von Bedeutung ist. Bsp: Mitteilung über die Einsatzbereitschaft des Stabes",
        "icon": "",
        "subcategory": "Mitteilungen der Stäbe",
        "subcategory_id": "staff_notes",
        "subcategory_icon": "",
        "category": "Stabsarbeit",
        "category_id": "staff_work",
    },
    {
        "title": "Wetterlage und -prognose",
        "id": "weather_conditions_and_forecast",
        "old_ids": ["trajectory", "weatherinformation"],
        "behaviors": ["elan"],
        "description": "Informationen zur Wetterlage am Ereignisort, Wetterprognosen für das Gefahrengebiet",
        "icon": "",
        "subcategory": "Wetterlage und -prognosen",
        "subcategory_id": "weather_conditions_and_forecasts",
        "subcategory_icon": "",
        "category": "Ereignis",
        "category_id": "incident",
    },
    # These two only exist in bayern!
    {
        "title": "Radiologisches Lagebild Entwurf",
        "id": "radiological_situation_report_draft",
        "old_ids": ["lagebildentwurf"],
        "behaviors": ["elan"],
        "description": "Radiologisches Lagebild (RLB) gemäß ANoPl Bund.",
        "icon": "",
        "subcategory": "Radiologische Lagebilder / Situationsdarstellungen",
        "subcategory_id": "situation_reports_and_overviews",
        "subcategory_icon": "",
        "category": "Lagebewältigung",
        "category_id": "incident_management",
    },
    {
        "title": "Situationsdarstellung Entwurf",
        "id": "situation_overview_draft",
        "old_ids": ["situationsberichtentwurf"],
        "behaviors": ["elan"],
        "description": "Darstellung der radiologischen Lage für ein Ereignis, dass nicht als Notfall eingestuft wurde und daher kein Radiologisches Lagebild hat.",
        "icon": "",
        "subcategory": "Radiologische Lagebilder / Situationsdarstellungen",
        "subcategory_id": "situation_reports_and_overviews",
        "subcategory_icon": "",
        "category": "Lagebewältigung",
        "category_id": "incident_management",
    },
]
