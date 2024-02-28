from AccessControl import ModuleSecurityInfo
from docpool.base import DocpoolMessageFactory as _
from plone.app.workflow.interfaces import ISharingPageRole
from Products.CMFCore.permissions import setDefaultRoles
from zope.interface import implementer


security = ModuleSecurityInfo("plone.app.workflow.permissions")


security.declarePublic("DelegateSiteAdminRole")
DelegateSiteAdminRole = "Sharing page: Delegate Site Administrator role"
setDefaultRoles(DelegateSiteAdminRole, ("Manager", "Site Administrator"))


@implementer(ISharingPageRole)
class SiteAdminRole:
    title = _("title_can_manage_site", default="Can manage site")
    required_permission = DelegateSiteAdminRole
    required_interface = None
