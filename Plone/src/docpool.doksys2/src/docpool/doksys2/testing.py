# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import docpool.doksys2


class DocpoolDoksys2Layer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        self.loadZCML(package=docpool.doksys2)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'docpool.doksys2:default')


DOCPOOL_DOKSYS2_FIXTURE = DocpoolDoksys2Layer()


DOCPOOL_DOKSYS2_INTEGRATION_TESTING = IntegrationTesting(
    bases=(DOCPOOL_DOKSYS2_FIXTURE,),
    name='DocpoolDoksys2Layer:IntegrationTesting',
)


DOCPOOL_DOKSYS2_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(DOCPOOL_DOKSYS2_FIXTURE,),
    name='DocpoolDoksys2Layer:FunctionalTesting',
)


DOCPOOL_DOKSYS2_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        DOCPOOL_DOKSYS2_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='DocpoolDoksys2Layer:AcceptanceTesting',
)
