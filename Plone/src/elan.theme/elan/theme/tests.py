from Products.Five import fiveconfigure
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import PloneSite

# from zope.testing import doctestunit
# from zope.component import testing
from Testing import ZopeTestCase as ztc

import elan.theme
import unittest


ptc.setupPloneSite()


class TestCase(ptc.PloneTestCase):
    class layer(PloneSite):
        @classmethod
        def setUp(cls):
            fiveconfigure.debug_mode = True
            ztc.installPackage(elan.theme)
            fiveconfigure.debug_mode = False

        @classmethod
        def tearDown(cls):
            pass


def test_suite():
    return unittest.TestSuite(
        [
            # Unit tests
            # doctestunit.DocFileSuite(
            #    'README.txt', package='elan.theme',
            #    setUp=testing.setUp, tearDown=testing.tearDown),
            # doctestunit.DocTestSuite(
            #    module='elan.theme.mymodule',
            #    setUp=testing.setUp, tearDown=testing.tearDown),
            # Integration tests that use PloneTestCase
            # ztc.ZopeDocFileSuite(
            #    'README.txt', package='elan.theme',
            #    test_class=TestCase),
            # ztc.FunctionalDocFileSuite(
            #    'browser.txt', package='elan.theme',
            #    test_class=TestCase),
        ]
    )


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
