from docpool.users import DocpoolMessageFactory as _
from zope.interface import Attribute, Interface


class IDocPoolUsersLayer(Interface):
    """Request marker installed via browserlayer.xml."""
