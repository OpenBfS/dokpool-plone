from AccessControl import allow_module
from zope.i18nmessageid import MessageFactory

DocpoolMessageFactory = MessageFactory("docpool.event")

allow_module("docpool.event.utils")
