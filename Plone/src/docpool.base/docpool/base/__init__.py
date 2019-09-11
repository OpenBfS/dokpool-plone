# -*- coding: utf-8 -*-
from AccessControl import allow_module
from zope.i18nmessageid import MessageFactory
from docpool.base import monkey  # noqa: F401
from plone import api

DocpoolMessageFactory = MessageFactory('docpool.base')

from docpool.base import appregistration  # noqa: F401

allow_module("docpool.base")
allow_module("docpool.base.config")
allow_module("docpool.base.utils")
api.__allow_access_to_unprotected_subobjects__ = 1
api.user.__allow_access_to_unprotected_subobjects__ = 1
api.group.__allow_access_to_unprotected_subobjects__ = 1
