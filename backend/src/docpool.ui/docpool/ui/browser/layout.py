from plone import api
from plone.app.layout.globals.layout import LayoutPolicy
from zope.component import getMultiAdapter

import re


CSS_CLASS_SAFE_CHARS = re.compile(r"[^a-z0-9_-]+")


def css_class_suffix(value):
    """Return a lower-case value that is safe to append to a CSS class."""
    return CSS_CLASS_SAFE_CHARS.sub("-", value.lower()).strip("-")


class DocpoolLayoutPolicy(LayoutPolicy):
    TOOLBAR_BODY_CLASSES = {
        "plone-toolbar-expanded",
        "plone-toolbar-left",
        "plone-toolbar-left-expanded",
    }

    def bodyClass(self, template, view):
        body_class = super().bodyClass(template, view)
        body_classes = body_class.split() if body_class else []
        body_classes.extend(self.active_app_classes())
        if not body_classes:
            return body_class

        if api.user.has_permission("Manage portal", obj=self.context):
            return " ".join(body_classes)

        return " ".join(cls for cls in body_classes if cls not in self.TOOLBAR_BODY_CLASSES)

    def active_app_classes(self):
        """Return body classes for the currently active Docpool app"""
        dp_app_state = getMultiAdapter((self.context, self.request), name="dp_app_state")

        body_classes = []
        for app in sorted(dp_app_state.appsActivatedByCurrentUser()):
            app_suffix = css_class_suffix(app)
            if not app_suffix:
                continue
            body_classes.append("active-app-" + app_suffix)

        return body_classes
