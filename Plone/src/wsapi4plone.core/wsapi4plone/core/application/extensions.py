# -*- coding: utf-8 -*-
from zope.component import getUtility
from zope.interface import implements

from wsapi4plone.core.interfaces import IFormatQueryResults
from wsapi4plone.core.extension import BaseExtension
from wsapi4plone.core.application.interfaces import (
    IPloneContents, IContentsQuery,)


class PloneContents(BaseExtension):
    implements(IPloneContents)

    @property
    def contents_query(self):
        if getattr(self, '_content_query', None) is None:
            self._contents_query = IContentsQuery(self.context)
        return self._contents_query

    def get_callback(self):
        query_args = self.contents_query.arguments()
        contents = {'function': 'query',
                    'args': query_args}

    def get(self):
        formatter = getUtility(IFormatQueryResults)
        return formatter(self.contents_query.results())


class BaseContentQuery(object):

    def __init__(self, context):
        self.context = context

    def results(self):
        return self.context.portal_catalog(*self.arguments())


class PloneFolderContents(BaseContentQuery):

    def arguments(self):
        arg = {'path': {
            'query': '/'.join(self.context.getPhysicalPath()), 'depth': 1}
            }
        return (arg,)
