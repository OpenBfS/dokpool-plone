from docpool.base.appregistry import appName
from docpool.base.config import BASE_APP
from docpool.base.content.archiving import IArchiving
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

        self.navtree_add_apps_menu(tree)

        if not IArchiving(self.context).is_archive:
            self.navtree_add_contentarea(tree)

        # for tab in tree[self.navtree_path]:
        #     if "config" in tab["id"]:
        #         tab["item_class"] = "config"

        return tree

    def navtree_add_apps_menu(self, tree):
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
            dp_path = f"{self.navtree_path}/apps/{dp_id}"
            tree[apps_path].append(
                dict(
                    id=dp_id,
                    path=dp_path,
                    uid=dp_id,
                    title=f"{dp.title}",
                    url=here,
                    review_state="visible",
                    # item_class=app_title,
                )
            )
            for app_name in app_names:
                app_title = (
                    utranslate("docpool.menu", "Docpool Base", context=self.context)
                    if app_name == BASE_APP
                    else appName(app_name)
                )
                app_id = f"{dp_id}-{app_name}"
                tree[dp_path].append(
                    dict(
                        id=app_id,
                        path=f"{dp_path}/{app_name}",
                        uid=app_id,
                        title=f"{app_title}",
                        url=f"{here}/setActiveApp?app={app_name}",
                        review_state="visible",
                        # item_class=app_title,
                    )
                )

    def navtree_add_contentarea(self, tree):
        folders = getFoldersForCurrentUser(self.context)
        if not folders:
            return

        content_path = f"{self.navtree_path}/content"
        tree[self.navtree_path].append(
            dict(
                id="content",
                path=content_path,
                uid="content",
                url="",
                title=utranslate("docpool.base", "Content Area", context=self.context),
                review_state="visible",
            )
        )

        tree[content_path] = []
        for folder in folders:
            self.recurse_folder(folder, content_path, tree)

    def recurse_folder(self, folder, parent_path, tree):
        path = folder["path"]
        tree[parent_path].append(
            dict(
                id=folder["id"],
                path=path,
                uid=folder["UID"],
                url=folder["getURL"],
                title=folder["Title"],
                review_state=folder["review_state"],
            )
        )
        tree[path] = []
        for child in folder.get("children", ()):
            self.recurse_folder(child, path, tree)
