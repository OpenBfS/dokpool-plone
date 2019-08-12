# -*- coding: utf-8 -*-
__author__ = 'Condat AG'
__docformat__ = 'plaintext'

from datetime import datetime
from docpool.dbaccess.dbinit import __metadata__
from docpool.dbaccess.dbinit import __session__
from docpool.transfers import DocpoolMessageFactory as _
from docpool.transfers.db.security import IDocpoolProtectedEntityClass
from elixir import DateTime
from elixir import Entity
from elixir import EntityBase
from elixir import Field
from elixir import ManyToOne
from elixir import OneToMany
from elixir import setup_all
from elixir import String
from elixir import Unicode
from elixir import using_options
from sqlalchemy import join
from sqlalchemy.orm import column_property
from sqlalchemy.orm import mapper
from sqlalchemy.orm import relation
from zope.interface import classProvides

import logging


metadata = __metadata__
session = __session__


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
    permissions = OneToMany('DocTypePermission', inverse='channel')
    sends = OneToMany('SenderLog', inverse='channel')
    receives = OneToMany('ReceiverLog', inverse='channel')

    def __repr__(self):
        return "%s --> %s (%s)" % (
            self.esd_from_title and self.esd_from_title.encode('utf-8'),
            self.esd_to_title and self.esd_to_title.encode('utf-8'),
            self.title and self.title.encode('utf-8'),
        )


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


class ChannelSends(EntityBase):
    classProvides(IDocpoolProtectedEntityClass)

    def __repr__(self):
        return "%s: --> %s" % (self.etimestamp, self.esd_to_title)


class ChannelReceives(EntityBase):
    classProvides(IDocpoolProtectedEntityClass)


setup_all(create_tables=True)

j = join(
    Channel.table,
    DocTypePermission.table,
    Channel.table.c.id == DocTypePermission.table.c.channel_id,
)
ChannelPermissions.mapper = mapper(
    ChannelPermissions,
    j,
    properties={
        'channel': relation(Channel),
        'channel_id': [Channel.table.c.id, DocTypePermission.table.c.channel_id],
        'id': [DocTypePermission.table.c.id],
    },
)

k = join(
    Channel.table, SenderLog.table, Channel.table.c.id == SenderLog.table.c.channel_id
)
ChannelSends.mapper = mapper(
    ChannelSends,
    k,
    properties={
        'channel': relation(Channel),
        'channel_id': [Channel.table.c.id, SenderLog.table.c.channel_id],
        'id': [SenderLog.table.c.id],
        'ctimestamp': column_property(Channel.table.c.timestamp),
        'etimestamp': column_property(SenderLog.table.c.timestamp),
    },
)

l = join(
    Channel.table,
    ReceiverLog.table,
    Channel.table.c.id == ReceiverLog.table.c.channel_id,
)
ChannelReceives.mapper = mapper(
    ChannelReceives,
    l,
    properties={
        'channel': relation(Channel),
        'channel_id': [Channel.table.c.id, ReceiverLog.table.c.channel_id],
        'id': [ReceiverLog.table.c.id],
        'ctimestamp': column_property(Channel.table.c.timestamp),
        'etimestamp': column_property(ReceiverLog.table.c.timestamp),
    },
)
