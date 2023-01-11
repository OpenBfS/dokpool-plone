from docpool.api.browser.setup import add_user
from docpool.elan.testing import DOCPOOL_EVENT_FUNCTIONAL_TESTING
from plone import api
from plone.app.testing import login
from plone.app.testing import logout
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.events import EditFinishedEvent
from zope.event import notify

import unittest


class TestNavigation(unittest.TestCase):

    layer = DOCPOOL_EVENT_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_personal_folder(self):
        """Personal Folder are not visible for elan
        See https://redmine-koala.bfs.de/issues/2690
        """
        docpool = api.content.create(
            container=self.portal,
            type="DocumentPool",
            id="bund",
            title="Bund",
            prefix="bund",
            supportedApps=("elan", "doksys"),
        )
        notify(EditFinishedEvent(docpool))

        add_user(docpool, "user1", ["group1"], enabled_apps=["elan", "doksys"])
        content = docpool["content"]
        self.assertEqual(content.keys(), ["Transfers", "Members", "Groups"])
        self.assertTrue(content["Members"]["user1"])
        logout()
        login(self.portal, "user1")

        # enable base or doksys (= not elan)
        # result: personal folder is in navigation
        url = docpool.setActiveApp("base")
        dp_app_state = docpool.restrictedTraverse("dp_app_state")
        self.assertFalse(dp_app_state.isCurrentlyActive("elan"))

        self.assertEqual(url, "http://nohost/plone/bund")
        view = docpool.restrictedTraverse("@@view")
        html = view()
        # personal folder is there
        self.assertIn('<a href="http://nohost/plone/bund/content/Members/user1"', html)
        # group folder is there
        self.assertIn(
            '<a href="http://nohost/plone/bund/content/Groups/bund_group1"', html
        )

        # enable elan
        # result: personal folder is not in navigation
        url = docpool.setActiveApp("elan")
        self.assertEqual(url, "http://nohost/plone/bund/esd")
        esd = docpool.esd
        dp_app_state = esd.restrictedTraverse("dp_app_state")
        # purge caching on request
        # key = (('', 'plone', 'bund'), 'ApplicationState', 'isCurrentlyActive', ('elan',), frozenset([]))
        # cache is self.layer["request"].__annotations__["plone.memoize"][key]
        self.layer["request"].__annotations__.pop("plone.memoize")
        self.assertTrue(dp_app_state.isCurrentlyActive("elan"))
        view = esd.restrictedTraverse("@@view")
        html = view()
        # personal folder is not there
        self.assertNotIn(
            '<a href="http://nohost/plone/bund/content/Members/user1"', html
        )
        # group folder is there
        self.assertIn(
            '<a href="http://nohost/plone/bund/content/Groups/bund_group1"', html
        )
