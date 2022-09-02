from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing.zope import WSGI_SERVER_FIXTURE


class DocpoolDoksysLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import docpool.base
        import docpool.config
        import docpool.elan
        import docpool.transfers
        import docpool.users
        import eea.facetednavigation
        import Products.CMFFormController

        self.loadZCML(package=docpool.base)
        self.loadZCML(package=docpool.config)
        # required since we need to be able to add DBTranfers
        self.loadZCML(package=docpool.transfers)
        self.loadZCML(package=docpool.users)
        self.loadZCML(package=eea.facetednavigation)
        self.loadZCML(package=Products.CMFFormController)
        self.loadZCML(package=docpool.doksys)

    def setUpPloneSite(self, portal):
        applyProfile(portal, "docpool.doksys:default")
        applyProfile(portal, "docpool.transfers:default")


DOCPOOL_DOKSYS_FIXTURE = DocpoolDoksysLayer()


DOCPOOL_DOKSYS_INTEGRATION_TESTING = IntegrationTesting(
    bases=(DOCPOOL_DOKSYS_FIXTURE,), name="DocpoolDoksysLayer:IntegrationTesting"
)


DOCPOOL_DOKSYS_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(DOCPOOL_DOKSYS_FIXTURE,), name="DocpoolDoksysLayer:FunctionalTesting"
)


DOCPOOL_DOKSYS_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(DOCPOOL_DOKSYS_FIXTURE, REMOTE_LIBRARY_BUNDLE_FIXTURE, WSGI_SERVER_FIXTURE),
    name="DocpoolDoksysLayer:AcceptanceTesting",
)
