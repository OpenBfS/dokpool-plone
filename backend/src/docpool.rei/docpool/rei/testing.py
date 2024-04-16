from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.testing.zope import WSGI_SERVER_FIXTURE


class DocpoolReiLayer(PloneSandboxLayer):
    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import collective.impersonate
        import docpool.base
        import eea.facetednavigation

        self.loadZCML(package=docpool.base)
        self.loadZCML(package=eea.facetednavigation)
        self.loadZCML(package=docpool.rei)
        self.loadZCML(package=collective.impersonate)

    def setUpPloneSite(self, portal):
        applyProfile(portal, "docpool.rei:default")


class DocpoolReiCleanLayer(PloneSandboxLayer):
    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import docpool.base
        import docpool.rei

        self.loadZCML(package=docpool.base)
        self.loadZCML(package=docpool.rei)

    def setUpPloneSite(self, portal):
        portal.acl_users.userFolderAddUser(
            SITE_OWNER_NAME, SITE_OWNER_PASSWORD, ["Manager"], []
        )


DOCPOOL_REI_FIXTURE = DocpoolReiLayer()
DOCPOOL_REI_CLEAN_FIXTURE = DocpoolReiCleanLayer()


DOCPOOL_REI_INTEGRATION_TESTING = IntegrationTesting(
    bases=(DOCPOOL_REI_FIXTURE,), name="DocpoolReiLayer:IntegrationTesting"
)

DOCPOOL_REI_FUNCTIONAL_FULL_TESTING = FunctionalTesting(
    bases=(DOCPOOL_REI_CLEAN_FIXTURE,),
    name="DocpoolReiLayer:FunctionalFullTesting",
)

DOCPOOL_REI_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(DOCPOOL_REI_FIXTURE,), name="DocpoolReiLayer:FunctionalTesting"
)


DOCPOOL_REI_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(DOCPOOL_REI_FIXTURE, REMOTE_LIBRARY_BUNDLE_FIXTURE, WSGI_SERVER_FIXTURE),
    name="DocpoolReiLayer:AcceptanceTesting",
)
