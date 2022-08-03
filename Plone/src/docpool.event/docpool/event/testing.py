from plone import api
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import (
    SITE_OWNER_NAME,
    SITE_OWNER_PASSWORD,
    TEST_USER_ID,
    FunctionalTesting,
    IntegrationTesting,
    PloneSandboxLayer,
    applyProfile,
    login,
    setRoles,
)
from plone.dexterity.events import EditFinishedEvent
from plone.testing.zope import WSGI_SERVER_FIXTURE
from zope.event import notify


class DocpoolEventLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import docpool.base
        import docpool.config
        import docpool.dashboard
        import docpool.doksys
        import docpool.elan
        import docpool.event
        import docpool.localbehavior
        import docpool.menu
        import docpool.theme
        import docpool.transfers
        import docpool.users
        import eea.facetednavigation
        import elan.esd
        import elan.journal
        import elan.policy
        import elan.sitrep
        import Products.CMFFormController

        self.loadZCML(package=docpool.base)
        self.loadZCML(package=elan.journal)
        self.loadZCML(package=docpool.elan)
        self.loadZCML(package=docpool.config)
        self.loadZCML(package=docpool.theme)
        self.loadZCML(package=docpool.menu)
        self.loadZCML(package=docpool.users)
        self.loadZCML(package=docpool.localbehavior)
        self.loadZCML(package=elan.policy)
        self.loadZCML(package=docpool.doksys)
        self.loadZCML(package=docpool.dashboard)
        self.loadZCML(package=elan.esd)
        self.loadZCML(package=docpool.transfers)
        self.loadZCML(package=elan.sitrep)
        self.loadZCML(package=eea.facetednavigation)
        self.loadZCML(package=Products.CMFFormController)
        self.loadZCML(package=docpool.event)

    def setUpPloneSite(self, portal):
        applyProfile(portal, "docpool.base:default")
        applyProfile(portal, "elan.policy:default")
        applyProfile(portal, "elan.journal:default")
        applyProfile(portal, "docpool.doksys:default")
        applyProfile(portal, "docpool.event:default")
        setRoles(portal, TEST_USER_ID, ["Manager"])
        # Create a docpool
        # Do it here because it takes a long time and creating a docpool
        # in each test or test-setup will lead to very long tests.
        # TODO: Move this to a different layer to allow shorter tests
        docpool = api.content.create(
            container=portal,
            type="DocumentPool",
            id="test_docpool",
            title="Test Dokpool",
            supportedApps=("elan",),
        )
        notify(EditFinishedEvent(docpool))


DOCPOOL_EVENT_FIXTURE = DocpoolEventLayer()


DOCPOOL_EVENT_INTEGRATION_TESTING = IntegrationTesting(
    bases=(DOCPOOL_EVENT_FIXTURE,),
    name="DocpoolEventLayer:IntegrationTesting",
)


DOCPOOL_EVENT_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(DOCPOOL_EVENT_FIXTURE,),
    name="DocpoolEventLayer:FunctionalTesting",
)


DOCPOOL_EVENT_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        DOCPOOL_EVENT_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        WSGI_SERVER_FIXTURE,
    ),
    name="DocpoolEventLayer:AcceptanceTesting",
)
