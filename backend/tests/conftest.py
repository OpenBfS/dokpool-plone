from docpool.ui.testing import DOCPOOL_UI_ACCEPTANCE_TESTING
from docpool.ui.testing import DOCPOOL_UI_FUNCTIONAL_TESTING
from docpool.ui.testing import DOCPOOL_UI_INTEGRATION_TESTING
from playwright.sync_api import Page
from plone import api
from plone.app.testing.interfaces import SITE_OWNER_NAME
from plone.app.testing.interfaces import SITE_OWNER_PASSWORD
from plone.app.testing.interfaces import TEST_USER_NAME
from pytest_plone import fixtures_factory
from zope.component.hooks import setSite

import base64
import pytest
import transaction


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


@pytest.fixture()
def portal_factory(acceptance, request):
    def factory(roles: list, username: str = TEST_USER_NAME):
        if not roles:
            roles = ["Member"]
        portal = acceptance["portal"]
        setSite(portal)
        with api.env.adopt_roles(["Manager", "Member"]):
            api.user.grant_roles(
                username=username,
                roles=roles,
            )
        transaction.commit()

        def cleanup():
            with api.env.adopt_roles(["Manager", "Member"]):
                api.user.revoke_roles(
                    username=username,
                    roles=roles,
                )
            transaction.commit()

        request.addfinalizer(cleanup)
        return portal

    return factory


@pytest.fixture()
def playwright_page_factory(new_context):
    def factory(username: str = SITE_OWNER_NAME, password: str = SITE_OWNER_PASSWORD) -> Page:
        context = new_context(
            extra_http_headers={
                "Authorization": generate_basic_authentication_header_value(username, password),
            }
        )
        page = context.new_page()
        return page

    return factory
