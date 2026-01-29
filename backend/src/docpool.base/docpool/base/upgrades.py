from docpool.base.content.simplefolder import ISimpleFolder
from docpool.base.setuphandlers import create_session_stuff
from docpool.base.utils import getDocumentPoolSite
from plone import api
from plone.app.upgrade.utils import loadMigrationProfile
from plone.base.utils import get_installer

import logging


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
        "subcategory": "Ergänzende Ereignisinformationen",
        "subcategory_id": "additional_event_information",
        "category": "Ereignis",
        "category_id": "incident",
    },
    {
        "title": "DOKSYS-Eintrag",
        "id": "doksys_entry",
        "old_ids": ["doksysdok"],
        "behaviors": ["doksys"],
        "description": "Eintragsart für die DOKSYS-Applikation",
        "subcategory": "DOKSYS",
        "subcategory_id": "doksys",
        "category": "DOKSYS",
        "category_id": "doksys",
    },
    {
        "title": "Prognose über Ausbreitung, Dosis und Kontamination",
        "id": "forecast_spread_dose_contamination",
        "old_ids": ["lasair_lasat_projection", "otherprojection", "rodosprojection"],
        "behaviors": ["elan", "rodos"],
        "description": "(RODOS-) Ausbreitungsrechnung über die prognostizierte Ankunftszeit radioaktiver Luftmassen, die zu erwartende Kontamination der Umwelt oder die zu erwartende Dosis der Bevölkerung unter Berücksichtigung der aktuellen und prognostizierten Wetterbedingungen.",
        "subcategory": "Prognosen über Ausbreitung, Dosis und Kontamination",
        "subcategory_id": "forecasts_spread_dose_contamination",
        "category": "Lagebewältigung",
        "category_id": "incident_management",
    },
    {
        "title": "Information an Bevölkerung",
        "id": "information_for_the_public",
        "old_ids": ["info_public", "mediarelease"],
        "behaviors": ["elan"],
        "description": "Abgestimmte Kommunikationsempfehlung zur Information der Bevölkerung, inklusive eigene Pressemitteilungen",
        "subcategory": "Informationen an Bevölkerung",
        "subcategory_id": "information_for_the_public",
        "category": "Lagebewältigung",
        "category_id": "incident_management",
    },
    {
        "title": "Messempfehlung",
        "id": "measurement_recommendation",
        "old_ids": ["inquiry_measurement_order", "measurement_order", "measurement_requirements"],
        "behaviors": ["elan"],
        "description": "Messempfehlung an Einsatzkräfte des Bundes und der Länder, sowie KHG",
        "subcategory": "Messempfehlungen",
        "subcategory_id": "measurement_recommendations",
        "category": "Lagebewältigung",
        "category_id": "incident_management",
    },
    {
        "title": "Messstrategie",
        "id": "measurement_strategy",
        "old_ids": ["messstrategie"],
        "behaviors": ["elan"],
        "description": "Messstrategie zu einem Radiologischen Lagebild gemäß ANoPl Bund.",
        "subcategory": "Messstrategien",
        "subcategory_id": "measurement_strategies",
        "category": "Lagebewältigung",
        "category_id": "incident_management",
    },
    {
        "title": "Medienbericht",
        "id": "media_report",
        "old_ids": ["mediareport"],
        "behaviors": ["elan"],
        "description": "Mediale Berichterstattung zum Ereignis",
        "subcategory": "Medienberichte",
        "subcategory_id": "media_reports",
        "category": "Ereignis",
        "category_id": "incident",
    },
    {
        "title": "Messergebnis Luft/externe Strahlung (Gamma-ODL)",
        "id": "mresult_air_external_radiation",
        "old_ids": ["gammadoserate_mobile", "gammadoserate_timeseries", "gammadoserate"],
        "behaviors": ["elan"],
        "description": "Messergebnis Luft/externe Strahlung",
        "subcategory": "Luft (inklusive Gamma-ODL)",
        "subcategory_id": "mresults_air",
        "category": "Messergebnisse",
        "category_id": "measurement_results",
    },
    {
        "title": "Messergebnis Luft/freie Atmosphäre",
        "id": "mresult_air_free_atmosphere",
        "old_ids": [],
        "behaviors": ["elan"],
        "description": "Messergebnis Luft/freie AtmosphäreAtmosphäre",
        "subcategory": "Luft (inklusive Gamma-ODL)",
        "subcategory_id": "mresults_air",
        "category": "Messergebnisse",
        "category_id": "measurement_results",
    },
    {
        "title": "Messergebnis Luft/bodennah",
        "id": "mresult_air_near_ground",
        "old_ids": ["airactivity", "mresult_emission", "mresult_flight", "mresult_insitu"],
        "behaviors": ["elan"],
        "description": "Messergebnis Luft/bodennah",
        "subcategory": "Luft (inklusive Gamma-ODL)",
        "subcategory_id": "mresults_air",
        "category": "Messergebnisse",
        "category_id": "measurement_results",
    },
    {
        "title": "Messergebnis Luft/bodennah (Spurenanalyse)",
        "id": "mresult_air_near_ground_traces",
        "old_ids": ["mresult_traceanalysis"],
        "behaviors": ["elan"],
        "description": "Messergebnis Luft/bodennah (Spurenanalyse einschließlich Edelgase)",
        "subcategory": "Luft (inklusive Gamma-ODL)",
        "subcategory_id": "mresults_air",
        "category": "Messergebnisse",
        "category_id": "measurement_results",
    },
    {
        "title": "Messergebnis Biologische Dosimetrie",
        "id": "mresult_biological_dosimetry",
        "old_ids": [],
        "behaviors": ["elan"],
        "description": "Messergebnis Biologische Dosimetrie",
        "subcategory": "Inkorporationsüberwachung und biologische Dosimetrie",
        "subcategory_id": "mresults_incorporation_and_biological_dosimetry",
        "category": "Messergebnisse",
        "category_id": "measurement_results",
    },
    {
        "title": "Messergebnis Grenzüberschreitender Verkehr",
        "id": "mresult_crossborder_traffic",
        "old_ids": [],
        "behaviors": ["elan"],
        "description": "Messergebnis Grenzüberschreitender Verkehr von Personen, Fahrzeugen, Gütern und Gepäck",
        "subcategory": "Beförderung von Gütern und grenzüberschreitender Verkehr",
        "subcategory_id": "mresults_transport_of_goods_and_crossborder_traffic",
        "category": "Messergebnisse",
        "category_id": "measurement_results",
    },
    {
        "title": "Messergebnis Trinkwasser",
        "id": "mresult_drinking_water",
        "old_ids": ["messergebnis_trinkwasser"],
        "behaviors": ["elan"],
        "description": "Messergebnis Trinkwasser",
        "subcategory": "Trinkwasser und Inverkehrbringen von Lebensmittel, Futtermitteln etc.",
        "subcategory_id": "mresults_drinking_water_and_placing_on_market",
        "category": "Messergebnisse",
        "category_id": "measurement_results",
    },
    {
        "title": "Messergebnis Fisch und Fischereierzeugnisse",
        "id": "mresult_fish",
        "old_ids": [],
        "behaviors": ["elan"],
        "description": "Messergebnis Fisch und Fischereierzeugnisse, Krustentiere, Schalentiere, Meereswasserpflanzen",
        "subcategory": "Gewässer, Fisch und Fischereierzeugnisse",
        "subcategory_id": "mresults_water_bodies_and_fish",
        "category": "Messergebnisse",
        "category_id": "measurement_results",
    },
    {
        "title": "Messergebnis Inkorporationsüberwachung",
        "id": "mresult_incorporation_monitoring",
        "old_ids": ["information_notfallstation"],
        "behaviors": ["elan"],
        "description": "Messergebnis Inkorporationsüberwachung",
        "subcategory": "Inkorporationsüberwachung und biologische Dosimetrie",
        "subcategory_id": "mresults_incorporation_and_biological_dosimetry",
        "category": "Messergebnisse",
        "category_id": "measurement_results",
    },
    {
        "title": "Messergebnis Nord- und Ostsee",
        "id": "mresult_north_and_baltic_sea",
        "old_ids": [],
        "behaviors": ["elan"],
        "description": "Messergebnis Nord- und Ostsee einschließlich Küstengewässer",
        "subcategory": "Gewässer, Fisch und Fischereierzeugnisse",
        "subcategory_id": "mresults_water_bodies_and_fish",
        "category": "Messergebnisse",
        "category_id": "measurement_results",
    },
    {
        "title": "Messergebnis Sonstige Oberflächengewässer",
        "id": "mresult_other_surface_waters",
        "old_ids": ["mresult_water"],
        "behaviors": ["elan"],
        "description": "Messergebnis Sonstige Oberflächengewässer",
        "subcategory": "Gewässer, Fisch und Fischereierzeugnisse",
        "subcategory_id": "mresults_water_bodies_and_fish",
        "category": "Messergebnisse",
        "category_id": "measurement_results",
    },
    {
        "title": "Messergebnis Arzneimittel",
        "id": "mresult_pharmaceuticals",
        "old_ids": [],
        "behaviors": ["elan"],
        "description": "Messergebnis Arzneimittel und deren Ausgangsstoffe",
        "subcategory": "Arzneimittel",
        "subcategory_id": "mresults_pharmaceuticals",
        "category": "Messergebnisse",
        "category_id": "measurement_results",
    },
    {
        "title": "Messergebnis Inverkehrbringen",
        "id": "mresult_placing_on_market",
        "old_ids": [],
        "behaviors": ["elan"],
        "description": "Messergebnis Inverkehrbringen von Lebensmitteln, Bedarfsgegenständen, Mitteln zum Tätowieren, kosmetischen Mitteln, Verfüttern oder Inverkehrbringen von Futtermitteln",
        "subcategory": "Trinkwasser und Inverkehrbringen von Lebensmittel, Futtermitteln etc.",
        "subcategory_id": "mresults_drinking_water_and_placing_on_market",
        "category": "Messergebnisse",
        "category_id": "measurement_results",
    },
    {
        "title": "Messergebnis Pflanzliche und tierische Erzeugnisse",
        "id": "mresult_plant_and_animal_products",
        "old_ids": ["mresult_feed", "mresult_food"],
        "behaviors": ["elan"],
        "description": "Messergebnis Produktion pflanzlicher und tierischer Erzeugnisse",
        "subcategory": "Repräsentative Medien, pflanzliche und tierische Erzeugnisse",
        "subcategory_id": "mresults_representive_media_and_plant_animal_procucts",
        "category": "Messergebnisse",
        "category_id": "measurement_results",
    },
    {
        "title": "Messergebnis Niederschlag",
        "id": "mresult_precipitation",
        "old_ids": ["mresult_precipitation"],
        "behaviors": ["elan"],
        "description": "Messergebnis Niederschlag",
        "subcategory": "Bodenoberfläche und Niederschlag",
        "subcategory_id": "mresults_soil_surface_and_precipitation",
        "category": "Messergebnisse",
        "category_id": "measurement_results",
    },
    {
        "title": "Messergebnis Repräsentative Medien",
        "id": "mresult_representative_media",
        "old_ids": [],
        "behaviors": ["elan"],
        "description": "Messergebnis Repräsentative Medien",
        "subcategory": "Repräsentative Medien, pflanzliche und tierische Erzeugnisse",
        "subcategory_id": "mresults_representive_media_and_plant_animal_procucts",
        "category": "Messergebnisse",
        "category_id": "measurement_results",
    },
    {
        "title": "Messergebnis Bodenoberfläche",
        "id": "mresult_soil_surface",
        "old_ids": ["groundcontamination"],
        "behaviors": ["elan"],
        "description": "Messergebnis Bodenoberfläche",
        "subcategory": "Bodenoberfläche und Niederschlag",
        "subcategory_id": "mresults_soil_surface_and_precipitation",
        "category": "Messergebnisse",
        "category_id": "measurement_results",
    },
    {
        "title": "Messergebnis Beförderung von Gütern",
        "id": "mresult_transport_of_goods",
        "old_ids": [],
        "behaviors": ["elan"],
        "description": "Messergebnis Beförderung von Gütern",
        "subcategory": "Beförderung von Gütern und grenzüberschreitender Verkehr",
        "subcategory_id": "mresults_transport_of_goods_and_crossborder_traffic",
        "category": "Messergebnisse",
        "category_id": "measurement_results",
    },
    {
        "title": "Messergebnis Abfälle",
        "id": "mresult_waste",
        "old_ids": [],
        "behaviors": ["elan"],
        "description": "Messergebnis Abfälle",
        "subcategory": "Abfälle, Abwasser und Klärschlamm",
        "subcategory_id": "mresults_waste_and_wastewater",
        "category": "Messergebnisse",
        "category_id": "measurement_results",
    },
    {
        "title": "Messergebnis Abwasser und Klärschlamm",
        "id": "mresult_wastewater",
        "old_ids": [],
        "behaviors": ["elan"],
        "description": "Messergebnis Abwasser und Klärschlamm",
        "subcategory": "Abfälle, Abwasser und Klärschlamm",
        "subcategory_id": "mresults_waste_and_wastewater",
        "category": "Messergebnisse",
        "category_id": "measurement_results",
    },
    {
        "title": "Messergebnis Bundeswasserstraßen",
        "id": "mresult_waterways",
        "old_ids": [],
        "behaviors": ["elan"],
        "description": "Messergebnis Bundeswasserstraßen, außer Küstengewässer",
        "subcategory": "Gewässer, Fisch und Fischereierzeugnisse",
        "subcategory_id": "mresults_water_bodies_and_fish",
        "category": "Messergebnisse",
        "category_id": "measurement_results",
    },
    {
        "title": "Offizielle Meldung",
        "id": "official_notification",
        "old_ids": ["notification"],
        "behaviors": ["elan"],
        "description": "Meldung über den Eintritt eines überregionalen oder regionalen Notfalls oder eines Ereignisses, das zu einem solchen Notfall führen kann, im Rahmen der gesetzlichen Alarmierungspflicht; sowie Folgemeldungen.",
        "subcategory": "Offizielle Meldungen",
        "subcategory_id": "official_notifications",
        "category": "Ereignis",
        "category_id": "incident",
    },
    {
        "title": "Sonstiger Eintrag",
        "id": "other_entry",
        "old_ids": ["mresult_other", "other_document"],
        "behaviors": ["elan"],
        "description": "Wählen Sie diese Eintragsart, wenn keine der anderen zutreffend erscheint.",
        "subcategory": "Sonstige Einträge",
        "subcategory_id": "other_entries",
        "category": "Sonstige Einträge",
        "category_id": "other_entries",
    },
    {
        "title": "Radiologisches Lagebild",
        "id": "radiological_situation_report",
        "old_ids": ["situationreport", "sitrep"],
        "behaviors": ["elan"],
        "description": "Radiologisches Lagebild (RLB) gemäß ANoPl Bund.",
        "subcategory": "Radiologische Lagebilder / Situationsdarstellungen",
        "subcategory_id": "situation_reports_and_overviews",
        "category": "Lagebewältigung",
        "category_id": "incident_management",
    },
    {
        "title": "Radiologisches Lagebild Entwurf",
        "id": "radiological_situation_report_draft",
        "old_ids": ["lagebildentwurf"],
        "behaviors": ["elan"],
        "description": "Radiologisches Lagebild (RLB) gemäß ANoPl Bund.",
        "subcategory": "Radiologische Lagebilder / Situationsdarstellungen",
        "subcategory_id": "situation_reports_and_overviews",
        "category": "Lagebewältigung",
        "category_id": "incident_management",
    },
    {
        "title": "REI-Bericht",
        "id": "rei_report",
        "old_ids": ["reireport"],
        "behaviors": ["rei"],
        "description": "REI-Bericht",
        "subcategory": "REI",
        "subcategory_id": "rei",
        "category": "REI",
        "category_id": "rei",
    },
    {
        "title": "Maßnahmengebiet",
        "id": "response_action_area",
        "old_ids": ["protectiveactions"],
        "behaviors": ["elan"],
        "description": "Ausweisung der Gebiete, in denen aus radiologischer Sicht Maßnahmen angemessen sind, und empfohlene Maßnahmen.",
        "subcategory": "Maßnahmengebiete",
        "subcategory_id": "response_action_areas",
        "category": "Lagebewältigung",
        "category_id": "incident_management",
    },
    {
        "title": "Durchgeführte Maßnahme",
        "id": "response_action_taken",
        "old_ids": ["instructions"],
        "behaviors": ["elan"],
        "description": "Rückmeldung über den Umfang und Erfolg der durchgeführten Maßnahmen",
        "subcategory": "Durchgeführte Maßnahmen",
        "subcategory_id": "response_actions_taken",
        "category": "Lagebewältigung",
        "category_id": "incident_management",
    },
    {
        "title": "Situationsdarstellung",
        "id": "situation_overview",
        "old_ids": ["situationsbericht"],
        "behaviors": ["elan"],
        "description": "Darstellung der radiologischen Lage für ein Ereignis, dass nicht als Notfall eingestuft wurde und daher kein Radiologisches Lagebild hat.",
        "subcategory": "Radiologische Lagebilder / Situationsdarstellungen",
        "subcategory_id": "situation_reports_and_overviews",
        "category": "Lagebewältigung",
        "category_id": "incident_management",
    },
    {
        "title": "Situationsdarstellung Entwurf",
        "id": "situation_overview_draft",
        "old_ids": ["situationsberichtentwurf"],
        "behaviors": ["elan"],
        "description": "Darstellung der radiologischen Lage für ein Ereignis, dass nicht als Notfall eingestuft wurde und daher kein Radiologisches Lagebild hat.",
        "subcategory": "Radiologische Lagebilder / Situationsdarstellungen",
        "subcategory_id": "situation_reports_and_overviews",
        "category": "Lagebewältigung",
        "category_id": "incident_management",
    },
    {
        "title": "Stabsmitteilung",
        "id": "staff_note",
        "old_ids": ["insituinformation", "note_measurement_teams", "note"],
        "behaviors": ["elan"],
        "description": "Mitteilung eines Stabes an alle ELAN-Nutzer, die für die Zusammenarbeit von Bedeutung ist. Bsp: Mitteilung über die Einsatzbereitschaft des Stabes",
        "subcategory": "Mitteilungen der Stäbe",
        "subcategory_id": "staff_notes",
        "category": "Stabsarbeit",
        "category_id": "staff_work",
    },
    {
        "title": "Wetterlage und -prognose",
        "id": "weather_conditions_and_forecast",
        "old_ids": ["trajectory", "weatherinformation"],
        "behaviors": ["elan"],
        "description": "Informationen zur Wetterlage am Ereignisort, Wetterprognosen für das Gefahrengebiet",
        "subcategory": "Wetterlage und -prognosen",
        "subcategory_id": "weather_conditions_and_forecasts",
        "category": "Ereignis",
        "category_id": "incident",
    },
]

log = logging.getLogger(__name__)


def to_1010(context=None):
    portal = api.portal.get()
    installer = get_installer(portal)
    if installer.is_product_installed("docpool.rei"):
        # reload workflow to change BMUV to BMUKN
        portal_setup = api.portal.get_tool("portal_setup")
        loadMigrationProfile(
            portal_setup,
            "profile-docpool.rei:default",
            steps=["workflow"],
        )


def to_1011(context=None):
    # Change history action to @@fullfull_review_history and View
    portal_setup = api.portal.get_tool("portal_setup")
    loadMigrationProfile(
        portal_setup,
        "profile-docpool.base:to_1011",
    )


def to_1012(context=None):
    # Fix regex for images and pdfs
    broken = ".*"
    fixed_pdf = ".+\.pdf$"
    fixed_image = ".+\.(png|jpg)$"
    for brain in api.content.find(portal_type="DocType"):
        obj = brain.getObject()
        if obj.pdfPattern and obj.pdfPattern == broken:
            obj.pdfPattern = fixed_pdf
            obj._p_changed = 1
            log.info("Fixed pdfPattern for %s", brain.getURL())
        if obj.imgPattern and obj.imgPattern == broken:
            obj.imgPattern = fixed_image
            obj._p_changed = 1
            log.info("Fixed imgPattern for %s", brain.getURL())

    # remove obsolete copies of transfer logs
    for brain in api.content.find(portal_type="DPDocument"):
        if hasattr((obj := brain.getObject()).aq_base, "transferLog"):
            del obj.transferLog
            obj._p_changed = 1


def to_1012_update_dp_doc_workflow(context=None):
    # Update dp_doc_workflow
    log.info("Reload dp_doc_workflow and remove Owner permissions in published state")
    portal_setup = api.portal.get_tool("portal_setup")
    loadMigrationProfile(portal_setup, "profile-docpool.base:default", steps=["workflow"])
    portal_workflow = api.portal.get_tool("portal_workflow")
    log.info("Upgrading permissions...")
    portal_workflow.updateRoleMappings()


def to_3000(context=None):
    """Upgrade existing DB to new GUI"""
    portal = api.portal.get()
    installer = get_installer(portal)
    if not installer.is_product_installed("docpool.ui"):
        installer.install_product("docpool.ui")

    catalog = api.portal.get_tool("portal_catalog")
    # the category index changes to FieldIndex
    catalog.delIndex("category")
    portal_setup = api.portal.get_tool("portal_setup")
    loadMigrationProfile(
        portal_setup,
        "profile-docpool.base:to_3000",
    )
    create_session_stuff(portal)

    # TODO: Enable ELAN for Bremen, Hamburg, Mecklenburg-Vorpommern, Sachsen-Anhalt

    # Drop unused relations
    api.relation.delete(relationship="contentCategory")
    api.relation.delete(relationship="docTypes")

    create_doctype_structure()
    delete_esd_structure()


def create_doctype_structure():

    rename_mapping = {}
    for item in DOCTYPES:
        for old in item["old_ids"]:
            assert old not in rename_mapping
            rename_mapping[old] = item["id"]

    for brain in api.content.find(portal_type="DocTypes", sort_on="path"):
        doctypes_container = brain.getObject()

        # Move old DocTypes out of the way before moving/updating them
        if "old" not in doctypes_container:
            old = api.content.create(
                container=doctypes_container,
                type="DocTypeCategory",
                id="old",
                title="Old DocTypes",
            )
            for obj in doctypes_container.contentValues({"portal_type": "DocType"}):
                api.content.move(source=obj, target=old)
        else:
            old = doctypes_container["old"]

        # TODO: Handle special cases (e.g. Ukraine)
        # * handle special doctypes
        # * update DPDocuments of these types

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
                )
        # Create subcategories
        for info in DOCTYPES:
            if subcategory_id := info.get("subcategory_id"):
                category_container = doctypes_container[info["category_id"]]
                if subcategory_id in category_container:
                    continue
                api.content.create(
                    container=category_container,
                    type="DocTypeCategory",
                    id=subcategory_id,
                    title=info["subcategory"],
                )

        # Create DocTypes
        for info in DOCTYPES:
            container = doctypes_container
            if category_id := info.get("category_id"):
                container = doctypes_container[info["category_id"]]
                if subcategory_id := info.get("subcategory_id"):
                    container = container[subcategory_id]
            if info["id"] in container:
                continue

            # Move and update existing doctypes
            for old_id in info["old_ids"]:
                if old.get(old_id) and container.get(info["id"]):
                    # A different old item with the same new id was already updated.
                    pass
                elif old_obj := old.get(old_id, None):
                    old_obj.title = info["title"]
                    old_obj.description = info["description"]
                    old_obj.local_behaviors = info["behaviors"]
                    api.content.move(source=old_obj, target=container, id=info["id"])

            if info["id"] not in container:
                # This is new!
                api.content.create(
                    container=container,
                    type="DocType",
                    id=info["id"],
                    title=info["title"],
                    description=info["description"],
                    local_behaviors=info["behaviors"],
                )

        # Remove old doctypes that were not moved and updated, ignore links and relations
        old = doctypes_container["old"]
        for old_doctype in old.contentValues():
            if old_doctype.id in rename_mapping:
                log.info("Deleting old DokType %s from %s", old_doctype.id, old.absolute_url())
                api.content.delete(old_doctype, check_linkintegrity=False)
        if not old.contentValues():
            api.content.delete(old, check_linkintegrity=False)

        # Log infos on remains that ceen to be cleaned up
        dp = getDocumentPoolSite(doctypes_container)
        log.info("Remains in %s", dp.absolute_url())
        content_area = dp.get("content", None)
        archive_area = dp.get("archive", None)
        for old_id in old.keys():
            if old_id in rename_mapping:
                continue
            old_obj = old[old_id]
            count_content = 0
            count_archive = 0
            if content_area:
                count_content = len(
                    api.content.find(context=content_area, portal_type="DPDocument", dp_type=old_id)
                )
            if archive_area:
                count_archive = len(
                    api.content.find(context=archive_area, portal_type="DPDocument", dp_type=old_id)
                )
            if count_content or count_archive:
                log.info(
                    f"{old_obj.id} ({old_obj.title}): {count_content + count_archive} ({count_archive} archived)"
                )
            else:
                log.info(f"{old_obj.id} ({old_obj.title})")

    # Change all existing DPDocuments
    for brain in api.content.find(portal_type="DPDocument", sort_on="path"):
        obj = brain.getObject()
        if obj.docType in rename_mapping:
            obj.docType = rename_mapping[obj.docType]
            obj.reindexObject(idxs=["category", "subcategory", "dp_type"])

    # Change all existing groups
    for group in api.group.get_groups():
        if allowed_types := group.getProperty("allowedDocTypes", []):
            new_allowed_types = list(set([rename_mapping[i] for i in allowed_types if i in rename_mapping]))
            group.setGroupProperties({"allowedDocTypes": new_allowed_types})

    # Change allowed types for some folder types
    for brain in api.content.find(object_provides=ISimpleFolder.__identifier__):
        obj = brain.getObject()
        if allowed_types := obj.allowedDocTypes:
            new_allowed_types = [rename_mapping[i] for i in allowed_types if i in rename_mapping]
            obj.allowedDocTypes = list(set(new_allowed_types))
    for brain in api.content.find(portal_type="CollaborationFolder"):
        obj = brain.getObject()
        if allowed_types := obj.allowedPartnerDocTypes:
            new_allowed_types = [rename_mapping[i] for i in allowed_types if i in rename_mapping]
            obj.allowedPartnerDocTypes = list(set(new_allowed_types))


def delete_esd_structure(context=None):
    # Delete old esd structure and types
    to_delete = [
        "Dashboard",
        "DashboardsConfig",
        "DashboardCollection",
        "ELANCurrentSituation",
        "ELANDocCollection",
        "ELANSection",
    ]
    for brain in api.content.find(portal_type="ELANCurrentSituation", sort_on="path"):
        obj = brain.getObject()
        api.content.delete(obj, check_linkintegrity=False)

    for portal_type in to_delete:
        for brain in api.content.find(portal_type=portal_type, sort_on="path"):
            obj = brain.getObject()
            api.content.delete(obj, check_linkintegrity=False)
    portal_types = api.portal.get_tool("portal_types")
    for portal_type in to_delete:
        if portal_type in portal_types:
            portal_types.manage_delObjects(portal_type)
