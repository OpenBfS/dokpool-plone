"""Setup testing infrastructure.

For Plone 5 we need to install plone.app.contenttypes.
"""
from plone import api
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import AUTOLOGIN_LIBRARY_FIXTURE
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


class Fixture(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import docpool.base
        import docpool.config
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
        self.loadZCML(package=eea.facetednavigation)
        self.loadZCML(package=Products.CMFFormController)
        self.loadZCML(package=docpool.transfers)
        self.loadZCML(package=elan.sitrep)
        self.loadZCML(package=elan.esd)
        self.loadZCML(package=docpool.doksys)
        self.loadZCML(package=docpool.event)
        self.loadZCML("testing.zcml", package=elan.journal)

    def setUpPloneSite(self, portal):
        # required because the templates in elan.journal use skin-scripts from docpool.base
        applyProfile(portal, "docpool.base:default")
        applyProfile(portal, "elan.journal:default")
        applyProfile(portal, "elan.esd:default")
        applyProfile(portal, "docpool.doksys:default")
        applyProfile(portal, "docpool.event:default")
        setRoles(portal, TEST_USER_ID, ["Manager"])
        docpool = api.content.create(
            container=portal,
            type="DocumentPool",
            id="test_docpool",
            title="Test Dokpool",
            supportedApps=("elan",),
        )
        notify(EditFinishedEvent(docpool))


FIXTURE = Fixture()

INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,), name="elan.journal:Integration"
)

FUNCTIONAL_TESTING = FunctionalTesting(bases=(FIXTURE,), name="elan.journal:Functional")

ROBOT_TESTING = FunctionalTesting(
    bases=(FIXTURE, AUTOLOGIN_LIBRARY_FIXTURE, WSGI_SERVER_FIXTURE),
    name="elan.journal:Robot",
)
