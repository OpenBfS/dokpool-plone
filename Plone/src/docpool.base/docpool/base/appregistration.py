from docpool.base.appregistry import registerApp
from docpool.base.config import BASE_APP
from docpool.config.local.base import dpAdded, dpRemoved

registerApp(BASE_APP, "Docpool Base", None, None, dpAdded, dpRemoved)
# "None" means: no extension support
