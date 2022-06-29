from docpool.base.appregistry import appName
from docpool.base.config import BASE_APP
from docpool.menu.utils import (
    getApplicationDocPoolsForCurrentUser,
    getFoldersForCurrentUser,
)
from plone import api
from plone.app.layout.viewlets import common
from plone.memoize.view import memoize
from Products.CMFPlone.i18nl10n import utranslate


class GlobalSectionsViewlet(common.GlobalSectionsViewlet):
    @property
    @memoize
    def navtree(self):
        tree = super().navtree

        if api.user.is_anonymous():
            return tree

        current_dp, current_app, dp_apps = getApplicationDocPoolsForCurrentUser(
            self.context
        )
        app_title = appName(current_app) if current_app else None

        if current_dp:
            root_title = f"{current_dp.title}: {app_title}"
        else:
            root_title = utranslate("docpool.menu", "Docpools", context=self.context)

        tree[self.navtree_path].insert(
            0,
            dict(
                id="apps",
                path=f"{self.navtree_path}/apps",
                uid="apps",
                url="",
                title=root_title,
                review_state="visible",
                # item_class="applications",
            ),
        )

        apps_path = f"{self.navtree_path}/apps"
        current_dp_id = current_dp.getId() if current_dp else None

        for dp, app_names in dp_apps:
            dp_id = dp.getId()
            here = (self.context if current_dp_id == dp_id else dp).absolute_url()
            for app_name in app_names:
                app_title = (
                    utranslate("docpool.menu", "Docpool Base", context=self.context)
                    if app_name == BASE_APP
                    else appName(app_name)
                )
                app_id = f"{dp_id}-{app_name}"
                tree[apps_path].append(
                    dict(
                        id=app_id,
                        path=f"{self.navtree_path}/apps/{app_id}",
                        uid=app_id,
                        title=f"{dp.title}: {app_title}",
                        url=f"{here}/setActiveApp?app={app_name}",
                        review_state="visible",
                        # item_class=app_title,
                    )
                )

        return tree

    def _portal_tabs(self):
        tabs = self._content_tabs()

        for tab in tabs:
            if tab["id"].find("config") != -1:
                tab["item_class"] = "config"
            elif tab["id"] == "content":
                tab["item_class"] = "hide"

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
