from docpool.menu.utils import (
    getApplicationDocPoolsForCurrentUser,
    getFoldersForCurrentUser,
)
from plone.app.layout.viewlets import common
from Products.CMFPlone.i18nl10n import utranslate


class GlobalSectionsViewlet(common.GlobalSectionsViewlet):
    def _portal_tabs(self):
        tabs = self._content_tabs()

        for tab in tabs:
            if tab["id"].find("config") != -1:
                tab["item_class"] = "config"
            elif tab["id"] == "content":
                tab["item_class"] = "hide"

        apds = getApplicationDocPoolsForCurrentUser(self.context)
        if apds:
            apds.extend(tabs)
            tabs = apds

        if not self.context.restrictedTraverse("@@context_helpers").is_archive():
            ffu = getFoldersForCurrentUser(self.context)
            if ffu:
                for f in ffu:
                    if "item_class" not in f:
                        f["item_class"] = "personal"
                tabs.append(
                    {
                        "id": "content",
                        "Title": utranslate(
                            "docpool.base", "Content Area", context=self.context
                        ),
                        "Description": "",
                        "getURL": "",
                        "show_children": True,
                        "children": ffu,
                        "currentItem": False,
                        "item_class": "contentarea",
                        "currentParent": self.context.isPersonal(),
                        "normalized_review_state": "visible",
                    }
                )
        return tabs
