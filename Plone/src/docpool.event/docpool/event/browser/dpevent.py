from plone.dexterity.browser.view import DefaultView

import json


class DPEventView(DefaultView):
    """View for Events
    """

    def changelog(self):
        """Changelog as a list of dicts
        """
        changelog = json.loads(self.context.changelog or '[]')
        changelog = self.harmonize_dicts(changelog)
        return changelog

    def harmonize_dicts(self, data):
        """Unify a list of dicts.
        Add missing keys with empty values to be able to export a nice csv.
        """
        all_keys = set()
        all_items = []
        for item in data:
            all_keys.update(item.keys())
        for item in data:
            for key in all_keys.difference(item.keys()):
                item[key] = None
            all_items.append(item)
        return all_items
