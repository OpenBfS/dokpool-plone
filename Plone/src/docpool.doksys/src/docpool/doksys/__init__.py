# -*- coding: utf-8 -*-
"""Init and utils."""
from AccessControl import allow_class
from docpool.doksys import appregistration  # noqa: F401
from zope.i18nmessageid import MessageFactory


_ = DocpoolMessageFactory = MessageFactory('docpool.doksys')
allow_class(DocpoolMessageFactory)
