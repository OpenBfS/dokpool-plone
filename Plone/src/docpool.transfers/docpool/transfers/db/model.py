# -*- coding: utf-8 -*-
__author__ = 'Condat AG'
__docformat__ = 'plaintext'

from zope.interface.declarations import classImplements
from zope.interface import Interface, implements, classProvides, directlyProvides

from docpool.dbaccess.dbinit import __metadata__, __session__

metadata = __metadata__
session = __session__

from elixir import Entity, EntityBase, Field, String, Unicode, DateTime, OneToMany, ManyToOne, using_options, setup_all
from sqlalchemy import or_, and_, join
from sqlalchemy.orm import mapper, class_mapper, relation, backref, column_property, ColumnProperty
import logging
from datetime import datetime
from docpool.transfers import DocpoolMessageFactory as _
from docpool.transfers.db.security import IDocpoolProtectedEntityClass

DEBUG = 0
__metadata__.bind.echo = False
if DEBUG:
    __metadata__.bind.echo = True
logger = logging.getLogger("docpool.transfers")


class Channel(Entity):
    """
    """
    classProvides(IDocpoolProtectedEntityClass)
    using_options(tablename='channels')
    
    title = Field(Unicode(128))
    esd_from_uid = Field(String(50))
    esd_from_title = Field(Unicode(100))    
    tf_uid = Field(String(50))
    esd_to_title = Field(Unicode(100))
    timestamp = Field(DateTime(), default=datetime.now)
    permissions = OneToMany('DocTypePermission',inverse='channel')
    sends = OneToMany('SenderLog',inverse='channel')
    receives = OneToMany('ReceiverLog',inverse='channel')
    
    def __repr__(self):
        return "%s --> %s (%s)" % (self.esd_from_title and self.esd_from_title.encode('utf-8'), self.esd_to_title and self.esd_to_title.encode('utf-8'), self.title and self.title.encode('utf-8'))

class DocTypePermission(Entity):
    """
    """
    classProvides(IDocpoolProtectedEntityClass)
    using_options(tablename='dtpermissions')
    doc_type = Field(String(80))
    perm = Field(String(20))
    channel = ManyToOne('Channel', ondelete='cascade', required=True)
    
    def __repr__(self):
        return "%s: %s" % (self.doc_type, _(self.perm))
    
class SenderLog(Entity):
    """
    """
    classProvides(IDocpoolProtectedEntityClass)
    using_options(tablename='senderlogs')
    document_uid = Field(String(50))
    document_title = Field(Unicode(250))
    timestamp = Field(DateTime())
    user = Field(String(100))
    scenario_ids = Field(String(150))
    channel = ManyToOne('Channel')

class ReceiverLog(Entity):
    """
    """
    classProvides(IDocpoolProtectedEntityClass)
    using_options(tablename='receiverlogs')
    document_uid = Field(String(50))
    document_title = Field(Unicode(250))
    timestamp = Field(DateTime())
    user = Field(String(100))
    scenario_ids = Field(String(150))
    channel = ManyToOne('Channel')

class ChannelPermissions(EntityBase):
    classProvides(IDocpoolProtectedEntityClass)
    pass

class ChannelSends(EntityBase):
    classProvides(IDocpoolProtectedEntityClass)
    
    def __repr__(self):
        return "%s: --> %s" % (self.etimestamp, self.esd_to_title)

class ChannelReceives(EntityBase):
    classProvides(IDocpoolProtectedEntityClass)
    pass

setup_all(create_tables=True)

j = join(Channel.table, DocTypePermission.table, Channel.table.c.id==DocTypePermission.table.c.channel_id)
ChannelPermissions.mapper = mapper(ChannelPermissions, j, properties={
    'channel': relation(Channel),
    'channel_id': [Channel.table.c.id, DocTypePermission.table.c.channel_id],
    'id' : [DocTypePermission.table.c.id]
})

k = join(Channel.table, SenderLog.table, Channel.table.c.id==SenderLog.table.c.channel_id)
ChannelSends.mapper = mapper(ChannelSends, k, properties={
    'channel': relation(Channel),
    'channel_id': [Channel.table.c.id, SenderLog.table.c.channel_id],
    'id' : [SenderLog.table.c.id],
    'ctimestamp' : column_property(Channel.table.c.timestamp),
    'etimestamp' : column_property(SenderLog.table.c.timestamp)
})

l = join(Channel.table, ReceiverLog.table, Channel.table.c.id==ReceiverLog.table.c.channel_id)
ChannelReceives.mapper = mapper(ChannelReceives, l, properties={
    'channel': relation(Channel),
    'channel_id': [Channel.table.c.id, ReceiverLog.table.c.channel_id],
    'id' : [ReceiverLog.table.c.id],
    'ctimestamp' : column_property(Channel.table.c.timestamp),
    'etimestamp' : column_property(ReceiverLog.table.c.timestamp)

})
