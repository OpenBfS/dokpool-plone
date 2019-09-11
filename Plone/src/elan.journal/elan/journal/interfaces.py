# -*- coding: utf-8 -*-
from elan.journal import _
from plone.app.textfield import RichText
from plone.namedfile.field import NamedBlobImage
from zope.interface import Interface


class IBrowserLayer(Interface):

    """A layer specific for this add-on product."""


class IJournal(Interface):

    """A journal is a blog post which is intended to provide a rolling
    textual coverage of an ongoing event.
    """
