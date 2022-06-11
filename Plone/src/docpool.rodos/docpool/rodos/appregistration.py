from docpool.base.appregistry import registerApp
from docpool.rodos.behaviors.rodosdoc import IRodosDoc
from docpool.rodos.behaviors.rodostype import IRodosType
from docpool.rodos.config import RODOS_APP

# This logic should eventually be bundled in the global docpool.config
# module to allow for easy customization
from docpool.rodos.local.rodos import dpAdded, dpRemoved

# TODO: register any app specific type extension, doc extension, methods
# to be executed when docpools are created
registerApp(
    RODOS_APP,
    "RODOS",
    IRodosType,
    IRodosDoc,
    dpAdded,
    dpRemoved,
    # Todo Skins folder
    # /src/docpool.elan/docpool/elan/skins/docpool_elan_images/
    icon="rodos_app_icon.png",
    implicit=False,
    # ./src/docpool.theme/docpool/theme/skins/docpooltheme_images/
    logo="rodoslogo.png",
)
