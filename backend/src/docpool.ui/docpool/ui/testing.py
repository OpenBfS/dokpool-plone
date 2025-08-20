from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.testing.zope import WSGI_SERVER_FIXTURE


class DocpoolUiLayer(PloneSandboxLayer):
    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import collective.impersonate
        import docpool.base
        import docpool.elan
        import docpool.ui
        import eea.facetednavigation
        import plone.restapi

        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=docpool.base)
        self.loadZCML(package=docpool.elan)
        self.loadZCML(package=docpool.ui)
        self.loadZCML(package=eea.facetednavigation)
        self.loadZCML(package=collective.impersonate)

    def setUpPloneSite(self, portal):
        applyProfile(portal, "docpool.base:default")
        applyProfile(portal, "docpool.elan:default")
        applyProfile(portal, "elan.journal:default")
        applyProfile(portal, "docpool.ui:default")


class DocpoolUiCleanLayer(PloneSandboxLayer):
    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import docpool.base
        import docpool.ui
        import plone.restapi

        self.loadZCML(package=docpool.base)
        self.loadZCML(package=docpool.ui)
        self.loadZCML(package=plone.restapi)

    def setUpPloneSite(self, portal):
        portal.acl_users.userFolderAddUser(SITE_OWNER_NAME, SITE_OWNER_PASSWORD, ["Manager"], [])


DOCPOOL_UI_FIXTURE = DocpoolUiLayer()
DOCPOOL_UI_CLEAN_FIXTURE = DocpoolUiCleanLayer()


DOCPOOL_UI_INTEGRATION_TESTING = IntegrationTesting(
    bases=(DOCPOOL_UI_FIXTURE,), name="DocpoolUiLayer:IntegrationTesting"
)

DOCPOOL_UI_FUNCTIONAL_CLEAN_TESTING = FunctionalTesting(
    bases=(DOCPOOL_UI_CLEAN_FIXTURE,),
    name="DocpoolUiLayer:FunctionalCleanTesting",
)

DOCPOOL_UI_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(DOCPOOL_UI_FIXTURE,), name="DocpoolUiLayer:FunctionalTesting"
)

DOCPOOL_UI_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(DOCPOOL_UI_FIXTURE, REMOTE_LIBRARY_BUNDLE_FIXTURE, WSGI_SERVER_FIXTURE),
    name="DocpoolUiLayer:AcceptanceTesting",
)
