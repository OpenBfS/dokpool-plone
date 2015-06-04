# -*- coding: utf-8 -*-
import os
import xmlrpclib

from DateTime import DateTime
import wsapi4plone.core as wsapi4plone

MEMBERS_SKELETON = {'allowDiscussion': {'required': False, 'type': 'boolean'},
                    'constrainTypesMode': {'required': False, 'type': 'integer'},
                    'contributors': {'required': False, 'type': 'lines'},
                    'creation_date': {'required': False, 'type': 'datetime'},
                    'creators': {'required': False, 'type': 'lines'},
                    'description': {'required': False, 'type': 'text'},
                    'effectiveDate': {'required': False, 'type': 'datetime'},
                    'excludeFromNav': {'required': False, 'type': 'boolean'},
                    'expirationDate': {'required': False, 'type': 'datetime'},
                    'id': {'required': 0, 'type': 'string'},
                    'immediatelyAddableTypes': {'required': False, 'type': 'lines'},
                    'language': {'required': False, 'type': 'string'},
                    'locallyAllowedTypes': {'required': False, 'type': 'lines'},
                    'location': {'required': False, 'type': 'string'},
                    'modification_date': {'required': False, 'type': 'datetime'},
                    'relatedItems': {'required': False, 'type': 'reference'},
                    'rights': {'required': False, 'type': 'text'},
                    'subject': {'required': False, 'type': 'lines'},
                    'title': {'required': 1, 'type': 'string'}}

MEMBERS_VALUES = {'allowDiscussion': False,
                  'constrainTypesMode': 0,
                  'contributors': (),
                  'creation_date': DateTime('2009/05/11 17:58:08.876 GMT-4'),
                  'creators': ('portal_owner',),
                  'description': "Container for users' home directories",
                  'effectiveDate': None,
                  'excludeFromNav': False,
                  'expirationDate': None,
                  'id': 'Members',
                  'immediatelyAddableTypes': ['Document',
                                              'Event',
                                              'Favorite',
                                              'File',
                                              'Image',
                                              'Link',
                                              'Folder',
                                              'News Item',
                                              'Topic'],
                  'language': '',
                  'locallyAllowedTypes': ['Document',
                                          'Event',
                                          'Favorite',
                                          'File',
                                          'Folder',
                                          'Image',
                                          'Link',
                                          'News Item',
                                          'Topic'],
                  'location': '',
                  'modification_date': DateTime('2009/05/11 17:58:13.484 GMT-4'),
                  'relatedItems': [],
                  'rights': '',
                  'subject': (),
                  'title': 'Users'}

MEMBERS_TYPE = 'Large Plone Folder'

MEMBERS_CHANGES = {'title': 'Members',
                   'description': "Container for members' home directories"}

data = open(os.path.join(wsapi4plone.__path__[0], 'tests', 'image.png')).read()
IMAGE1 = {'image': {'alt': 'image1',
                    'content_type': 'image/png',
                    'data': xmlrpclib.Binary(data),
                    'height': 10,
                    'size': 262,
                    'title': 'image1',
                    'width': 10}}

PORTAL_SKELETON = {'description': {'required': False, 'type': 'string'},
                   'id': {'required': True, 'type': 'string'},
                   'title': {'required': True, 'type': 'string'}}

PORTAL_VALUES = {'title': 'Plone site', 'id': 'plone', 'description': ''}
