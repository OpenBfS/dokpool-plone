from AccessControl import allow_class
from AccessControl import allow_module
from zope.i18nmessageid import MessageFactory


allow_module("elan.policy")
allow_module("elan.policy.utils")

DocpoolMessageFactory = MessageFactory('elan.policy')
allow_class(DocpoolMessageFactory)


def initialize(context):
    """Initializer called when used as a Zope 2 product."""
