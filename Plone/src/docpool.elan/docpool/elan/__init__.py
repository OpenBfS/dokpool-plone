from AccessControl import allow_module
from docpool.elan import monkey  # noqa: F401
from zope.i18nmessageid import MessageFactory


DocpoolMessageFactory = MessageFactory("docpool.elan")

from docpool.elan import appregistration  # noqa: F401


allow_module("docpool.elan.config")
allow_module("docpool.elan.utils")
