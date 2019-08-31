# -*- coding: utf-8 -*-
"""Setup testing infrastructure.

For Plone 5 we need to install plone.app.contenttypes.
"""
from plone import api
from plone.app.robotframework.testing import AUTOLOGIN_LIBRARY_FIXTURE
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import pkg_resources


try:
    pkg_resources.get_distribution('plone.app.contenttypes')
except pkg_resources.DistributionNotFound:
    from plone.app.testing import PLONE_FIXTURE
else:
    from plone.app.contenttypes.testing import (
        PLONE_APP_CONTENTTYPES_FIXTURE as PLONE_FIXTURE,
    )


IS_PLONE_5 = api.env.plone_version().startswith('5')


class Fixture(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import elan.journal
        # required because docpool.base:default sets the permissions of wsapi4plone.core
        import wsapi4plone.core
        import docpool.base
        self.loadZCML(package=docpool.base)
        self.loadZCML(package=wsapi4plone.core)
        self.loadZCML(package=elan.journal)
        self.loadZCML('testing.zcml', package=elan.journal)

    def setUpPloneSite(self, portal):
        # required because the templates in elan.journal use skin-scripts from docpool.base
        self.applyProfile(portal, 'docpool.base:default')
        self.applyProfile(portal, 'elan.journal:default')


FIXTURE = Fixture()

INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,), name='elan.journal:Integration'
)

FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE,), name='elan.journal:Functional')

ROBOT_TESTING = FunctionalTesting(
    bases=(FIXTURE, AUTOLOGIN_LIBRARY_FIXTURE, z2.ZSERVER_FIXTURE),
    name='elan.journal:Robot',
)
