# -*- coding: utf-8 -*-

from docpool.base.appregistry import registerApp

# This logic should eventually be bundled in the global docpool.config module to allow for easy customization
from docpool.rei.local.rei import dpAdded, dpRemoved
from docpool.rei.behaviors.reidoc import IREIDoc
from docpool.rei.behaviors.reitype import IREIType
from docpool.rei.config import REI_APP

# TODO: register any app specific type extension, doc extension, methods to be executed when docpools are created
registerApp(
    REI_APP,
    u"REI",
    IREIType,
    IREIDoc,
    dpAdded,
    dpRemoved,
    icon="rei_app_icon.png",
    implicit=False,
)
