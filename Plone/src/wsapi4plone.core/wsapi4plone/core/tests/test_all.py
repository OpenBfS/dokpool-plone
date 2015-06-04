# -*- coding: utf-8 -*-
import os
import doctest
import unittest
import xmlrpclib

from Products.Five import zcml
from Products.PloneTestCase import PloneTestCase
from Products.PloneTestCase.layer import onsetup
from Testing import ZopeTestCase

import wsapi4plone.core as wsapi4plone

DOCTESTFLAGS = (doctest.ELLIPSIS |
    # doctest.REPORT_ONLY_FIRST_FAILURE |
    doctest.NORMALIZE_WHITESPACE)

@onsetup
def setup():
    zcml.load_config('configure.zcml', wsapi4plone)

setup()
PloneTestCase.setupPloneSite()

def format_xmlrpc(method_name, params=tuple()):
    return xmlrpclib.dumps(params, method_name)


class DocTestCase(PloneTestCase.PloneTestCase):

    def afterSetUp(self):
        usr = pwd = 'test_user_1'
        self.loginAsPortalOwner()
        self.app.plone.portal_registration.addMember(usr, pwd,
            properties={'username': usr, 'fullname': 'test user', 'email': 'test@example.com'})
        self.app.plone.portal_groups.getGroupById('Administrators').addMember(usr)
        self.logout()
        response = self.publish("plone/login_form?came_from=&form.submitted=1&js_enabled=0&cookies_enabled=&login_name=&pwd_empty=0&__ac_name=%s&__ac_password=%s&submit=Log+in" % (usr, pwd))
        self.cookie = '__ac="%s"; Path=/' % response.getCookie('__ac')['value']


class WorkflowDocTestCase(DocTestCase):

    def afterSetUp(self):
        DocTestCase.afterSetUp(self)
        self.logout()
        self.login('test_user_1')
        self.portal.invokeFactory('Folder', 'folder1')
        self.logout()

    def beforeTearDown(self):
        self.loginAsPortalOwner()
        self.portal.manage_delObjects('folder1')
        self.logout()


def test_suite():
    suite = unittest.TestSuite()
    # suite.addTest(
    #     ZopeTestCase.FunctionalDocFileSuite(
    #         'sys.txt', package='wsapi4plone.core.browser',
    #         test_class=DocTestCase,
    #         optionflags=DOCTESTFLAGS,
    #         globs=dict(format_xmlrpc=format_xmlrpc)) )
    suite.addTest(doctest.DocTestSuite('wsapi4plone.core.utilities.scrubber'))
    suite.addTest(doctest.DocTestSuite('wsapi4plone.core.utilities.lookup'))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')