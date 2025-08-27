# -*- coding: utf-8 -*-
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import zope
from plone.testing import z2

import docpool.playwright


class DocpoolPlaywrightLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.app.dexterity

        self.loadZCML(package=plone.app.dexterity)
        import plone.restapi

        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=docpool.playwright)

    def setUpPloneSite(self, portal):
        applyProfile(portal, "docpool.playwright:default")


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
