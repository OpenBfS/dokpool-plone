from AccessControl import allow_module
from zope.i18nmessageid import MessageFactory

DocpoolMessageFactory = MessageFactory("docpool.transfers")

from docpool.transfers import appregistration  # noqa: F401

allow_module("docpool.transfers.config")
allow_module("docpool.transfers.utils")
