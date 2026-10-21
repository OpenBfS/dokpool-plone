from docpool.base.traversal import app_active_after_traversal_subscriber
from docpool.elan.interfaces import IELANActive
from docpool.rei.interfaces import IREIActive
from docpool.ui.browser.viewlets.sidebar import ISidebarManager
from docpool.ui.testing import DOCPOOL_UI_REI_INTEGRATION_TESTING
from lxml import html
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from Products.Five.browser import BrowserView
from zope.component import getMultiAdapter
from zope.interface import noLongerProvides
from ZPublisher.pubevents import PubAfterTraversal

import unittest


class TestReiSidebar(unittest.TestCase):
    layer = DOCPOOL_UI_REI_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        self.docpool = self.portal["bund"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.set_active_app("rei")
        group = api.group.get(groupname="bund_REIUsers")
        group.setGroupProperties({"allowedDocTypes": ["rei_report"]})
        api.group.add_user(group=group, username=TEST_USER_ID)

    def set_active_app(self, app):
        for marker in (IELANActive, IREIActive):
            if marker.providedBy(self.request):
                noLongerProvides(self.request, marker)
        api.user.get_current().setMemberProperties({"apps": [app]})
        app_active_after_traversal_subscriber(PubAfterTraversal(self.request))

    def render_sidebar(self, context=None):
        if context is None:
            context = self.docpool
        view = BrowserView(context, self.request)
        manager = getMultiAdapter(
            (context, self.request, view), ISidebarManager, name="docpool.sidebar.manager"
        )
        manager.update()
        return html.fromstring(manager.render())

    def test_switching_apps_restores_default_navigation(self):
        self.set_active_app("elan")
        sidebar = self.render_sidebar()
        self.assertIn("Chronology", sidebar.text_content())
        self.assertTrue(sidebar.xpath('.//a[contains(@href, "/@@entrytypes")]'))
        self.assertNotIn("REI-Berichte", sidebar.text_content())
        self.set_active_app("rei")
        self.assertIn("REI-Berichte", self.render_sidebar().text_content())

    def test_emergency_folder_uses_tree_navigation(self):
        folder = api.content.create(
            container=self.docpool, type="Folder", id="hintergrundinfos-ns", title="Notfallschutz"
        )
        child = api.content.create(container=folder, type="Folder", id="child", title="Unterordner")
        sidebar = self.render_sidebar(child)
        self.assertIn("Notfallschutz", sidebar.text_content())
        self.assertTrue(
            sidebar.xpath('.//nav//a[@href=$url][contains(@class, "current")]', url=child.absolute_url())
        )
        self.assertNotIn("REI-Berichte", sidebar.text_content())
