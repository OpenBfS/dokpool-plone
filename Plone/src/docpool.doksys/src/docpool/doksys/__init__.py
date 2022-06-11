"""Init and utils."""
from zope.i18nmessageid import MessageFactory

_ = DocpoolMessageFactory = MessageFactory("docpool.doksys")

from docpool.doksys import appregistration  # noqa: F401
