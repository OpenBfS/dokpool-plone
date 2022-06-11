import unittest

from docpool.elan.behaviors.elandocument import IELANDocument
from docpool.event.testing import DOCPOOL_EVENT_FUNCTIONAL_TESTING
from docpool.event.utils import getScenariosForCurrentUser, setScenariosForCurrentUser
from plone import api
from plone.app.testing import TEST_USER_ID, login, logout, setRoles
from plone.app.textfield import RichTextValue
from plone.dexterity.events import EditFinishedEvent
from zope.component import getUtility
from zope.event import notify
from zope.lifecycleevent import modified
from zope.schema.interfaces import IVocabularyFactory


class TestDocTypes(unittest.TestCase):

    layer = DOCPOOL_EVENT_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_default_content(self):
        global_config = self.portal["config"]
        global_contentconfig = self.portal["contentconfig"]
        global_esd = self.portal["esd"]
        self.assertEqual(global_config.portal_type, "DPConfig")
        self.assertEqual(global_contentconfig.portal_type, "ELANContentConfig")
        self.assertEqual(global_esd.portal_type, "ELANCurrentSituation")

        global_dtypes = global_config["dtypes"]
        self.assertEqual(
            global_dtypes.keys(),
            [
                "notification",
                "note",
                "eventinformation",
                "nppinformation",
                "weatherinformation",
                "trajectory",
                "rodosprojection",
                "otherprojection",
                "gammadoserate",
                "gammadoserate_timeseries",
                "gammadoserate_mobile",
                "airactivity",
                "mresult_insitu",
                "groundcontamination",
                "mresult_feed",
                "mresult_food",
                "mresult_water",
                "mresult_other",
                "mresult_flight",
                "situationreport",
                "sitrep",
                "estimation",
                "instructions",
                "protectiveactions",
                "mediarelease",
                "information_expert_advisor",
                "measurement_order",
                "operation_map",
                "measurement_requirements",
                "note_measurement_teams",
                "inquiry_measurement_order",
                "info_ecc",
                "info_public",
                "mediareport",
                "lasair_lasat_projection",
                "rodosrun_elan",
                "other_document",
                "doksysdok",
            ],
        )
        self.assertEqual(global_contentconfig.keys(), ["impressum"])
        self.assertEqual(
            global_esd.keys(),
            [
                "front-page",
                "incident",
                "current-situation",
                "management",
                "information-of-the-public",
                "separator",
                "meteorology",
                "dose-projections",
                "measurement-results",
                "overview",
                "recent",
                "dashboard",
                "situationoverview",
            ],
        )

        from docpool.base.appregistry import selectableApps

        self.assertEqual([i[0] for i in selectableApps()], ["doksys", "elan", "rei"])
        docpool = self.portal["test_docpool"]

        self.assertEqual(
            docpool.keys(),
            ["esd", "content", "config", "archive", "contentconfig", "help"],
        )

        esd = docpool["esd"]
        self.assertEqual(
            esd.keys(),
            [
                "front-page",
                "incident",
                "current-situation",
                "management",
                "information-of-the-public",
                "separator",
                "meteorology",
                "dose-projections",
                "measurement-results",
                "overview",
                "recent",
                "dashboard",
                "situationoverview",
            ],
        )

        content = docpool["content"]
        self.assertEqual(content.keys(), ["Transfers", "Members", "Groups"])

        config = docpool["config"]
        self.assertEqual(config.keys(), ["dtypes"])

        dtypes = docpool["config"]["dtypes"]
        self.assertEqual(
            dtypes.keys(),
            [
                "notification",
                "note",
                "eventinformation",
                "nppinformation",
                "weatherinformation",
                "trajectory",
                "rodosprojection",
                "otherprojection",
                "gammadoserate",
                "gammadoserate_timeseries",
                "gammadoserate_mobile",
                "airactivity",
                "mresult_insitu",
                "groundcontamination",
                "mresult_feed",
                "mresult_food",
                "mresult_water",
                "mresult_other",
                "mresult_flight",
                "situationreport",
                "sitrep",
                "estimation",
                "instructions",
                "protectiveactions",
                "mediarelease",
                "information_expert_advisor",
                "measurement_order",
                "operation_map",
                "measurement_requirements",
                "note_measurement_teams",
                "inquiry_measurement_order",
                "info_ecc",
                "info_public",
                "mediareport",
                "lasair_lasat_projection",
                "rodosrun_elan",
                "other_document",
                "doksysdok",
            ],
        )

        archive = docpool["archive"]
        self.assertEqual(archive.keys(), [".wf_policy_config"])

        contentconfig = docpool["contentconfig"]
        self.assertEqual(contentconfig.keys(), ["scen", "ticker", "dbconfig"])

        notify(EditFinishedEvent(docpool))
        # trigger dpAdded method for enabled docpool-products
        # since only elan is active that doe not create new content

        self.assertEqual(
            docpool.keys(),
            ["esd", "content", "config", "archive", "contentconfig", "help"],
        )

        esd = docpool["esd"]
        self.assertEqual(
            esd.keys(),
            [
                "front-page",
                "incident",
                "current-situation",
                "management",
                "information-of-the-public",
                "separator",
                "meteorology",
                "dose-projections",
                "measurement-results",
                "overview",
                "recent",
                "dashboard",
                "situationoverview",
            ],
        )

        content = docpool["content"]
        self.assertEqual(content.keys(), ["Transfers", "Members", "Groups"])

        config = docpool["config"]
        self.assertEqual(config.keys(), ["dtypes"])

        dtypes = docpool["config"]["dtypes"]
        self.assertEqual(
            dtypes.keys(),
            [
                "notification",
                "note",
                "eventinformation",
                "nppinformation",
                "weatherinformation",
                "trajectory",
                "rodosprojection",
                "otherprojection",
                "gammadoserate",
                "gammadoserate_timeseries",
                "gammadoserate_mobile",
                "airactivity",
                "mresult_insitu",
                "groundcontamination",
                "mresult_feed",
                "mresult_food",
                "mresult_water",
                "mresult_other",
                "mresult_flight",
                "situationreport",
                "sitrep",
                "estimation",
                "instructions",
                "protectiveactions",
                "mediarelease",
                "information_expert_advisor",
                "measurement_order",
                "operation_map",
                "measurement_requirements",
                "note_measurement_teams",
                "inquiry_measurement_order",
                "info_ecc",
                "info_public",
                "mediareport",
                "lasair_lasat_projection",
                "rodosrun_elan",
                "other_document",
                "doksysdok",
            ],
        )

        archive = docpool["archive"]
        self.assertEqual(archive.keys(), [".wf_policy_config"])

        contentconfig = docpool["contentconfig"]
        self.assertEqual(contentconfig.keys(), ["scen", "ticker", "dbconfig"])

    def test_doctypes_change_event(self):
        docpool = self.portal["test_docpool"]

        # check for available subtypes of DPDocument
        voc = getUtility(IVocabularyFactory, name="docpool.base.vocabularies.DocType")
        doctypes = voc(self.portal).by_value
        doctypes_ids = [i.id for i in doctypes]
        self.assertEqual(
            set(doctypes_ids),
            {
                "notification",
                "rodosprojection",
                "mresult_flight",
                "info_ecc",
                "mediarelease",
                "lasair_lasat_projection",
                "mresult_feed",
                "measurement_requirements",
                "protectiveactions",
                "note_measurement_teams",
                "mresult_food",
                "instructions",
                "weatherinformation",
                "mresult_insitu",
                "other_document",
                "mresult_water",
                "airactivity",
                "mresult_other",
                "eventinformation",
                "inquiry_measurement_order",
                "nppinformation",
                "trajectory",
                "operation_map",
                "gammadoserate_mobile",
                "mediareport",
                "gammadoserate",
                "rodosrun_elan",
                "gammadoserate_timeseries",
                "otherprojection",
                "groundcontamination",
                "measurement_order",
                "estimation",
                "information_expert_advisor",
                "situationreport",
                "info_public",
                "sitrep",
                "note",
                "doksysdok",
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
        user = api.user.create(email="foo@plone.org", username="foo", password="secret")

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

        # add a dpdocument of type weatherinformation
        weatherinfo = api.content.create(
            container=folder,
            type="DPDocument",
            title="Some Document",
            description="foo",
            docType="weatherinformation",
        )
        self.assertEqual(
            weatherinfo.created_by, "foo <i>Content Administrators (Test Dokpool)</i>"
        )

        eventinfo = api.content.create(
            container=folder,
            type="DPDocument",
            title="Some Document",
            description="foo",
            docType="eventinformation",
        )
        modified(weatherinfo)
        modified(eventinfo)

        # they can be found using the index dp_type
        self.assertEqual(
            len(
                api.content.find(portal_type="DPDocument", dp_type="weatherinformation")
            ),
            1,
        )
        self.assertEqual(
            len(api.content.find(portal_type="DPDocument", dp_type="eventinformation")),
            1,
        )

        # only the one is reindexed
        self.assertEqual(len(api.content.find(Description="foo")), 2)
        self.assertEqual(len(api.content.find(Description="bar")), 0)
        weatherinfo.description = "bar"
        eventinfo.description = "bar"

        # they are not reindexed when changed like this
        self.assertEqual(len(api.content.find(Description="bar")), 0)

        # get the base-doctype for one of the two
        weatherinfo_template = docpool["config"]["dtypes"]["weatherinformation"]

        # trigger reindexing content derived from this
        notify(EditFinishedEvent(weatherinfo_template))

        # only that one was reindexed
        self.assertEqual(len(api.content.find(Description="foo")), 1)
        self.assertEqual(len(api.content.find(Description="bar")), 1)

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
        folder = docpool["content"]["Groups"]["test_docpool_ELANUsers"]
        new = api.content.create(
            container=folder,
            type="DPDocument",
            title="Test DPDocument",
            description="willbefound",
            docType="weatherinformation",
            text=RichTextValue("<p>Text</p>", "text/html", "text/x-html-safe"),
            local_behaviors=["elan", "doksys"],
            scenarios=[event.id],
        )
        api.content.transition(obj=new, transition="publish")
        modified(new)
        # Test setting event/scenario
        setScenariosForCurrentUser(self.portal, scenarios=[event.id])
        scenarios = getScenariosForCurrentUser(self.portal)
        self.assertEqual(scenarios, [event.id])
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
        self.assertEqual(len(res_not), 0)
        # Check the catalog_path
        catalog_path = IELANDocument(new).cat_path()
        self.assertEqual(catalog_path, "esd/meteorology/weather-information")
