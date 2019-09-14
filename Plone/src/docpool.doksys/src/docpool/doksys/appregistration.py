# -*- coding: utf-8 -*-

from docpool.base.appregistry import registerApp
from docpool.doksys.behaviors.doksysdoc import IDoksysDoc
from docpool.doksys.config import DOKSYS_APP

# This logic should eventually be bundled in the global docpool.config
# module to allow for easy customization
from docpool.doksys.local.doksys import dpAdded
from docpool.doksys.local.doksys import dpRemoved


# TODO: register any app specific type extension, doc extension, methods
# to be executed when docpools are created
registerApp(
    DOKSYS_APP,
    u"IMIS Doksys",
    None,
    IDoksysDoc,
    dpAdded,
    dpRemoved,
    # Todo Skins folder
    # /src/docpool.elan/docpool/elan/skins/docpool_elan_images/
    icon="doksys_app_icon.png",
    implicit=False,
    # ./src/docpool.theme/docpool/theme/skins/docpooltheme_images/
    logo="doksyslogo.png",
)
