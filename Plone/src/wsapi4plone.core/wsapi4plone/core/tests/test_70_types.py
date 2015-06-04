# -*- coding: utf-8 -*-
import unittest
import xmlrpclib

from zope.component import getUtility
from ZPublisher.xmlrpc import Response
from ZPublisher.tests.test_xmlrpc import FauxResponse

from Products.PloneTestCase import PloneTestCase

from wsapi4plone.core.browser.types import Types

class TestTypes(PloneTestCase.PloneTestCase):
    """What kind of content-types do we have the ability to add using the
    'get_types' call."""

    def test_types(self):
        resp = Response(FauxResponse())
        t = Types(self.folder, '')
        type_results = [ [x.id, x.title_or_id()] for x in self.folder.allowedContentTypes() ]
        t_data = t.get_types()
        resp.setBody(t_data)
        t_body = resp._body
        t_resp, method = xmlrpclib.loads(t_body)
        t_results = t_resp[0]
        self.failUnlessEqual(type_results, t_results)

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestTypes))
    return suite

