# -*- coding: utf-8 -*-
import unittest

from zope.interface import implements, Interface
from zope.interface.verify import verifyObject
from zope.component import getMultiAdapter, getSiteManager
from zope.app.container.interfaces import IContainer

from wsapi4plone.core.tests.test_00_service import ServiceTestCase
from wsapi4plone.core.interfaces import (
    ICallbackExtension, IReadExtension, IWriteExtension)
from wsapi4plone.core.extension import BaseExtension


# ################### #
#   Example classes   #
# ################### #


class Dummy(object):
    implements(Interface)


class DummyContainer(object):
    implements(IContainer)


class ICrashTestExtension(IReadExtension, ICallbackExtension):
    """Crash test extension interface with read-only support."""


class ICrashTestWriteExtension(IWriteExtension):
    """Crash Test extension interface with write support."""


class BaseCrashTestExtension(BaseExtension):
    """Base class so that we can reuse the get method."""

    def get(self):
        """Returns whether or not the dummy object has crashed or not."""
        return getattr(self.context, 'has_crashed', False)


class ReadOnlyCrashTestExtension(BaseCrashTestExtension):
    implements(ICrashTestExtension)

    def get_callback(self):
        return self.get()


class WriteCrashTestExtension(BaseCrashTestExtension):
    implements(ICrashTestWriteExtension)

    def set(self, has_crashed):
        """Crash or repair the dummy object."""
        if not isinstance(has_crashed, bool):
            raise TypeError("%s.set_extension argument has_crashed is not "
                            "a boolean value. Recieved: %s" % \
                            (self.__class__.__name__, has_crashed))
        self.context.has_crashed = has_crashed

    def get_skeleton(self):
        return dict(has_crashed=dict(type='bool', required=True))


# ################### #
#   Extension Tests   #
# ################### #


class BaseExtensionTestCase(ServiceTestCase):

    ext_key = ''

    def setUp(self):
        super(BaseExtensionTestCase, self).setUp()
        if not self.ext_key and not instance(self.ext_key, str):
            raise ValueError("You must assign a value to 'ext_key' in your "
                             "test case. Otherwise the test case will not "
                             "work correctly.")

    def test_extension_implements(self):
        from wsapi4plone.core.interfaces import IExtension
        obj = self.serviced_object.context
        ext = getMultiAdapter((self.serviced_object, obj,),
                              IExtension, name=self.ext_key)
        self.assert_(verifyObject(IExtension, ext))

    def get_extension(self):
        context = self.serviced_object.context
        # Grab the extension
        from wsapi4plone.core.interfaces import IExtension
        ext = getMultiAdapter((self.serviced_object, context,),
                              IExtension,
                              name=self.ext_key)
        return ext


class TestReadExtension(BaseExtensionTestCase):

    ext_key = 'crashtest'

    def setUp(self):
        super(TestReadExtension, self).setUp()
        sm = getSiteManager()
        # Register the example extension
        from wsapi4plone.core.interfaces import (IService, IServiceExtension)
        sm.registerUtility(ICrashTestExtension,
                           provided=IServiceExtension,
                           name=self.ext_key)
        sm.registerAdapter(ReadOnlyCrashTestExtension,
                           required=(IService, Interface,),
                           provided=ICrashTestExtension,
                           name=self.ext_key)

    def tearDown(self):
        sm = getSiteManager()
        # Unregister the example extension
        from wsapi4plone.core.interfaces import (IService, IServiceExtension)
        assert sm.unregisterUtility(component=ICrashTestExtension,
                                    provided=IServiceExtension,
                                    name=self.ext_key)
        assert sm.unregisterAdapter(factory=ReadOnlyCrashTestExtension,
                                    required=(IService, Interface,),
                                    provided=ICrashTestExtension,
                                    name=self.ext_key)
        super(TestReadExtension, self).tearDown()

    def test_verfiy_write_provider(self):
        from wsapi4plone.core.interfaces import IExtension, IReadExtension
        obj = self.serviced_object.context
        ext = getMultiAdapter((self.serviced_object, obj,),
                              IExtension, name=self.ext_key)
        self.assert_(verifyObject(IReadExtension, ext))

    def test_verify_extension_registration(self):
        result = self.serviced_object.get_extensions()
        key = self.ext_key
        self.assertTrue(key in result, "Couldn't find the " \
            "extension data. The component must not have been registered " \
            "properly.")

    def test_extension_data_as_callback(self):
        key = '%s.callback' % self.ext_key
        orig_key = self.ext_key
        ext = self.get_extension()
        # First test it without a callback provided
        result = ext.get()
        self.assertFalse(result)
        # Test the provides callback property returns True.
        self.assertTrue(ext.provides_callback)
        # Test for the callback.
        setattr(self.serviced_object.context, 'has_crashed', True)
        result = ext.get_callback()
        self.assertTrue(result)


class TestWriteExtension(BaseExtensionTestCase):

    ext_key = 'crashtest'

    def setUp(self):
        super(TestWriteExtension, self).setUp()
        sm = getSiteManager()
        # Register the example extension
        from wsapi4plone.core.interfaces import (IService, IServiceExtension)
        sm.registerUtility(ICrashTestWriteExtension,
                           provided=IServiceExtension,
                           name=self.ext_key)
        sm.registerAdapter(WriteCrashTestExtension,
                           required=(IService, Interface,),
                           provided=ICrashTestWriteExtension,
                           name=self.ext_key)

    def tearDown(self):
        sm = getSiteManager()
        # Unregister the example extension
        from wsapi4plone.core.interfaces import (IService, IServiceExtension)
        assert sm.unregisterUtility(component=ICrashTestWriteExtension,
                                    provided=IServiceExtension,
                                    name=self.ext_key)
        assert sm.unregisterAdapter(factory=WriteCrashTestExtension,
                                    required=(IService, Interface,),
                                    provided=ICrashTestWriteExtension,
                                    name=self.ext_key)
        super(TestWriteExtension, self).tearDown()

    # We break interface verification because we use keyword arguments in
    # the set method.
    # def test_verfiy_write_provider(self):
    #     from wsapi4plone.core.interfaces import IExtension, IWriteExtension
    #     obj = self.serviced_object.context
    #     ext = getMultiAdapter((self.serviced_object, obj,),
    #                           IExtension, name=self.ext_key)
    #     self.assert_(verifyObject(IWriteExtension, ext))

    def test_get_skeleton(self):
        expected_results = {'has_crashed': {'type': 'bool', 'required': True}}
        ext = self.get_extension()
        results = ext.get_skeleton()
        # Check the results.
        self.assertEqual(results, expected_results)

    def test_set(self):
        has_crashed = True
        # Grab the extension
        ext = self.get_extension()
        ext.set(has_crashed=has_crashed)
        # Verify the change.
        context = self.serviced_object.context
        self.failUnlessEqual(getattr(context, 'has_crashed', None),
            has_crashed)

    def test_set_extensions(self):
        has_crashed = True
        params = {self.ext_key: dict(has_crashed=has_crashed)}
        self.serviced_object.set_extensions(params)
        context = self.serviced_object.context
        self.assertEqual(getattr(context, 'has_crashed', None), has_crashed)


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestReadExtension))
    suite.addTest(unittest.makeSuite(TestWriteExtension))
    return suite
