from AccessControl import allow_class
from AccessControl import allow_module
from zope.i18nmessageid import MessageFactory


allow_module("docpool.policy")
allow_module("docpool.policy.utils")

DocpoolMessageFactory = MessageFactory('docpool.policy')
allow_class(DocpoolMessageFactory)


def initialize(context):
    """Initializer called when used as a Zope 2 product."""
