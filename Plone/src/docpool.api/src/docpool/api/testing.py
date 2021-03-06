# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.app.testing import applyProfile
from plone.testing import z2
import docpool.api


class DocpoolApiLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import wsapi4elan.core
        import plone.restapi
        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=wsapi4elan.core)
        self.loadZCML(package=docpool.api)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'docpool.api:default')

class DocpoolApiCleanLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import wsapi4elan.core
        import plone.restapi
        import docpool.rei
        import elan.policy
        import docpool.transfers
        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=wsapi4elan.core)
        self.loadZCML(package=docpool.transfers)
        self.loadZCML(package=docpool.api)
        self.loadZCML(package=docpool.menu)
        self.loadZCML(package=docpool.doksys)
        self.loadZCML(package=docpool.config)
        self.loadZCML(package=docpool.event)
        self.loadZCML(package=elan.policy)
        self.loadZCML(package=elan.journal)
        self.loadZCML(package=docpool.rei)

    def setUpPloneSite(self, portal):
        portal.acl_users.userFolderAddUser(SITE_OWNER_NAME, SITE_OWNER_PASSWORD, ['Manager'], [])

DOCPOOL_API_FIXTURE = DocpoolApiLayer()
DOCPOOL_API_CLEAN_FIXTURE = DocpoolApiCleanLayer()


DOCPOOL_API_INTEGRATION_TESTING = IntegrationTesting(
    bases=(DOCPOOL_API_FIXTURE,), name='DocpoolApiLayer:IntegrationTesting'
)

DOCPOOL_API_FUNCTIONAL_FULL_TESTING = FunctionalTesting(
    bases=(DOCPOOL_API_CLEAN_FIXTURE,),
    name='DocpoolApiLayer:FunctionalFullTesting',
)

DOCPOOL_API_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(DOCPOOL_API_FIXTURE,), name='DocpoolApiLayer:FunctionalTesting'
)


DOCPOOL_API_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(DOCPOOL_API_FIXTURE, REMOTE_LIBRARY_BUNDLE_FIXTURE, z2.ZSERVER_FIXTURE),
    name='DocpoolApiLayer:AcceptanceTesting',
)
