from docpool.base.browser.dpdocument import DPDocumentView
from docpool.base.marker import IJournalContainerMarker
from docpool.base.marker import IJournalEntryMarker
from docpool.base.users.usergroups_groupdetails import create_journalfolder
from docpool.base.utils import possibleDocTypes
from docpool.elan.testing import DOCPOOL_EVENT_FUNCTIONAL_TESTING
from docpool.elan.utils import get_scenario_for_current_user
from docpool.elan.utils import getScenariosForCurrentUser
from docpool.elan.utils import setScenariosForCurrentUser
from plone import api
from plone.app.layout.globals.interfaces import IViewView
from plone.app.testing import login
from plone.app.testing import logout
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.textfield import RichTextValue
from plone.dexterity.events import EditFinishedEvent
from plone.dexterity.interfaces import IDexterityFTI
from Products.CMFPlone.controlpanel.events import handleConfigurationChangedEvent
from zope.component import getUtility
from zope.event import notify
from zope.lifecycleevent import modified
from zope.schema.interfaces import IVocabularyFactory

import unittest


class TestDocTypes(unittest.TestCase):
    layer = DOCPOOL_EVENT_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_default_content(self):
        global_config = self.portal["config"]
        global_contentconfig = self.portal["contentconfig"]
        self.assertEqual(global_config.portal_type, "DPConfig")
        self.assertEqual(global_contentconfig.portal_type, "ELANContentConfig")

        global_dtypes = global_config["dtypes"]
        self.assertEqual(
            global_dtypes.keys(),
            [
                "incident",
                "doksys",
                "incident_management",
                "measurement_results",
                "other_entries",
                "rei",
                "staff_work",
                "doksysdok",
            ],
        )
        global_doctypes = api.content.find(context=global_dtypes, portal_type="DocType", sort_on="id")
        self.assertEqual(
            [i.id for i in global_doctypes],
            [
                "additional_event_information",
                "doksys_entry",
                "doksysdok",
                "forecast_spread_dose_contamination",
                "information_for_the_public",
                "journalentry",
                "measurement_recommendation",
                "measurement_strategy",
                "media_report",
                "mresult_air_external_radiation",
                "mresult_air_free_atmosphere",
                "mresult_air_near_ground",
                "mresult_air_traceanalysis",
                "mresult_biological_dosimetry",
                "mresult_crossborder_traffic",
                "mresult_drinking_water",
                "mresult_fish",
                "mresult_incorporation_monitoring",
                "mresult_north_and_baltic_sea",
                "mresult_other_surface_waters",
                "mresult_pharmaceuticals",
                "mresult_placing_on_market",
                "mresult_plant_and_animal_products",
                "mresult_precipitation",
                "mresult_representative_media",
                "mresult_soil",
                "mresult_soil_surface",
                "mresult_transport_of_goods",
                "mresult_waste",
                "mresult_wastewater",
                "mresult_waterways",
                "official_notification",
                "other_entry",
                "radiological_situation_report",
                "radiological_situation_report_draft",
                "rei_report",
                "response_action",
                "response_action_taken",
                "situation_overview",
                "situation_overview_draft",
                "staff_note",
                "weather_conditions_and_forecast",
            ],
        )
        self.assertEqual(global_contentconfig.keys(), ["impressum"])

        from docpool.base.appregistry import selectableApps

        self.assertEqual([i[0] for i in selectableApps()], ["doksys", "elan", "rei"])
        docpool = self.portal["test_docpool"]

        self.assertEqual(
            docpool.keys(),
            ["content", "config", "archive", "contentconfig", "help"],
        )

        content = docpool["content"]
        self.assertEqual(content.keys(), ["Transfers", "Members", "Groups"])

        config = docpool["config"]
        self.assertEqual(config.keys(), ["dtypes"])

        local_dtypes = docpool["config"]["dtypes"]
        self.assertEqual(
            local_dtypes.keys(),
            [
                "incident",
                "doksys",
                "incident_management",
                "measurement_results",
                "other_entries",
                "rei",
                "staff_work",
                "doksysdok",
            ],
        )
        local_doctypes = api.content.find(context=local_dtypes, portal_type="DocType", sort_on="id")
        self.assertEqual(
            [i.id for i in local_doctypes],
            [
                "additional_event_information",
                "doksys_entry",
                "doksysdok",
                "forecast_spread_dose_contamination",
                "information_for_the_public",
                "journalentry",
                "measurement_recommendation",
                "measurement_strategy",
                "media_report",
                "mresult_air_external_radiation",
                "mresult_air_free_atmosphere",
                "mresult_air_near_ground",
                "mresult_air_traceanalysis",
                "mresult_biological_dosimetry",
                "mresult_crossborder_traffic",
                "mresult_drinking_water",
                "mresult_fish",
                "mresult_incorporation_monitoring",
                "mresult_north_and_baltic_sea",
                "mresult_other_surface_waters",
                "mresult_pharmaceuticals",
                "mresult_placing_on_market",
                "mresult_plant_and_animal_products",
                "mresult_precipitation",
                "mresult_representative_media",
                "mresult_soil",
                "mresult_soil_surface",
                "mresult_transport_of_goods",
                "mresult_waste",
                "mresult_wastewater",
                "mresult_waterways",
                "official_notification",
                "other_entry",
                "radiological_situation_report",
                "radiological_situation_report_draft",
                "rei_report",
                "response_action",
                "response_action_taken",
                "situation_overview",
                "situation_overview_draft",
                "staff_note",
                "weather_conditions_and_forecast",
            ],
        )

        archive = docpool["archive"]
        self.assertEqual(archive.keys(), [".wf_policy_config"])

        contentconfig = docpool["contentconfig"]
        self.assertEqual(contentconfig.keys(), ["scen", "ticker"])

        notify(EditFinishedEvent(docpool))
        # trigger dpAdded method for enabled docpool-products
        # since only elan is active that does not create new content

        self.assertEqual(
            docpool.keys(),
            ["content", "config", "archive", "contentconfig", "help"],
        )
        content = docpool["content"]
        self.assertEqual(content.keys(), ["Transfers", "Members", "Groups"])

        config = docpool["config"]
        self.assertEqual(config.keys(), ["dtypes"])

        archive = docpool["archive"]
        self.assertEqual(archive.keys(), [".wf_policy_config"])

        contentconfig = docpool["contentconfig"]
        self.assertEqual(contentconfig.keys(), ["scen", "ticker"])

    def test_doctypes_change_event(self):
        docpool = self.portal["test_docpool"]

        # check for available subtypes of DPDocument
        voc = getUtility(IVocabularyFactory, name="docpool.base.vocabularies.DocType")
        doctypes = voc(raw=True)
        doctypes_ids = [i[0] for i in doctypes]
        self.assertEqual(
            set(doctypes_ids),
            {
                "measurement_strategy",
                "situation_overview_draft",
                "mresult_soil",
                "mresult_waste",
                "mresult_plant_and_animal_products",
                "response_action",
                "mresult_drinking_water",
                "forecast_spread_dose_contamination",
                "mresult_soil_surface",
                "mresult_placing_on_market",
                "mresult_air_external_radiation",
                "rei_report",
                "mresult_air_near_ground",
                "mresult_pharmaceuticals",
                "journalentry",
                "measurement_recommendation",
                "weather_conditions_and_forecast",
                "doksysdok",
                "mresult_transport_of_goods",
                "mresult_biological_dosimetry",
                "media_report",
                "doksys_entry",
                "mresult_fish",
                "staff_note",
                "mresult_representative_media",
                "mresult_crossborder_traffic",
                "mresult_air_traceanalysis",
                "situation_overview",
                "mresult_other_surface_waters",
                "additional_event_information",
                "information_for_the_public",
                "mresult_precipitation",
                "mresult_incorporation_monitoring",
                "official_notification",
                "mresult_air_free_atmosphere",
                "radiological_situation_report",
                "radiological_situation_report_draft",
                "mresult_wastewater",
                "response_action_taken",
                "mresult_waterways",
                "mresult_north_and_baltic_sea",
                "other_entry",
            },
        )

        # get the content-folder for a group to test with
        groups = docpool["content"]["Groups"]
        folder = groups["test_docpool_ContentAdministrators"]

        # DPDocument is allowed
        self.assertEqual(
            [i.id for i in folder.allowedContentTypes()],
            [
                "Collection",
                "InfoFolder",
                "DPDocument",
                "SimpleFolder",
                "ReviewFolder",
                "CollaborationFolder",
                "PrivateFolder",
            ],
        )

        # but not for the current user...
        from docpool.base.utils import getAllowedDocumentTypes

        self.assertFalse(bool(getAllowedDocumentTypes(folder)))

        # add a user to test with
        user = api.user.create(email="foo@plone.org", username="foo", password="verysecret")

        # add the user to the groups
        api.group.add_user(groupname="test_docpool_ContentAdministrators", user=user)
        docpool_contentadmins = api.group.get("test_docpool_ContentAdministrators")
        # enable all doctypes for this group
        docpool_contentadmins.setGroupProperties({"allowedDocTypes": doctypes_ids})

        # login as a the new user
        logout()
        login(self.portal, "foo")

        # now this user can add dpdocument using all doctypes
        allowed = getAllowedDocumentTypes(folder)
        self.assertEqual({i.id for i in allowed}, set(doctypes_ids))
        from docpool.base.utils import getAllowedDocumentTypesForGroup

        self.assertEqual(
            {i.id for i in getAllowedDocumentTypesForGroup(folder)},
            set(doctypes_ids),
        )

        # portal_types are still the same
        self.assertEqual(
            [i.id for i in folder.allowedContentTypes()],
            [
                "Collection",
                "InfoFolder",
                "DPDocument",
                "SimpleFolder",
                "ReviewFolder",
                "CollaborationFolder",
                "PrivateFolder",
            ],
        )

        # add a dpdocument of type weather_conditions_and_forecast
        weatherinfo = api.content.create(
            container=folder,
            type="DPDocument",
            title="Weatherinfo",
            description="foo",
            docType="weather_conditions_and_forecast",
            local_behaviors=["elan"],
        )
        self.assertEqual(
            weatherinfo.created_by,
            ("foo", "foo", "Content Administrators (Test Dokpool)"),
        )

        eventinfo = api.content.create(
            container=folder,
            type="DPDocument",
            title="Eventinfo",
            description="foo",
            docType="additional_event_information",
            local_behaviors=["elan"],
        )
        modified(weatherinfo)
        modified(eventinfo)

        # they can be found using the index dp_type
        self.assertEqual(
            len(api.content.find(portal_type="DPDocument", dp_type="weather_conditions_and_forecast")),
            1,
        )
        self.assertEqual(
            len(api.content.find(portal_type="DPDocument", dp_type="additional_event_information")),
            1,
        )

        # check the category of the weatherinfo
        # TODO: Update test after new categories are setup in tests
        brain = api.content.find(portal_type="DPDocument", dp_type="weather_conditions_and_forecast")[0]
        self.assertEqual(brain.category, "Ereignis")
        self.assertEqual(brain.subcategory, "Wetterlage und -prognosen")

        # get the base-doctype for one of the two
        weatherinfo_template = docpool["config"]["dtypes"]["incident"]["weather_conditions_and_forecasts"][
            "weather_conditions_and_forecast"
        ]

        # Only admins can change/move doktypes
        logout()
        login(self.portal, TEST_USER_NAME)

        # Change the Category of this item by moving it to a different DocTypeSubCategory
        weatherinfo_template = api.content.move(
            weatherinfo_template, docpool["config"]["dtypes"]["staff_work"]["staff_notes"]
        )

        # Invalidate Cache on dokTypeObj()
        handleConfigurationChangedEvent(None)
        # reindex category and subcategory for it and for all items of that type
        notify(EditFinishedEvent(weatherinfo_template))

        brain = api.content.find(portal_type="DPDocument", dp_type="weather_conditions_and_forecast")[0]
        self.assertEqual(brain.category, "Stabsarbeit")
        self.assertEqual(brain.subcategory, "Mitteilungen der Stäbe")

    def test_docpool_searchresults(self):
        docpool = self.portal["test_docpool"]
        # Create a event/Scenario

        container = docpool["contentconfig"]["scen"]
        event = api.content.create(
            container=container,
            type="DPEvent",
            id="test_event",
            title="Test Event",
        )
        event_uid = event.UID()
        folder = docpool["content"]["Groups"]["test_docpool_ELANUsers"]

        # Allow docType for Group and User
        api.group.add_user(groupname=folder.id, username=TEST_USER_NAME)
        group = folder.getGroupOfFolder()
        group.setGroupProperties({"allowedDocTypes": ["weather_conditions_and_forecast"]})

        new = api.content.create(
            container=folder,
            type="DPDocument",
            title="Test DPDocument",
            description="willbefound",
            docType="weather_conditions_and_forecast",
            text=RichTextValue("<p>Text</p>", "text/html", "text/x-html-safe"),
            local_behaviors=["elan", "doksys"],
            scenario=event_uid,
        )
        api.content.transition(obj=new, transition="publish")
        modified(new)
        # Test setting event/scenario
        scenarios = {b.UID: False for b in api.content.find(portal_type="DPEvent")}
        scenarios[event_uid] = True
        setScenariosForCurrentUser(scenarios=scenarios)
        scenarios = getScenariosForCurrentUser()
        self.assertEqual(scenarios, [event_uid])
        # Test search in catalog
        brains = api.content.find(SearchableText="willbefound")
        self.assertEqual(brains[0].getObject().description, "willbefound")
        # Success in the 'content' folder
        query_found = {"SearchableText": "willbefound"}
        # We call the search from the docpool
        # Because of the registration of plone.restapi.controlpanels.SearchControlpanel
        # a lookup by name will not find the default search-form. Duh!
        from Products.CMFPlone.browser.search import Search

        search_view = Search(docpool, self.request)
        res = search_view.results(query=query_found, batch=False)
        self.assertEqual(len(res), 1)
        # failure in 'config'
        query_notfound = {"SearchableText": "Test Event"}
        res_not = search_view.results(query=query_notfound)
        # TODO: Update when global search is implemented in GUI
        # Since docpool.elan.monkey is deactivated we find the item in /config
        self.assertEqual(len(res_not), 1)
        # Check the catalog_path
        # catalog_path = IELANDocument(new).cat_path()
        # self.assertEqual(catalog_path, "esd/meteorology/weather-information")

    def test_commenting(self):
        docpool = self.portal["test_docpool"]
        groups = docpool["content"]["Groups"]
        folder = groups["test_docpool_ContentAdministrators"]

        # Allow docType for Group and User
        api.group.add_user(groupname="test_docpool_ContentAdministrators", username=TEST_USER_NAME)
        group = folder.getGroupOfFolder()
        group.setGroupProperties({"allowedDocTypes": ["weather_conditions_and_forecast"]})

        weatherinfo = api.content.create(
            container=folder,
            type="DPDocument",
            title="Some Document",
            description="foo",
            docType="weather_conditions_and_forecast",
        )

        # check that commenting is enabled globally, per fti and per item
        self.assertTrue(
            api.portal.get_registry_record(
                "plone.app.discussion.interfaces.IDiscussionSettings.globally_enabled"
            )
        )
        self.assertFalse(weatherinfo.restrictedTraverse("@@conversation_view").enabled())
        # inherited from doctype
        doctype = weatherinfo.docTypeObj()
        self.assertFalse(doctype.allow_discussion_on_dpdocument)
        self.assertFalse(weatherinfo.allow_discussion)

        fti = getUtility(IDexterityFTI, name="DPDocument")
        self.assertTrue(fti.allow_discussion)

        view = DPDocumentView(weatherinfo, self.request)

        # The view needs IViewView to render the commenting Viewlet!
        self.assertTrue(IViewView.providedBy(view))

        view_html = view()
        self.assertNotIn("pat-discussion", view_html)

        # Change DocType and commenting is enabled
        doctype.allow_discussion_on_dpdocument = True
        view_html = view()
        self.assertIn("pat-discussion", view_html)

    def test_journalentry_in_available_doctypes(self):
        docpool = self.portal["test_docpool"]
        self.assertIn("journalentry|Tagebucheintrag", possibleDocTypes(docpool))

    def test_allow_journalentry_creates_journal_folder(self):
        docpool = self.portal["test_docpool"]
        groups = docpool["content"]["Groups"]
        folder = groups["test_docpool_ContentAdministrators"]

        # Allow docType for Group and User
        api.group.add_user(groupname="test_docpool_ContentAdministrators", username=TEST_USER_NAME)
        group = folder.getGroupOfFolder()

        # Pretend we modified the group using the form
        group.setGroupProperties({"allowedDocTypes": ["weather_conditions_and_forecast", "journalentry"]})
        create_journalfolder(docpool, group)

        journal_folder = folder["journal"]
        self.assertEqual(journal_folder.portal_type, "SimpleFolder")
        self.assertTrue(IJournalContainerMarker.providedBy(journal_folder))
        self.assertIn("journalentry", journal_folder.allowedDocTypes)
        self.assertNotIn("journalentry", folder.allowedDocTypes)
        self.assertIn("weather_conditions_and_forecast", folder.allowedDocTypes)

        journalentry = api.content.create(
            container=journal_folder,
            type="DPDocument",
            title="Some Document",
            description="foo",
            docType="journalentry",
            local_behaviors=["elan"],
            scenario=get_scenario_for_current_user(),
        )
        self.assertTrue(IJournalEntryMarker.providedBy(journalentry))
