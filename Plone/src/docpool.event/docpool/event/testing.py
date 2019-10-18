# -*- coding: utf-8 -*-
from plone import api
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.events import EditFinishedEvent
from plone.testing import z2
from zope.event import notify


class DocpoolEventLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import elan.journal
        import docpool.event
        import docpool.config
        import docpool.base
        import docpool.elan
        import docpool.theme
        import docpool.menu
        import wsapi4plone.core
        import elan.policy
        import docpool.doksys
        self.loadZCML(package=docpool.base)
        self.loadZCML(package=docpool.elan)
        self.loadZCML(package=docpool.config)
        self.loadZCML(package=docpool.theme)
        self.loadZCML(package=docpool.menu)
        self.loadZCML(package=wsapi4plone.core)
        self.loadZCML(package=elan.policy)
        self.loadZCML(package=docpool.doksys)
        self.loadZCML(package=elan.journal)
        self.loadZCML(package=docpool.event)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'docpool.base:default')
        applyProfile(portal, 'elan.policy:default')
        applyProfile(portal, 'docpool.doksys:default')
        applyProfile(portal, 'elan.journal:default')
        applyProfile(portal, 'docpool.event:default')
        setRoles(portal, TEST_USER_ID, ['Manager'])
        # Create a docpool
        # Do it here because it takes a long time and creating a docpool
        # in each test or test-setup will lead to very long tests.
        # TODO: Move this to a different layer to allow shorter tests
        docpool = api.content.create(
            container=portal,
            type='DocumentPool',
            id='test_docpool',
            title=u'Test Dokpool',
            supportedApps=('elan',),
        )
        notify(EditFinishedEvent(docpool))


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
