""" Menu
"""
from plone.app.contentmenu.menu import FactoriesMenu


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
