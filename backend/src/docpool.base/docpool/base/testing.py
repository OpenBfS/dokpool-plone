from plone import api
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import setRoles
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.app.testing import TEST_USER_ID
from plone.dexterity.events import EditFinishedEvent
from zope.event import notify


class DocpoolBaseLayer(PloneSandboxLayer):
    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import collective.impersonate
        import docpool.base
        import docpool.elan  # XXX
        import eea.facetednavigation

        self.loadZCML(package=docpool.base)
        self.loadZCML(package=docpool.elan)  # XXX
        self.loadZCML(package=eea.facetednavigation)
        self.loadZCML(package=collective.impersonate)

    def setUpPloneSite(self, portal):
        applyProfile(portal, "docpool.base:default")
        applyProfile(portal, "docpool.elan:default")  # XXX only while logging inconsistent scenario index
        setRoles(portal, TEST_USER_ID, ["Manager"])
        docpool = api.content.create(
            container=portal,
            type="DocumentPool",
            id="test_docpool",
            title="Test Dokpool",
        )
        notify(EditFinishedEvent(docpool))
        self["test_docpool"] = docpool
        portal.acl_users.userFolderAddUser(SITE_OWNER_NAME, SITE_OWNER_PASSWORD, ["Manager"], [])


DOCPOOL_BASE_FIXTURE = DocpoolBaseLayer()


DOCPOOL_BASE_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(DOCPOOL_BASE_FIXTURE,),
    name="DocpoolBaseLayer:FunctionalTesting",
)


class DocpoolTransferLayer(PloneSandboxLayer):
    defaultBases = (DOCPOOL_BASE_FIXTURE,)

    def setUpPloneSite(self, portal):
        source = portal["test_docpool"]
        for i in ("a", "b"):
            docpool = api.content.create(
                container=portal,
                type="DocumentPool",
                id=f"target_docpool_{i}",
                title=f"Target Dokpool {i}",
                supportedApps=(),
            )
            notify(EditFinishedEvent(docpool))
            transfer_folder = api.content.create(
                container=docpool["content"]["Transfers"],
                type="DPTransferFolder",
                id="from_test",
                title="from Test",
                sendingESD=source.UID(),
            )
            notify(EditFinishedEvent(transfer_folder))
            self[f"target_docpool_{i}"] = docpool
            self[f"target_transfer_folder_{i}"] = transfer_folder


DOCPOOL_TRANSFER_FIXTURE = DocpoolTransferLayer()


DOCPOOL_TRANSFER_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(DOCPOOL_TRANSFER_FIXTURE,),
    name="DocpoolTransferLayer:FunctionalTesting",
)
