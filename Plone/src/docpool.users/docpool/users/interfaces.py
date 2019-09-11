# -*- coding: utf-8 -*-
from zope.interface import Interface, Attribute
from docpool.users import DocpoolMessageFactory as _


class IDocPoolUsersLayer(Interface):
    """Request marker installed via browserlayer.xml.
    """
