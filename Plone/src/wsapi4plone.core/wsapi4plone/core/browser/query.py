from logging import getLogger
from Products.CMFCore.utils import getToolByName
from wsapi4plone.core.browser.interfaces import IQuery
from wsapi4plone.core.interfaces import IFormatQueryResults
from zope.component import getUtility
from zope.component.hooks import getSite
from zope.interface import implementer

import DateTime


def _convert_datetime(datetime):
    """
    Convert xmlrpclib.DateTime objects into DateTime.DateTime objects
    """
    # deal with the fact that xmlrpclib.DateTime doesn't do proper ISO 8601
    # formatting (it's missing the hyphens for some reason?)
    dt_str = '%s-%s-%s' % (datetime.value[:4],
                           datetime.value[4:6], datetime.value[6:])
    return DateTime.DateTime(dt_str)


@implementer(IQuery)
class Query(object):
    logger = getLogger(' Query ')

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def query(self, filtr={}):
        """
        @param filtr - search criteria given to filter the results
        """
        # marshal xmlrpclib.DateTime objects into Zope DateTime.DateTime
        # objects so that DateIndex searching works properly
        for k, v in filtr.items():
            if isinstance(v, type({})):
                if 'query' in v:
                    filtr[k]['query'] = [
                        _convert_datetime(x) for x in filtr[k]['query']
                    ]

        catalog = getToolByName(getSite(), 'portal_catalog')
        brains = catalog(filtr)
        formatter = getUtility(IFormatQueryResults)
        self.logger.info(
            "- query - Searching catalog with this search criteria: %s." % (
                filtr)
        )
        return formatter(brains)
