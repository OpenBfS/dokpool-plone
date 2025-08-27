# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import zope


class DocpoolPlaywrightLayer(PloneSandboxLayer):
    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import collective.impersonate
        import docpool.base
        import docpool.elan
        import docpool.playwright
        import docpool.ui
        import eea.facetednavigation
        import plone.restapi

        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=docpool.base)
        self.loadZCML(package=docpool.elan)
        # self.loadZCML(package=docpool.ui)
        self.loadZCML(package=eea.facetednavigation)
        self.loadZCML(package=collective.impersonate)
        self.loadZCML(package=docpool.playwright)

    def setUpPloneSite(self, portal):
        applyProfile(portal, "docpool.base:default")
        applyProfile(portal, "docpool.elan:default")
        applyProfile(portal, "elan.journal:default")
        # applyProfile(portal, "docpool.ui:default")
        applyProfile(portal, "docpool.playwright:default")
        # setRoles(portal, TEST_USER_ID, ["Manager"])
        # # Create a docpool
        # # Do it here because it takes a long time and creating a docpool
        # # in each test or test-setup will lead to very long tests.
        # dp = api.content.create(
        #     container=portal,
        #     type="DocumentPool",
        #     id="bund",
        #     title="Bund",
        #     prefix="bund",
        #     supportedApps=("elan",),
        # )
        # notify(EditFinishedEvent(dp))
        # portal.acl_users.userFolderAddUser(SITE_OWNER_NAME, SITE_OWNER_PASSWORD, ["Manager"], [])
        #


DOCPOOL_PLAYWRIGHT_FIXTURE = DocpoolPlaywrightLayer()


DOCPOOL_PLAYWRIGHT_INTEGRATION_TESTING = IntegrationTesting(
    bases=(DOCPOOL_PLAYWRIGHT_FIXTURE,),
    name="DocpoolPlaywrightLayer:IntegrationTesting",
)


DOCPOOL_PLAYWRIGHT_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(DOCPOOL_PLAYWRIGHT_FIXTURE,),
    name="DocpoolPlaywrightLayer:FunctionalTesting",
)


DOCPOOL_PLAYWRIGHT_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        DOCPOOL_PLAYWRIGHT_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        zope.WSGI_SERVER_FIXTURE,
    ),
    name="DocpoolPlaywrightLayer:AcceptanceTesting",
)
