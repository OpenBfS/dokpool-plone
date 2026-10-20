from docpool.api.browser.setup import add_user
from docpool.ui.testing import DOCPOOL_UI_ACCEPTANCE_TESTING
from docpool.ui.testing import DOCPOOL_UI_FUNCTIONAL_TESTING
from docpool.ui.testing import DOCPOOL_UI_INTEGRATION_TESTING
from playwright.sync_api import Page
from plone import api
from pytest_plone import fixtures_factory
from zope.component.hooks import setSite

import base64
import pytest
import transaction


BUND_CONTENT_ADMIN_NAME = "bund_contentadmin"
BUND_CONTENT_ADMIN_PASSWORD = "admin"


pytest_plugins = ["pytest_plone"]

globals().update(
    fixtures_factory((
        (DOCPOOL_UI_ACCEPTANCE_TESTING, "acceptance"),
        (DOCPOOL_UI_FUNCTIONAL_TESTING, "functional"),
        (DOCPOOL_UI_INTEGRATION_TESTING, "integration"),
    ))
)


def generate_basic_authentication_header_value(username: str, password: str) -> str:
    token = base64.b64encode("{}:{}".format(username, password).encode("utf-8")).decode("ascii")
    return "Basic {}".format(token)


# Create ELAN test user with Bund content-admin membership.
@pytest.fixture()
def bund_content_admin(acceptance):
    portal = acceptance["portal"]
    setSite(portal)
    with api.env.adopt_roles(["Manager", "Member"]):
        portal.acl_users.userFolderAddUser(
            BUND_CONTENT_ADMIN_NAME, BUND_CONTENT_ADMIN_PASSWORD, ["Member"], []
        )
        user = api.user.get(username=BUND_CONTENT_ADMIN_NAME)
        user.setMemberProperties({"fullname": "Content Admin (Bund)"})
        add_user(portal["bund"], BUND_CONTENT_ADMIN_NAME, enabled_apps=["elan"])
        api.group.add_user(groupname="bund_ContentAdministrators", user=user)
    transaction.commit()
    return user


def create_authenticated_page(new_context, username: str, password: str) -> Page:
    context = new_context(
        extra_http_headers={
            "Authorization": generate_basic_authentication_header_value(username, password),
        }
    )
    return context.new_page()


# Factory for browser pages authenticated as Bund content-admin user
@pytest.fixture()
def content_admin_page_factory(new_context, bund_content_admin):
    def factory() -> Page:
        return create_authenticated_page(
            new_context,
            username=bund_content_admin.getId(),
            password=BUND_CONTENT_ADMIN_PASSWORD,
        )

    return factory


# Factory for browser pages authenticated as site owner
@pytest.fixture()
def site_owner_page_factory(
    new_context,
    site_owner_name,
    site_owner_password,
):
    def factory() -> Page:
        return create_authenticated_page(
            new_context,
            username=site_owner_name,
            password=site_owner_password,
        )

    return factory
