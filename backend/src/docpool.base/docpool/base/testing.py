"""Testing layers and fixtures for docpool.base tests."""

from docpool.base.localbehavior.localbehavior import LocalBehaviorSupport
from plone import api
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import setRoles
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.app.testing import TEST_USER_ID
from plone.app.textfield import RichTextValue
from plone.dexterity.events import EditFinishedEvent
from plone.testing.zope import WSGI_SERVER_FIXTURE
from zope.event import notify


class DocpoolBaseLayer(PloneSandboxLayer):
    """Testing layer for docpool.base with minimal dependencies."""

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        """Load ZCML for testing."""
        # Load basic packages required for docpool.base
        import collective.impersonate
        import docpool.base
        import docpool.config
        import docpool.elan  # XXX
        import eea.facetednavigation

        self.loadZCML(package=docpool.base)
        self.loadZCML(package=docpool.config)
        self.loadZCML(package=docpool.elan)  # XXX
        self.loadZCML(package=eea.facetednavigation)
        self.loadZCML(package=collective.impersonate)

    def setUpPloneSite(self, portal):
        """Set up Plone site for testing."""
        applyProfile(portal, "docpool.base:default")
        # Skip docpool.config:default as it has theme dependencies we don't need for testing
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


class DocpoolBaseLocalBehaviorLayer(DocpoolBaseLayer):
    """Testing layer specifically for local behavior testing with test data."""

    def setUpPloneSite(self, portal):
        """Set up site with DocumentPool and test applications."""
        super().setUpPloneSite(portal)

        # Create a test DocumentPool with multiple apps
        hessen = api.content.create(
            container=portal,
            type="DocumentPool",
            id="hessen",
            title="Hessen DocumentPool",
            supportedApps=("test_app1", "test_app2"),
        )
        notify(EditFinishedEvent(hessen))

        # Create a minimal DocumentPool for testing restricted scenarios
        minimal = api.content.create(
            container=portal,
            type="DocumentPool",
            id="minimal",
            title="Minimal DocumentPool",
            supportedApps=("test_app1",),
        )
        notify(EditFinishedEvent(minimal))


class DocpoolBaseRealAppsLayer(PloneSandboxLayer):
    """Testing layer with real Dokpool applications (ELAN, REI, Config)."""

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        """Load ZCML for real Dokpool applications."""
        # Load all necessary packages for realistic testing
        import collective.impersonate
        import docpool.base
        import docpool.config
        import docpool.elan
        import docpool.rei
        import eea.facetednavigation
        import elan.journal

        self.loadZCML(package=docpool.base)
        self.loadZCML(package=docpool.config)
        self.loadZCML(package=elan.journal)
        self.loadZCML(package=docpool.elan)
        self.loadZCML(package=docpool.rei)
        self.loadZCML(package=eea.facetednavigation)
        self.loadZCML(package=collective.impersonate)

    def setUpPloneSite(self, portal):
        """Set up site with real applications and DocumentPools."""
        # Apply profiles for all real applications
        applyProfile(portal, "docpool.base:default")
        applyProfile(portal, "elan.journal:default")
        applyProfile(portal, "docpool.elan:default")
        applyProfile(portal, "docpool.rei:default")
        # Skip docpool.config:default due to theme dependencies

        setRoles(portal, TEST_USER_ID, ["Manager"])
        portal.acl_users.userFolderAddUser(SITE_OWNER_NAME, SITE_OWNER_PASSWORD, ["Manager"], [])

        # Create DocumentPool with ELAN and REI applications
        bund = api.content.create(
            container=portal,
            type="DocumentPool",
            id="bund",
            title="Bund DocumentPool",
            supportedApps=("elan", "rei"),
        )
        notify(EditFinishedEvent(bund))

        # Create DocumentPool with only ELAN
        hessen = api.content.create(
            container=portal,
            type="DocumentPool",
            id="hessen",
            title="Hessen DocumentPool",
            supportedApps=("elan",),
        )
        notify(EditFinishedEvent(hessen))


# Base fixtures
DOCPOOL_BASE_FIXTURE = DocpoolBaseLayer()
DOCPOOL_BASE_LOCALBEHAVIOR_FIXTURE = DocpoolBaseLocalBehaviorLayer()
DOCPOOL_BASE_REALAPPS_FIXTURE = DocpoolBaseRealAppsLayer()

# Testing layers
DOCPOOL_BASE_INTEGRATION_TESTING = IntegrationTesting(
    bases=(DOCPOOL_BASE_FIXTURE,),
    name="DocpoolBaseLayer:IntegrationTesting",
)

DOCPOOL_BASE_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(DOCPOOL_BASE_FIXTURE,),
    name="DocpoolBaseLayer:FunctionalTesting",
)

DOCPOOL_BASE_LOCALBEHAVIOR_INTEGRATION_TESTING = IntegrationTesting(
    bases=(DOCPOOL_BASE_LOCALBEHAVIOR_FIXTURE,),
    name="DocpoolBaseLocalBehaviorLayer:IntegrationTesting",
)

DOCPOOL_BASE_LOCALBEHAVIOR_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(DOCPOOL_BASE_LOCALBEHAVIOR_FIXTURE,),
    name="DocpoolBaseLocalBehaviorLayer:FunctionalTesting",
)

DOCPOOL_BASE_REALAPPS_INTEGRATION_TESTING = IntegrationTesting(
    bases=(DOCPOOL_BASE_REALAPPS_FIXTURE,),
    name="DocpoolBaseRealAppsLayer:IntegrationTesting",
)

DOCPOOL_BASE_REALAPPS_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(DOCPOOL_BASE_REALAPPS_FIXTURE,),
    name="DocpoolBaseRealAppsLayer:FunctionalTesting",
)

DOCPOOL_BASE_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        DOCPOOL_BASE_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        WSGI_SERVER_FIXTURE,
    ),
    name="DocpoolBaseLayer:AcceptanceTesting",
)


class LocalBehaviorTestMixin:
    """Mixin providing common test utilities for local behavior testing."""

    def setUp_test_apps(self):
        """Register test applications in the app registry."""
        from docpool.base.appregistry import BEHAVIOR_REGISTRY
        from docpool.base.appregistry import registerApp

        # Register test applications
        registerApp("test_app1", "Test Application 1", implicit=False, extensions=["test_extension1"])
        registerApp("test_app2", "Test Application 2", implicit=False, extensions=["test_extension2"])
        registerApp(
            "test_app_implicit",
            "Implicit Test Application",
            implicit=True,
            extensions=["test_extension_implicit"],
        )

        # Register test behaviors
        BEHAVIOR_REGISTRY["test.extension1"] = ["test_app1"]
        BEHAVIOR_REGISTRY["test.extension2"] = ["test_app2"]
        BEHAVIOR_REGISTRY["test.extension_implicit"] = ["test_app_implicit"]

    def tearDown_test_apps(self):
        """Clean up test applications from registry."""
        from docpool.base.appregistry import BEHAVIOR_REGISTRY
        from docpool.base.appregistry import EXTENSION_REGISTRY

        # Clean up test data
        for app_id in ["test_app1", "test_app2", "test_app_implicit"]:
            if app_id in EXTENSION_REGISTRY:
                del EXTENSION_REGISTRY[app_id]

        for behavior_id in ["test.extension1", "test.extension2", "test.extension_implicit"]:
            if behavior_id in BEHAVIOR_REGISTRY:
                del BEHAVIOR_REGISTRY[behavior_id]

    def create_test_dpdocument(self, container=None, local_behaviors=None, doctype=None):
        """Create a test DPDocument with specified behaviors.

        Args:
            container: Container to create document in (defaults to bund docpool content area)
            local_behaviors: List of local behavior identifiers to assign
            doctype: DocType to assign to the document

        Returns:
            DPDocument: Created document
        """
        if container is None or getattr(container, "portal_type", None) == "DocumentPool":
            # Find a suitable GroupFolder for DPDocuments
            # If container is a DocumentPool, look within it; otherwise use bund
            target_docpool = (
                container
                if container and getattr(container, "portal_type", None) == "DocumentPool"
                else getattr(self.portal, "bund", None)
            )

            if (
                target_docpool
                and hasattr(target_docpool, "content")
                and hasattr(target_docpool.content, "Groups")
            ):
                groups_folder = target_docpool.content.Groups

                # Look for existing GroupFolders like bund_ELANUsers
                for group_id in groups_folder.objectIds():
                    if group_id.endswith("ELANUsers") or group_id.endswith("Users"):
                        container = groups_folder[group_id]
                        break

                if container is None or getattr(container, "portal_type", None) == "DocumentPool":
                    # Create a test GroupFolder
                    container = api.content.create(
                        container=groups_folder, type="GroupFolder", id="test_users", title="Test Users Group"
                    )
            else:
                container = self.portal

        document = api.content.create(
            container=container,
            type="DPDocument",
            id="test_document",
            title="Test Document",
            text=RichTextValue("<p>Text</p>", "text/html", "text/x-html-safe"),
        )

        if doctype:
            document.doctype = doctype

        if local_behaviors:
            adapter = LocalBehaviorSupport(document)
            adapter.local_behaviors = local_behaviors

        return document

    def create_test_doctype(self, container=None, local_behaviors=None, title="Test DocType"):
        """Create a test DocType with specified behaviors.

        Args:
            container: Container to create doctype in (defaults to bund docpool config)
            local_behaviors: List of local behavior identifiers to assign
            title: Title for the doctype

        Returns:
            DocType: Created doctype
        """
        if container is None:
            # Find config/dtypes folder in bund docpool
            bund = getattr(self.portal, "bund", None)
            if bund and hasattr(bund, "config") and hasattr(bund.config, "dtypes"):
                container = bund.config.dtypes
            else:
                container = self.portal

        doctype = api.content.create(container=container, type="DocType", id="test_doctype", title=title)

        if local_behaviors:
            adapter = LocalBehaviorSupport(doctype)
            adapter.local_behaviors = local_behaviors

        return doctype

    def mock_app_state(self, **kwargs):
        """Create a mock app state adapter with specified return values.

        Args:
            **kwargs: Method return values for the mock

        Returns:
            Mock: Configured mock object
        """
        from unittest.mock import Mock

        mock_state = Mock()

        # Default return values
        defaults = {
            "appsPermittedForCurrentUser": ["test_app1", "test_app2"],
            "appsEffectiveForObject": ["test_app1"],
            "effectiveAppsHere": ["test_app1", "test_app2"],
            "appsSupportedHere": ["test_app1", "test_app2"],
            "appsActivatedByCurrentUser": ["test_app1", "test_app2"],
            "appsPermittedForObject": ["test_app1"],
        }

        # Override with provided values
        defaults.update(kwargs)

        # Configure mock methods
        for method_name, return_value in defaults.items():
            getattr(mock_state, method_name).return_value = return_value

        return mock_state


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
