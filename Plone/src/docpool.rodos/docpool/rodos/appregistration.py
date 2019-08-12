# -*- coding: utf-8 -*-

from docpool.base.appregistry import registerApp

# This logic should eventually be bundled in the global docpool.config module to allow for easy customization
from docpool.rodos.local.rodos import dpAdded, dpRemoved
from docpool.rodos.behaviors.rodosdoc import IRodosDoc
from docpool.rodos.behaviors.rodostype import IRodosType
from docpool.rodos.config import Rodos_APP

# TODO: register any app specific type extension, doc extension, methods to be executed when docpools are created
registerApp(
    Rodos_APP,
    u"RODOS",
    IRodosType,
    IRodosDoc,
    dpAdded,
    dpRemoved,
    icon="rodos_app_icon.png",
    implicit=False,
)
