from logging import getLogger

from zope.component import getUtility

from wsapi4plone.core.interfaces import IContextBuilder
from plone.protect.interfaces import IDisableCSRFProtection
from zope.interface import alsoProvides


class WSAPI(object):
    logger = getLogger('WS API')

    def __init__(self, context, request):
        """Typical browser view instantiation."""
        self.context = context
        self.request = request
        alsoProvides(request, IDisableCSRFProtection)

        self.builder = getUtility(IContextBuilder)
