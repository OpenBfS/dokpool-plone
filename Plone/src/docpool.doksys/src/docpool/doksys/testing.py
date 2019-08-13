# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import docpool.doksys


class DocpoolDoksysLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        self.loadZCML(package=docpool.doksys)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'docpool.doksys:default')


DOCPOOL_DOKSYS_FIXTURE = DocpoolDoksysLayer()


DOCPOOL_DOKSYS_INTEGRATION_TESTING = IntegrationTesting(
    bases=(DOCPOOL_DOKSYS_FIXTURE,), name='DocpoolDoksysLayer:IntegrationTesting'
)


DOCPOOL_DOKSYS_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(DOCPOOL_DOKSYS_FIXTURE,), name='DocpoolDoksysLayer:FunctionalTesting'
)


DOCPOOL_DOKSYS_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        DOCPOOL_DOKSYS_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE),
    name='DocpoolDoksysLayer:AcceptanceTesting',
)
