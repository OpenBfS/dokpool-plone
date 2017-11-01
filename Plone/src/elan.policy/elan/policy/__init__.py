# -*- coding: utf-8 -*- 
from AccessControl import allow_module, allow_class
from zope.i18nmessageid import MessageFactory

allow_module("elan.policy");
allow_module("elan.policy.utils");

DocpoolMessageFactory = MessageFactory('elan.policy')
allow_class(DocpoolMessageFactory)

def initialize(context):
    """Initializer called when used as a Zope 2 product."""
