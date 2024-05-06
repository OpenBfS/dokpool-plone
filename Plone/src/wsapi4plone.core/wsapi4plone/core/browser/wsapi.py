from logging import getLogger
from plone.protect.interfaces import IDisableCSRFProtection
from wsapi4plone.core.interfaces import IContextBuilder
from zope.component import getUtility
from zope.interface import alsoProvides


class WSAPI(object):
    logger = getLogger('WS API')

    def __init__(self, context, request):
        """Typical browser view instantiation."""
        self.context = context
        self.request = request
        alsoProvides(request, IDisableCSRFProtection)

        self.builder = getUtility(IContextBuilder)

        self.logger.info('WSAPI request ACTUAL_URL: %s', self.request.ACTUAL_URL)
        self.logger.info('WSAPI request form: %s', self.request.form)
