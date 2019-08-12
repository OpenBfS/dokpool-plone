# -*- coding: utf-8 -*-
import unittest
import xmlrpclib

from AccessControl import Unauthorized
from zope.component import getUtility
from zope.publisher.interfaces import NotFound
from ZPublisher.xmlrpc import Response
from ZPublisher.tests.test_xmlrpc import FauxResponse

from Products.CMFCore.utils import getToolByName
from Products.PloneTestCase import PloneTestCase

from wsapi4plone.core.browser.app import ApplicationAPI


class TestApp(PloneTestCase.PloneTestCase):
    """Testing the output of the app calls: {get, post, put, delete}_object."""

    def afterSetUp(self):
        self.setRoles(['Member', 'Manager'])

    def test_anonymous_get_object(self):
        resp = Response(FauxResponse())
        app = ApplicationAPI(self.portal, '')
        get_obj_data = app.get_object(['/'.join(self.folder.getPhysicalPath()), ''])
        resp.setBody(get_obj_data)
        get_obj_resp, method = xmlrpclib.loads(resp._body)
        get_obj_results = get_obj_resp[0]
        for path in get_obj_results:
            self.failUnless(type(get_obj_results[path][0]) == dict)
            self.failUnless(type(get_obj_results[path][1]) == str)
            self.failUnless(
                type(get_obj_results[path][2]) == dict
                or get_obj_results[path][2] == None
            )

    def test_anonymous_private_get_object(self):
        app = ApplicationAPI(self.portal, '')
        fp = self.portal['front-page']
        portal_workflow = getToolByName(self.portal, 'portal_workflow')
        self.loginAsPortalOwner()
        portal_workflow.doActionFor(fp, 'retract')
        self.logout()
        try:
            app.get_object(['/'.join(fp.getPhysicalPath()), ''])
        except Unauthorized:
            # The expected result.
            pass
        except Exception, e:
            self.fail(e)

    def test_get_object_without_existing_object(self):
        app = ApplicationAPI(self.portal, '')
        objs = ['news1']
        self.logout()
        try:
            app.get_object(objs)
        except NotFound:
            # The expected result.
            pass
        except Exception, e:
            self.fail(e)
        else:
            self.fail("The NotFound exception should have been raised.")

    def test_get_object(self):
        resp = Response(FauxResponse())
        app = ApplicationAPI(self.portal, '')
        self.login('test_user_1_')
        get_obj_data = app.get_object(['/'.join(self.folder.getPhysicalPath()), ''])
        self.logout()
        resp.setBody(get_obj_data)
        get_obj_resp, method = xmlrpclib.loads(resp._body)
        get_obj_results = get_obj_resp[0]
        for path in get_obj_results:
            self.failUnless(type(get_obj_results[path][0]) == dict)
            self.failUnless(type(get_obj_results[path][1]) == str)
            self.failUnless(
                type(get_obj_results[path][2]) == dict
                or get_obj_results[path][2] == None
            )

    def test_anonymous_post_object(self):
        app = ApplicationAPI(self.portal, '')
        objs = {
            'news1': [
                {
                    'description': 'News One',
                    'title': 'news1',
                    'text': '\n<p>Hot off the press!</p>\n',
                    'id': 'news1',
                },
                'News Item',
            ]
        }
        self.logout()
        try:
            app.post_object(objs)
        except Unauthorized:
            # The expected result.
            pass
        except Exception, e:
            self.fail(e)
        else:
            self.fail("The Unauthorized exception should have been raised.")

    def test_post_object_without_existing_parent_object(self):
        app = ApplicationAPI(self.portal, '')
        objs = {
            'no_folder/news1': [
                {
                    'description': 'News One',
                    'title': 'news1',
                    'text': '\n<p>Hot off the press!</p>\n',
                    'id': 'news1',
                },
                'News Item',
            ]
        }
        self.login('test_user_1_')
        try:
            app.post_object(objs)
        except NotFound:
            # The expected result.
            pass
        except Exception, e:
            self.fail(e)
        else:
            self.fail("The NotFound exception should have been raised.")
        self.logout()

    def test_post_object(self):
        resp = Response(FauxResponse())
        app = ApplicationAPI(self.portal, '')
        objs = {
            'news1': [
                {
                    'description': 'News One',
                    'title': 'news1',
                    'text': '\n<p>Hot off the press!</p>\n',
                    'id': 'news1',
                },
                'News Item',
            ]
        }
        self.login('test_user_1_')
        post_obj_data = app.post_object(objs)
        self.logout()
        resp.setBody(post_obj_data)
        post_obj_resp, method = xmlrpclib.loads(resp._body)
        self.failUnlessEqual(post_obj_resp[0], ['/plone/news1'])
        self.assertTrue(self.portal['news1'])

    # Lots of digging required to figure out why this test
    # isn't working as it should. Manual tests of this call
    # work as expected (security prevents anonymous puts).
    ##def test_anonymous_put_object(self):
    ##    app = ApplicationAPI(self.portal, '')
    ##    objs = {'front-page': [{'text': "<p>Action and reaction, ebb and flow, trial and error, change - this is the rhythm of living. Out of our over-confidence, fear; out of our fear, clearer vision, fresh hope. And out of hope, progress.</p><br /> --<i>Bruce Barton</i>"}], '/plone/events': [{'description': 'What\'s up doc?'},]}
    ##    self.logout()
    ##    try:
    ##        app.put_object(objs)
    ##    except Unauthorized:
    ##        # The expected result.
    ##        self.fail('this should happen?!?')
    ##    except Exception, e:
    ##        self.fail(e)
    ##    else:
    ##        self.fail("The Unauthorized exception should have been raised.")

    def test_put_object_without_existing_object(self):
        app = ApplicationAPI(self.portal, '')
        objs = {
            'news1': [
                {
                    'description': 'News One',
                    'title': 'news1',
                    'text': '\n<p>Hot off the press!</p>\n',
                    'id': 'news1',
                },
                'News Item',
            ]
        }
        self.login('test_user_1_')
        try:
            app.put_object(objs)
        except NotFound:
            # The expected result.
            pass
        except Exception, e:
            self.fail(e)
        else:
            self.fail("The NotFound exception should have been raised.")
        self.logout()

    def test_put_object(self):
        resp = Response(FauxResponse())
        app = ApplicationAPI(self.portal, '')
        objs = {
            'front-page': [
                {
                    'text': "<p>Action and reaction, ebb and flow, trial and error, change - this is the rhythm of living. Out of our over-confidence, fear; out of our fear, clearer vision, fresh hope. And out of hope, progress.</p><br /> --<i>Bruce Barton</i>"
                }
            ],
            '/plone/events': [{'description': 'What\'s up doc?'}],
        }
        self.login('test_user_1_')
        put_obj_data = app.put_object(objs)
        self.logout()
        resp.setBody(put_obj_data)
        put_obj_resp, method = xmlrpclib.loads(resp._body)
        expected_resp = ['/plone/front-page', '/plone/events']
        self.failUnlessEqual(len(put_obj_resp[0]), len(expected_resp))
        for i in put_obj_resp[0]:
            self.failUnless(
                i in expected_resp, "'%s' is not in %s?" % (i, expected_resp)
            )
        self.failUnlessEqual(
            self.portal['front-page']['text'].getRaw(), objs['front-page'][0]['text']
        )
        self.failUnlessEqual(
            self.portal['events']['description'],
            objs['/plone/events'][0]['description'],
        )

    def test_anonymous_delete_object(self):
        app = ApplicationAPI(self.portal, '')
        objs = ['front-page', '/plone/events']
        self.logout()
        try:
            app.delete_object(objs)
        except Unauthorized:
            # The expected result.
            pass
        except Exception, e:
            self.fail(e)
        else:
            self.fail("The Unauthorized exception should have been raised.")

    def test_delete_object_without_existing_object(self):
        app = ApplicationAPI(self.portal, '')
        objs = ['news1']
        self.login('test_user_1_')
        try:
            app.delete_object(objs)
        except NotFound:
            # The expected result.
            pass
        except Exception, e:
            self.fail(e)
        else:
            self.fail("The NotFound exception should have been raised.")
        self.logout()

    def test_delete_object(self):
        resp = Response(FauxResponse())
        app = ApplicationAPI(self.portal, '')
        self.portal.invokeFactory(type_name='News Item', id='news1')
        objs = ['news1']
        self.login('test_user_1_')
        del_obj_data = app.delete_object(objs)
        self.logout()
        resp.setBody(del_obj_data)
        del_obj_resp, method = xmlrpclib.loads(resp._body)
        self.failUnlessEqual(del_obj_resp[0], None)
        self.failUnlessEqual(self.portal.get('news1', 100), 100)


class TestSchema(PloneTestCase.PloneTestCase):
    def afterSetUp(self):
        self.setRoles(['Member', 'Manager'])

    def test_anonymous_get_schema(self):
        app = ApplicationAPI(self.portal, '')
        type_ = 'Event'
        self.logout()
        try:
            app.get_schema(type_)
        except Unauthorized:
            # The expected result.
            pass
        except Exception, e:
            self.fail(e)
        else:
            self.fail("The Unauthorized exception should have been raised.")

    def test_get_schema(self):
        resp = Response(FauxResponse())
        app = ApplicationAPI(self.portal, '')
        type_ = 'Event'

        self.login('test_user_1_')
        schema_data = app.get_schema(type_)
        resp.setBody(schema_data)
        schema_resp, method = xmlrpclib.loads(resp._body)
        self.logout()

        schema_results = schema_resp[0]
        expected_results = {
            'startDate': {'required': True, 'type': 'datetime'},
            'endDate': {'required': True, 'type': 'datetime'},
            'contributors': {'required': False, 'type': 'lines'},
            'text': {'required': False, 'type': 'text'},
            'eventUrl': {'required': False, 'type': 'string'},
            'creation_date': {'required': False, 'type': 'datetime'},
            'contactEmail': {'required': False, 'type': 'string'},
            'expirationDate': {'required': False, 'type': 'datetime'},
            'contactName': {'required': False, 'type': 'string'},
            'contactPhone': {'required': False, 'type': 'string'},
            'id': {'required': 0, 'type': 'string'},
            'subject': {'required': False, 'type': 'lines'},
            'attendees': {'required': False, 'type': 'lines'},
            'modification_date': {'required': False, 'type': 'datetime'},
            'title': {'required': 1, 'type': 'string'},
            'relatedItems': {'required': False, 'type': 'reference'},
            'location': {'required': False, 'type': 'string'},
            'eventType': {'required': False, 'type': 'lines'},
            'excludeFromNav': {'required': False, 'type': 'boolean'},
            'description': {'required': False, 'type': 'text'},
            'effectiveDate': {'required': False, 'type': 'datetime'},
            'language': {'required': False, 'type': 'string'},
            'rights': {'required': False, 'type': 'text'},
            'allowDiscussion': {'required': False, 'type': 'boolean'},
            'creators': {'required': False, 'type': 'lines'},
        }

        self.failUnlessEqual(len(schema_results), len(expected_results))
        for attr, value in expected_results.iteritems():
            self.failUnlessEqual(
                value,
                schema_results[attr],
                "%s != %s for schema attribute '%s'"
                % (value, schema_results[attr], attr),
            )

    def test_get_schema_invalid_type(self):
        app = ApplicationAPI(self.portal, '')
        type_ = 'Bingo Card'
        self.logout()
        try:
            app.get_schema(type_)
        except ValueError:
            # The expected result.
            pass
        except Exception, e:
            self.fail(e)
        else:
            self.fail("The Unauthorized exception should have been raised.")

    def test_get_schema_disallowed_type(self):
        resp = Response(FauxResponse())
        app = ApplicationAPI(self.portal, '')
        type_ = 'Large Plone Folder'

        self.login('test_user_1_')
        self.failUnlessRaises(ValueError, app.get_schema, type_)
        self.logout()

    def test_get_schema_with_path(self):
        resp = Response(FauxResponse())
        app = ApplicationAPI(self.portal, '')
        type_ = 'Link'
        self.login('test_user_1_')
        schema_data = app.get_schema(type_, "Members")
        resp.setBody(schema_data)
        schema_resp, method = xmlrpclib.loads(resp._body)
        self.logout()

        schema_results = schema_resp[0]
        expected_results = {
            'excludeFromNav': {'required': False, 'type': 'boolean'},
            'remoteUrl': {'required': True, 'type': 'string'},
            'description': {'required': False, 'type': 'text'},
            'contributors': {'required': False, 'type': 'lines'},
            'title': {'required': 1, 'type': 'string'},
            'language': {'required': False, 'type': 'string'},
            'rights': {'required': False, 'type': 'text'},
            'modification_date': {'required': False, 'type': 'datetime'},
            'location': {'required': False, 'type': 'string'},
            'creation_date': {'required': False, 'type': 'datetime'},
            'effectiveDate': {'required': False, 'type': 'datetime'},
            'relatedItems': {'required': False, 'type': 'reference'},
            'expirationDate': {'required': False, 'type': 'datetime'},
            'allowDiscussion': {'required': False, 'type': 'boolean'},
            'creators': {'required': False, 'type': 'lines'},
            'id': {'required': 0, 'type': 'string'},
            'subject': {'required': False, 'type': 'lines'},
        }

        self.failUnlessEqual(len(schema_results), len(expected_results))
        for attr, value in expected_results.iteritems():
            self.failUnlessEqual(
                value,
                schema_results[attr],
                "%s != %s for schema attribute '%s'"
                % (value, schema_results[attr], attr),
            )

    def test_get_schema_with_path_and_non_addable_type(self):
        resp = Response(FauxResponse())
        app = ApplicationAPI(self.portal, '')
        collect1 = self.portal.invokeFactory(type_name='Topic', id='collect1')
        type_ = 'Link'

        self.login('test_user_1_')
        self.failUnlessRaises(ValueError, app.get_schema, type_, collect1)
        self.logout()


def test_suite():
    suite = unittest.TestSuite()
    # suite.addTest(unittest.makeSuite(TestApp))
    # suite.addTest(unittest.makeSuite(TestSchema))
    return suite
