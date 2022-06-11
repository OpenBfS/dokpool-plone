""" Menu
"""
from plone import api
from plone.app.contentmenu.menu import FactoriesMenu
from plone.app.contentmenu.menu import WorkflowMenu

class DPFactoriesMenu(FactoriesMenu):
    """ Overrides display menu
    """

    def getMenuItems(self, obj, request):
        """ Safely get menu items
        """
        menu_items = super().getMenuItems(obj, request)

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

class DPWorkflowMenu(WorkflowMenu):
    """ Overrides display menu
    """

    def getMenuItems(self, context, request):

        results = super().getMenuItems(context, request)
        if len(results) > 0:

            # Remove status history menu item ('Advanced...')

            results = [r for r in results
                if not r['action'].endswith(('/content_status_history','/placeful_workflow_configuration'))]

        return results
