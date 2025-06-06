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
    "IMIS Doksys",
    None,
    IDoksysDoc,
    dpAdded,
    dpRemoved,
    icon="++plone++docpool.doksys/doksys_app_icon.png",
    implicit=False,
    logo="++plone++docpool/doksyslogo.png",
)
