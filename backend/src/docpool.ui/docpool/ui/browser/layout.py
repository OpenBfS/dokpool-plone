from plone import api
from plone.app.layout.globals.layout import LayoutPolicy


class DocpoolLayoutPolicy(LayoutPolicy):
    TOOLBAR_BODY_CLASSES = {
        "plone-toolbar-expanded",
        "plone-toolbar-left",
        "plone-toolbar-left-expanded",
    }

    def bodyClass(self, template, view):
        body_class = super().bodyClass(template, view)
        if not body_class:
            return body_class

        if api.user.has_permission("Manage portal", obj=self.context):
            return body_class

        return " ".join(cls for cls in body_class.split() if cls not in self.TOOLBAR_BODY_CLASSES)
