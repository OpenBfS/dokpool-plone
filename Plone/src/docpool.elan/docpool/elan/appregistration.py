from docpool.base.appregistry import registerApp
from docpool.config.local.elan import dpAdded
from docpool.config.local.elan import dpRemoved
from docpool.elan.behaviors.elandoctype import IELANDocType
from docpool.elan.behaviors.elandocument import IELANDocument
from docpool.elan.config import ELAN_APP


registerApp(
    ELAN_APP,
    "ELAN",
    IELANDocType,
    IELANDocument,
    dpAdded,
    dpRemoved,
    # Todo Skins folder
    # /src/docpool.elan/docpool/elan/skins/docpool_elan_images/elan_app_icon.png
    icon="elan_app_icon.png",
    # ./src/docpool.theme/docpool/theme/skins/docpooltheme_images/elanlogo.png
    logo="elanlogo.png",
)
