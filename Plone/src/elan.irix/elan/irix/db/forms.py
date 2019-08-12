# -*- coding: utf-8 -*-
__author__ = 'Condat AG'
__docformat__ = 'plaintext'

from docpool.dbaccess.content.forms import *
from docpool.dbaccess.content.registry import registerEntityConfig
from docpool.dbaccess.dbinit import __metadata__
from docpool.dbaccess.dbinit import __session__
from elan.irix import DocpoolMessageFactory as _
from elixir import *
from formalchemy import Grid
from model import *


session = __session__
metadata = __metadata__


def cListe(context=None):
    g = Grid(IRIXReport, session=__session__)
    g.configure(
        include=[g.title.label(_(u"Title")), g.timestamp.label(_(u"Timestamp"))]
    )
    return {'form': g, 'importRestricted': True, 'sortNames': ["title", "timestamp"]}


registerEntityConfig(
    "irixreport",
    IRIXReport,
    gen_fs=True,
    protect=True,
    edit_fs=IRIXReport.edit_fs,
    create_fs=IRIXReport.create_fs,
    sort_default='title',
    label=_(u"IRIX Reports"),
)
