# -*- coding: utf-8 -*-

from docpool.base.appregistry import registerApp
# This logic should eventually be bundled in the global docpool.config module to allow for easy customization
from docpool.doksys.local.doksys import dpAdded, dpRemoved
from docpool.doksys.behaviors.doksysdoc import IDoksysDoc
from docpool.doksys.config import DOKSYS_APP

# TODO: register any app specific type extension, doc extension, methods to be executed when docpools are created
registerApp(DOKSYS_APP, u"IMIS Doksys", None, IDoksysDoc, dpAdded, dpRemoved, icon="doksys_app_icon.png", implicit=False)
