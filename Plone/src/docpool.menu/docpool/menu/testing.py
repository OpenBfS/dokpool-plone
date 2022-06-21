import docpool.menu
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import (
    FunctionalTesting,
    IntegrationTesting,
    PloneSandboxLayer,
    applyProfile,
)
from plone.testing.zope import WSGI_SERVER_FIXTURE


class DocpoolMenuLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        self.loadZCML(package=docpool.menu)

    def setUpPloneSite(self, portal):
        applyProfile(portal, "docpool.menu:default")


DOCPOOL_MENU_FIXTURE = DocpoolMenuLayer()


DOCPOOL_MENU_INTEGRATION_TESTING = IntegrationTesting(
    bases=(DOCPOOL_MENU_FIXTURE,), name="DocpoolMenuLayer:IntegrationTesting"
)


DOCPOOL_MENU_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(DOCPOOL_MENU_FIXTURE,), name="DocpoolMenuLayer:FunctionalTesting"
)


DOCPOOL_MENU_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(DOCPOOL_MENU_FIXTURE, REMOTE_LIBRARY_BUNDLE_FIXTURE, WSGI_SERVER_FIXTURE),
    name="DocpoolMenuLayer:AcceptanceTesting",
)
