# -*- coding: utf-8 -*-
import os
import unittest
import six.moves.xmlrpc_client

from zope.component import getMultiAdapter, getSiteManager
from zope.interface import Interface
from zope.app.container.interfaces import IContainer
from DateTime import DateTime

from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot

# from Products.Five import zcml
from Products.PloneTestCase import PloneTestCase
from Products.PloneTestCase.layer import onsetup

from wsapi4plone.core.tests.expected_results import PORTAL_SKELETON, PORTAL_VALUES


@onsetup
def setup():
    # We may eventually want to put something here when the wsapi4plone is
    # GenericSetup installable.
    pass


setup()
PloneTestCase.setupPloneSite()

# ??? These two tests are necessary, but should and should not be part
# of these test. We need to find a better place for them to live.

# def test_with_binary_data(self):
#     # Grab some sample data.
#     os.chdir(wsapi4plone.__path__[0])
#     data = open(os.path.join('tests', 'image.png')).read()
#     # Create an Image object at image1.
#     self.loginAsPortalOwner()
#     self.portal.invokeFactory('Image', 'image1', image=data)
#     self.logout()
#     # Login and get the object from the Service point-of-view.
#     self.login('test_user_1_')
#     img = wsapi4plone.IService(self.portal.image1).get_object(['image'])
#     self.logout()
#     # Examin that everything is as expected.
#     for attr in img['image']:
#         if attr == 'data':
#             self.failUnlessEqual(img['image'][attr], data)
#             continue
#         self.failUnlessEqual(img['image'][attr],
#                              IMAGE1['image'][attr])

# def test_set_binary_data(self):
#     # Grab some sample data.
#     os.chdir(wsapi4plone.__path__[0])
#     data = open(os.path.join('tests', 'image.png')).read()
#     # Create an Image object at image1.
#     self.loginAsPortalOwner()
#     self.portal.invokeFactory('Image', 'image1', image=data)
#     self.logout()
#     # Login and get the object from the Service point-of-view.
#     self.login('test_user_1_')
#     serviced_image = wsapi4plone.IService(self.portal.image1)
#     set_properties = serviced_image.set_properties
#     result = set_properties({'image': xmlrpclib.Binary(data)})
#     self.logout()
#     # Check that the data was set.
#     self.failUnlessEqual(self.portal.image1['image'].data, data)


class BaseTestCase(PloneTestCase.PloneTestCase):
    def afterSetUp(self):
        super(BaseTestCase, self).afterSetUp()
        sm = getSiteManager()
        # Register the Plone root service adapter.
        from wsapi4plone.core.interfaces import IServiceContainer
        from wsapi4plone.core.application.services import PloneRootService

        sm.registerAdapter(
            PloneRootService, required=(
                IPloneSiteRoot,), provided=IServiceContainer
        )

    def afterTearDown(self):
        sm = getSiteManager()
        # Unregister the Plone root service adapter.
        from wsapi4plone.core.interfaces import IServiceContainer
        from wsapi4plone.core.application.services import PloneRootService

        sm.unregisterAdapter(
            factory=PloneRootService,
            required=(IPloneSiteRoot,),
            provided=IServiceContainer,
        )
        super(BaseTestCase, self).afterTearDown()


class BasePloneRootServiceTestCase(BaseTestCase):
    def afterSetUp(self):
        super(BasePloneRootServiceTestCase, self).afterSetUp()
        # Authorize the test user to add and edit content at the site root.
        self.portal.manage_setLocalRoles(
            'test_user_1_', ['Reader', 'Editor', 'Contributor']
        )
        # Set up a serviced site object.
        from wsapi4plone.core.interfaces import IServiceContainer

        self.serviced_site = IServiceContainer(self.portal)

    def afterTearDown(self):
        del self.serviced_site
        self.portal.manage_delLocalRoles('test_user_1_')
        super(BasePloneRootServiceTestCase, self).afterTearDown()

    # XXX This method violates dependency relationships.
    def _put_image_in(self, context):
        return context.invokeFactory('Image', 'image4')


class TestPloneServiceContainer(BasePloneRootServiceTestCase):
    def test_create_object(self):
        self.login('test_user_1_')
        id = self.serviced_site.create_object(type_name='Image', id_='image1')
        self.logout()
        # Check to see if image1 exists.
        self.assertTrue(self.portal.get(id, None))

    # def test_clipboard(self):
    #     self.fail("This is not implmented yet, therefore it is suppose "
    #               "to fail.")

    def test_delete_object(self):
        self.login('test_user_1_')
        id = self._put_image_in(self.portal)
        deleted = self.serviced_site.delete_object(id_=id)
        self.logout()
        # Check to see if image1 exists.
        self.failIf(self.portal.get(id, None))


class TestPloneRootService(BasePloneRootServiceTestCase):
    def test_get_skeleton(self):
        from wsapi4plone.core.interfaces import IService

        skel = IService(self.portal).get_skeleton()
        self.failUnlessEqual(skel, PORTAL_SKELETON)

    def test_get_object(self):
        # We need to login to get the values of some of the attributes
        # (e.g. locallyAllowedTypes).
        self.login('test_user_1_')
        from wsapi4plone.core.interfaces import IService

        portal = IService(self.portal).get_object()
        self.logout()
        actual = portal
        expected = PORTAL_VALUES
        actual_keys = list(actual.keys())
        expected_keys = list(expected.keys())

        def diff(a, b):
            c = set(a).difference(set(b))
            return list(c)

        # Check the keys for any differences before moving on.
        self.failUnlessEqual(
            set(actual_keys),
            set(expected_keys),
            "Difference attributes were discovered. The \
                             differening attribute(s) are %s."
            % diff(actual_keys, expected_keys),
        )
        # Check each attribute's value individually since list order and
        # DateTime values will not be the same.
        for attr in actual:
            if isinstance(expected[attr], DateTime):
                # It is good enough that they are the same type?
                # The expected results do not have the most current
                # date and time.
                continue
            elif isinstance(expected[attr], list):
                # We need to take a closer look at lists. There is no
                # guaranty that the results will be in the same order.
                expected_value = expected[attr]
                resulting_value = actual[attr]
                self.failUnlessEqual(
                    set(resulting_value),
                    set(expected_value),
                    "Difference attributes were discovered. \
                                     The differening attribute(s) are %s."
                    % diff(resulting_value, expected_value),
                )
                continue
            # If it gets this far, it must be a base type or it will fail.
            self.failUnlessEqual(expected[attr], actual[attr])

    # def test_get_type(self):
    #     type_ = wsapi4plone.IService(self.portal.Members).get_type()
    #     self.failUnlessEqual(type_, MEMBERS_TYPE)

    # def test_set_properties(self):
    #     obj = wsapi4plone.IService(self.portal.Members)
    #     self.login('test_user_1_')
    #     nata = obj.set_properties(MEMBERS_CHANGES)
    #     self.logout()
    #     # Check the object for the changes.
    #     for attr in MEMBERS_CHANGES:
    #         self.failUnlessEqual(self.portal.Members[attr],
    #                              MEMBERS_CHANGES[attr])


class BasePloneContentsExtensionTestCase(BasePloneRootServiceTestCase):
    def afterSetUp(self):
        super(BasePloneContentsExtensionTestCase, self).afterSetUp()
        sm = getSiteManager()
        # Register the extensions' interface
        from wsapi4plone.core.interfaces import IServiceExtension
        from wsapi4plone.core.application.interfaces import IPloneContents

        sm.registerUtility(
            IPloneContents,
            provided=IServiceExtension,
            name='contents')
        # Register the extension itself
        from wsapi4plone.core.interfaces import IServiceContainer
        from wsapi4plone.core.application.extensions import PloneContents

        sm.registerAdapter(
            PloneContents,
            required=(IServiceContainer, IContainer),
            provided=IPloneContents,
            name='contents',
        )
        # Register the adapter(s) and utilities used by the extension to
        # achieve its purpose.
        from wsapi4plone.core.application.interfaces import IContentsQuery
        from wsapi4plone.core.application.extensions import PloneFolderContents

        sm.registerAdapter(
            PloneFolderContents, required=(
                IContainer,), provided=IContentsQuery
        )
        # IFormatQueryResults is registered for IContentsQuery
        from wsapi4plone.core.utilities.interfaces import IFormatQueryResults
        from wsapi4plone.core.utilities.query import formatter

        sm.registerUtility(formatter(), provided=IFormatQueryResults)
        # IScrubber is registered for IFormatQueryResults
        from wsapi4plone.core.utilities.interfaces import IScrubber
        from wsapi4plone.core.utilities.scrubber import scrub

        sm.registerUtility(scrub(), provided=IScrubber)

    def beforeTearDown(self):
        sm = getSiteManager()
        # Register the extensions' interface
        from wsapi4plone.core.interfaces import IServiceExtension
        from wsapi4plone.core.application.interfaces import IPloneContents

        sm.unregisterUtility(
            IPloneContents, provided=IServiceExtension, name='contents'
        )
        # Register the extension itself
        from wsapi4plone.core.interfaces import IServiceContainer
        from wsapi4plone.core.application.extensions import PloneContents

        sm.unregisterAdapter(
            factory=PloneContents,
            required=(IServiceContainer, IContainer),
            provided=IPloneContents,
            name='contents',
        )
        # Register the adapter(s) and utilities used by the extension to
        # achieve its purpose.
        from wsapi4plone.core.application.interfaces import IContentsQuery
        from wsapi4plone.core.application.extensions import PloneFolderContents

        sm.unregisterAdapter(
            factory=PloneFolderContents, required=(
                IContainer,), provided=IContentsQuery
        )
        # IFormatQueryResults is registered for IContentsQuery
        from wsapi4plone.core.utilities.interfaces import IFormatQueryResults

        # -- from wsapi4plone.core.query import formatter
        sm.unregisterUtility(provided=IFormatQueryResults)
        # IScrubber is registered for IFormatQueryResults
        # -- from wsapi4plone.core.scrubber import scrub
        from wsapi4plone.core.utilities.interfaces import IScrubber

        sm.unregisterUtility(provided=IScrubber)
        super(BasePloneContentsExtensionTestCase, self).beforeTearDown()


class TestPloneContentsExtensions(BasePloneContentsExtensionTestCase):
    def test_get_PloneFolderContents(self):
        self.login('test_user_1_')
        # Create a piece of content.
        id_ = self._put_image_in(self.portal)
        # Grab the extension.
        from wsapi4plone.core.interfaces import IExtension

        ext = getMultiAdapter(
            (self.serviced_site, self.serviced_site.context),
            IExtension,
            name=u'contents',
        )
        contents = ext.get()
        content_uri = u'/plone/image4'
        self.failUnless(
            content_uri in contents, "Failed to get the contents of the folder."
        )
        self.logout()


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestPloneServiceContainer))
    suite.addTest(unittest.makeSuite(TestPloneRootService))
    suite.addTest(unittest.makeSuite(TestPloneContentsExtensions))
    return suite
