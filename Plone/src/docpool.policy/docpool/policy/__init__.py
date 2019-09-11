from AccessControl import allow_module
from zope.i18nmessageid import MessageFactory

DocpoolMessageFactory = MessageFactory('docpool.policy')
allow_module("docpool.policy")
allow_module("docpool.policy.utils")
