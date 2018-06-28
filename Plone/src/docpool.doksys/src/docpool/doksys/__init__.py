# -*- coding: utf-8 -*-
"""Init and utils."""
from AccessControl import allow_class
from zope.i18nmessageid import MessageFactory
from docpool.base.appregistry import registerApp

DocpoolMessageFactory = MessageFactory('docpool.doksys')
allow_class(DocpoolMessageFactory)

import appregistration


