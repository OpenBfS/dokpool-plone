from _pytest.pytester import Pytester
from _pytest.python import Metafunc
import base64
from pathlib import Path
from typing import Generator

import pytest
import transaction
from playwright.sync_api import Page
from plone import api
from plone.app.testing.interfaces import (
    SITE_OWNER_NAME,
    SITE_OWNER_PASSWORD,
    TEST_USER_NAME,
)
from plone.testing.zope import WSGI_SERVER_FIXTURE
from pytest_plone import fixtures_factory
from pythongettext.msgfmt import Msgfmt, PoSyntaxError
from zope.component.hooks import setSite

from docpool.playwright.testing import (
    DOCPOOL_PLAYWRIGHT_INTEGRATION_TESTING,
    DOCPOOL_PLAYWRIGHT_FUNCTIONAL_TESTING,
    DOCPOOL_PLAYWRIGHT_ACCEPTANCE_TESTING
)

pytest_plugins = ["pytest_plone"]

globals().update(
    fixtures_factory(
        (
            (DOCPOOL_PLAYWRIGHT_ACCEPTANCE_TESTING, "acceptance"),
            (DOCPOOL_PLAYWRIGHT_FUNCTIONAL_TESTING, "functional"),
            (DOCPOOL_PLAYWRIGHT_INTEGRATION_TESTING, "integration"),
        )
    )
)


def generate_basic_authentication_header_value(username: str, password: str) -> str:
    token = base64.b64encode("{}:{}".format(username, password).encode("utf-8")).decode(
        "ascii"
    )
    return "Basic {}".format(token)


@pytest.fixture()
def portal_factory(acceptance, request):
    def factory(roles: list, username: str = TEST_USER_NAME):
        if not roles:
            roles = ['Member']
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
    def factory(
        username: str = SITE_OWNER_NAME, password: str = SITE_OWNER_PASSWORD
    ) -> Page:
        context = new_context(
            extra_http_headers={
                "Authorization": generate_basic_authentication_header_value(
                    username, password
                ),
            }
        )
        page = context.new_page()
        return page

    return factory
