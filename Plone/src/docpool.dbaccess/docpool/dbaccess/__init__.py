# -*- coding: utf-8 -*-
from AccessControl import allow_class
from AccessControl import allow_module
from docpool.dbaccess.content.errors import ObjectDuplicateException
from zope.i18nmessageid import MessageFactory


DocpoolMessageFactory = MessageFactory('docpool.dbaccess')


allow_class(ObjectDuplicateException)
allow_module("docpool.dbaccess")
allow_module("docpool.dbaccess.utils")
