# -*- coding: utf-8 -*-
from Products.Archetypes.utils import shasattr

from docpool.base.appregistry import registerApp, createTypeObject, createDocumentObject
from docpool.config.local.base import dpAdded, dpRemoved
from docpool.base.config import BASE_APP


registerApp(BASE_APP, None, None, dpAdded, dpRemoved)