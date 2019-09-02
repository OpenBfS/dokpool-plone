from AccessControl import allow_module
from zope.i18nmessageid import MessageFactory

DocpoolMessageFactory = MessageFactory('elan.policy')

allow_module("elan.policy")
allow_module("elan.policy.utils")
