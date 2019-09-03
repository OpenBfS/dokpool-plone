# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import docpool.event


class DocpoolEventLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import docpool.config
        import docpool.base
        import docpool.elan
        import docpool.theme
        import docpool.menu
        import wsapi4plone.core
        import elan.policy
        self.loadZCML(package=docpool.base)
        self.loadZCML(package=docpool.elan)
        self.loadZCML(package=docpool.config)
        self.loadZCML(package=docpool.theme)
        self.loadZCML(package=docpool.menu)
        self.loadZCML(package=wsapi4plone.core)
        self.loadZCML(package=elan.policy)
        self.loadZCML(package=docpool.event)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'docpool.base:default')
        applyProfile(portal, 'elan.policy:default')
        applyProfile(portal, 'docpool.event:default')


DOCPOOL_EVENT_FIXTURE = DocpoolEventLayer()


DOCPOOL_EVENT_INTEGRATION_TESTING = IntegrationTesting(
    bases=(DOCPOOL_EVENT_FIXTURE,),
    name='DocpoolEventLayer:IntegrationTesting',
)


DOCPOOL_EVENT_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(DOCPOOL_EVENT_FIXTURE,),
    name='DocpoolEventLayer:FunctionalTesting',
)


DOCPOOL_EVENT_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        DOCPOOL_EVENT_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='DocpoolEventLayer:AcceptanceTesting',
)
