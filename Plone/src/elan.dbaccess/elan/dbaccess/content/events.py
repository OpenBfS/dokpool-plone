# -*- coding: utf-8 -*-

__author__ = 'Condat AG'
__docformat__ = 'plaintext'

from zope.interface import Interface, implements
from zope.component.interfaces import ObjectEvent
from Products.CMFPlone.utils import log, log_exc

class IObjectAddedEvent(Interface):
    pass

class IObjectChangedEvent(Interface):
    pass

class IObjectDeletedEvent(Interface):
    pass

class ObjectAddedEvent(ObjectEvent):
    implements(IObjectAddedEvent)

    def __init__(self, object, tool, data, context=None):
        ObjectEvent.__init__(self, object)
        self.tool = tool
        self.data = data
        self.context = context
#        log('ObjectAddedEvent -> elan.dbaccess.content.events')

class ObjectChangedEvent(ObjectEvent):
    implements(IObjectChangedEvent)

    def __init__(self, object, tool, diff, context=None, comment=None):
        ObjectEvent.__init__(self, object)
        self.tool = tool
        self.diff = diff
        self.context = context
        self.comment = comment
#        log('ObjectChangedEvent -> elan.dbaccess.content.events')

class ObjectDeletedEvent(ObjectEvent):
    implements(IObjectDeletedEvent)

    def __init__(self, object, tool, context=None):
        ObjectEvent.__init__(self, object)
        self.tool = tool
        self.context = context
#        log('ObjectDeletedEvent -> elan.dbaccess.content.events')
    