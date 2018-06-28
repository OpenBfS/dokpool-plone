""" Menu
"""
from zope import interface
from zope.component import queryAdapter
from plone.app.contentmenu.menu import FactoriesMenu
from Products.statusmessages.interfaces import IStatusMessage
from Products.Five.browser import BrowserView

class DPFactoriesMenu(FactoriesMenu):
    """ Overrides display menu
    """
    def getMenuItems(self, obj, request):
        """ Safely get menu items
        """
        menu_items = super(DPFactoriesMenu, self).getMenuItems(obj, request)
        if hasattr(obj, "customMenu"):
            return obj.customMenu(menu_items)
        else:
            return menu_items

