# -*- coding: utf-8 -*-
__author__ = 'Condat AG'
__docformat__ = 'plaintext'

from docpool.dbaccess.content.forms import *
from docpool.dbaccess.content.registry import registerEntityConfig
from docpool.dbaccess.dbinit import __metadata__
from docpool.dbaccess.dbinit import __session__
from docpool.transfers import DocpoolMessageFactory as _
from docpool.transfers.db.model import *
from elixir import *
from formalchemy import FieldSet
from formalchemy import Grid


session = __session__
metadata = __metadata__


def cFilter(context=None):
    ffs = FieldSet(Channel, session=__session__)
    ffs.permissions.is_collection = True
    ffs.configure(
        include=[
            ffs.title.label(
                _(u"Title")), ffs.permissions.label(
                _(u"Permissions"))]
    )
    return {'form': ffs}


def cListe(context=None):
    g = Grid(Channel, session=__session__)
    g.configure(
        include=[
            g.title.label(
                _(u"Title")), g.timestamp.label(
                _(u"Timestamp"))]
    )
    return {'form': g, 'importRestricted': True,
            'sortNames': ["title", "timestamp"]}


registerEntityConfig(
    "channel",
    Channel,
    gen_fs=True,
    protect=True,
    list_fs=cListe,
    filter_fs=cFilter,
    sort_default='title',
    label=_(u"Channels"),
)
