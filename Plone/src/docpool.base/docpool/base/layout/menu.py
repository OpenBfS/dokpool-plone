""" Menu
"""
from plone import api
from plone.app.contentmenu.menu import FactoriesMenu


class DPFactoriesMenu(FactoriesMenu):
    """ Overrides display menu
    """

    def getMenuItems(self, obj, request):
        """ Safely get menu items
        """
        menu_items = super(DPFactoriesMenu, self).getMenuItems(obj, request)

        if not api.user.has_permission(
                'Docpool: Manage Addable Types', obj=obj):
            menu_items = [
                item for item in menu_items
                if not item['action'].endswith((
                    '/folder_factories',
                    '/folder_constraintypes_form',
                ))]

        if hasattr(obj, "customMenu"):
            return obj.customMenu(menu_items)
        else:
            return menu_items
