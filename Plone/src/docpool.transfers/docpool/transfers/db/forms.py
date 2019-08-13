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
from formalchemy import FieldRenderer
from formalchemy import FieldSet
from formalchemy import Grid
from formalchemy.fields import HiddenFieldRenderer
from Products.Archetypes.utils import shasattr
from Products.CMFPlone.utils import safe_unicode


session = __session__
metadata = __metadata__


perm_options = [
    (_(u'publish immediately'), 'publish'),
    (_(u'don\'t accept'), 'block'),
    (_(u'needs confirmation'), 'confirm'),
]


def p_pre_filter(context):
    """
    """
    if shasattr(context, "myDPTransferFolder", acquire=True):
        channel_id = context.channelId()
        if channel_id:
            return {
                'ChannelPermissions--channel_id': channel_id,
                'ChannelPermissions-_-channel_id': channel_id,
            }
    return {}


def cpFilter(context=None):
    """
    """
    ffs = FieldSet(ChannelPermissions, session=__session__)
    ffs.channel.is_collection = True
    self = context.getContextObj()
    if shasattr(self, "myDPTransferFolder", acquire=True):
        c_field = ffs.channel_id.with_renderer(HiddenFieldRenderer)
    else:
        c_field = ffs.channel.with_null_as(
            ('---', '')).dropdown(multiple=True, size=5)
    ffs.configure(
        include=[
            c_field,
            ffs.doc_type.label(_(u"Doc. type short")),
            ffs.perm.label(_("Permission")),
        ]
    )
    return {'form': ffs, 'filter': p_pre_filter}


def cpListe(context=None):
    """
    This method unfortunately needs a side effect:
    The current set of common doc types needs to be reflected in the database.
    """

    class DTRenderer(FieldRenderer):
        def render_readonly(self, **kwargs):
            """render html for read only mode"""
            # print self._value
            # print self.dts
            if self._value and self._value in self.dts:
                return u"%s (%s)" % (
                    safe_unicode(self.dts[self._value]),
                    safe_unicode(self._value),
                )
            else:
                return self._value

    obj = context.getContextObj()
    # print obj
    if shasattr(obj, "myDocumentTypes", True):
        # print "ja"
        dts = obj.myDocumentTypes()
        DTRenderer.dts = {}
        for dt in dts:
            DTRenderer.dts[safe_unicode(dt[0])] = dt[1]

        # Here me make sure that all current matching document types are in the
        # database.
        obj.ensureMatchingDocumentTypesInDatabase()
    else:
        DTRenderer.dts = {}
    g = Grid(ChannelPermissions, session=__session__)
    g.configure(
        include=[
            g.id.with_renderer(HiddenFieldRenderer),
            g.doc_type.label(_(u"Doc. type (short)"))
            .readonly()
            .with_renderer(DTRenderer),
            g.perm.label(_("Permission")).dropdown(perm_options),
        ]
    )
    return {'form': g, 'importRestricted': True,
            'sortNames': ["doc_type", "perm"]}


def cpEdit(context=None):

    fs = FieldSet(ChannelPermissions, session=__session__)
    fs.configure(include=[fs.id, fs.perm])
    return fs


registerEntityConfig(
    "channelpermissions",
    ChannelPermissions,
    gen_fs=True,
    protect=True,
    list_fs=cpListe,
    filter_fs=cpFilter,
    edit_fs=cpEdit,
    sort_default='doc_type',
    label=_(u"Permissions"),
)


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
