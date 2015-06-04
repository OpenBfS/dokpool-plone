# -*- coding: utf-8 -*-
"""Base level Service (wsapi4plone.service) unittests."""
import unittest

from zope.component import getSiteManager
from zope.interface import implements, Interface
from zope.app.container.interfaces import IContainer


class Dummy(object):
    implements(Interface)


class DummyContainer(object):
    implements(IContainer)


# ########################### #
#   Base Service Test Cases   #
# ########################### #


class ServiceTestCase(unittest.TestCase):

    def setUp(self):
        sm = getSiteManager()
        # Register the base service adapter.
        from wsapi4plone.core.interfaces import IService
        from wsapi4plone.core.service import Service
        sm.registerAdapter(Service,
                           required=(Interface,),
                           provided=IService)
        # Adapter a dummy object to play with in the tests.
        dummy = Dummy()
        self.serviced_object = IService(dummy)

    def tearDown(self):
        del self.serviced_object
        sm = getSiteManager()
        # Unregister the service adapter
        from wsapi4plone.core.service import Service
        assert sm.unregisterAdapter(factory=Service)


class ServiceContainerTestCase(ServiceTestCase):

    def setUp(self):
        super(ServiceContainerTestCase, self).setUp()
        sm = getSiteManager()
        # Register the base service container adapter.
        from wsapi4plone.core.interfaces import IServiceContainer
        from wsapi4plone.core.service import ServiceContainer
        sm.registerAdapter(ServiceContainer,
                           required=(IContainer,),
                           provided=IServiceContainer)
        dummy_container = DummyContainer()
        self.serviced_container = IServiceContainer(dummy_container)

    def tearDown(self):
        del self.serviced_container
        sm = getSiteManager()
        # Unregister the service container adapter.
        from wsapi4plone.core.service import ServiceContainer
        assert sm.unregisterAdapter(factory=ServiceContainer)
        super(ServiceContainerTestCase, self).tearDown()


# ################# #
#   Service Tests   #
# ################# #


class TestService(ServiceTestCase):

    def test_context(self):
        self.failUnlessEqual(Dummy, self.serviced_object.context.__class__)

    def test_get_skleton(self):
        try:
            skel = self.serviced_object.get_skeleton(filtr=[])
        except NotImplementedError:
            return
        self.fail("Something was returned from a method that is not "
                  "implemented. returned: %s" % skel)

    def test_get_object(self):
        try:
            obj = self.serviced_object.get_object(attrs=[])
        except NotImplementedError:
            return
        self.fail("Something was returned from a method that is not "
                  "implemented. returned: %s" % obj)

    def test_get_type(self):
        try:
            type = self.serviced_object.get_type()
        except NotImplementedError:
            return
        self.fail("Something was returned from a method that is not "
                  "implemented. returned: %s" % type)

    # See the extensions tests for tests regarding the {get,set}_extensions
    # methods.

    def test_set_properties(self):
        try:
            props = self.serviced_object.set_properties(params={})
        except NotImplementedError:
            return
        self.fail("Something was returned from a method that is not "
                  "implemented. returned: %s" % props)

    def test_clipboard(self):
        try:
            cb = self.serviced_object.clipboard(action='',
                                                target='somewhere',
                                                destination='elsewhere')
        except NotImplementedError:
            return
        self.fail("Something was returned from a method that is not "
                  "implemented. returned: %s" % cb)


class TestServiceContainer(ServiceContainerTestCase):

    def test_create_object(self):
        create_object = self.serviced_container.create_object
        try:
            obj = create_object(type_name='object_type', id_='object')
        except NotImplementedError:
            return
        self.fail("Something was returned from a method that is not "
                  "implemented. returned: %s" % obj)

    def test_delete_object(self):
        try:
            is_deleted = self.serviced_container.delete_object(id_='object')
        except NotImplementedError:
            return
        self.fail("Something was returned from a method that is not "
                  "implemented. returned: %s" % is_deleted)


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestService))
    suite.addTest(unittest.makeSuite(TestServiceContainer))
    return suite
