# -*- coding: utf-8 -*-
__author__ = 'Condat AG'
__docformat__ = 'plaintext'

from model import *
from docpool.dbaccess.dbinit import __session__, __metadata__

session = __session__
metadata = __metadata__

from elixir import *

from docpool.dbaccess.content.dbadmin import (
    registerEntityConfig,
    registerExportDBObjectConfig,
)
from docpool.dbaccess.content.forms import *

from formalchemy import FieldSet, Grid
from formalchemy import config
from formalchemy import types
from formalchemy import Field
from formalchemy import FieldRenderer
from formalchemy.validators import email, required
from formalchemy.fields import HiddenFieldRenderer

from Products.Archetypes.utils import shasattr
from Products.CMFPlone.utils import safe_unicode
from elan.irix import DocpoolMessageFactory as _


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
