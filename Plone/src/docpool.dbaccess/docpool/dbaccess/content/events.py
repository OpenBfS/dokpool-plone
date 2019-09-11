# -*- coding: utf-8 -*-

__author__ = 'Condat AG'
__docformat__ = 'plaintext'

from zope.component.interfaces import ObjectEvent
from zope.interface import implementer
from zope.interface import Interface


class IObjectAddedEvent(Interface):
    pass


class IObjectChangedEvent(Interface):
    pass


class IObjectDeletedEvent(Interface):
    pass


@implementer(IObjectAddedEvent)
class ObjectAddedEvent(ObjectEvent):

    def __init__(self, object, tool, data, context=None):
        ObjectEvent.__init__(self, object)
        self.tool = tool
        self.data = data
        self.context = context


#        log('ObjectAddedEvent -> docpool.dbaccess.content.events')


@implementer(IObjectChangedEvent)
class ObjectChangedEvent(ObjectEvent):

    def __init__(self, object, tool, diff, context=None, comment=None):
        ObjectEvent.__init__(self, object)
        self.tool = tool
        self.diff = diff
        self.context = context
        self.comment = comment


#        log('ObjectChangedEvent -> docpool.dbaccess.content.events')


@implementer(IObjectDeletedEvent)
class ObjectDeletedEvent(ObjectEvent):

    def __init__(self, object, tool, context=None):
        ObjectEvent.__init__(self, object)
        self.tool = tool
        self.context = context


#        log('ObjectDeletedEvent -> docpool.dbaccess.content.events')
