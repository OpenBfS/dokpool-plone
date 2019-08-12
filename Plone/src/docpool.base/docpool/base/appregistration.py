# -*- coding: utf-8 -*-

from docpool.base.appregistry import registerApp
from docpool.base.config import BASE_APP
from docpool.config.local.base import dpAdded
from docpool.config.local.base import dpRemoved


registerApp(BASE_APP, u"Docpool Base", None, None, dpAdded, dpRemoved)
# "None" means: no extension support
