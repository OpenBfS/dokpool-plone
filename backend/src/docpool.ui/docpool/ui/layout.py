from docpool.base.content.dpdocument import IDPDocument
from docpool.base.utils import is_admin
from docpool.base.utils import is_contentadmin
from plone import api
from plone.app.layout.globals.interfaces import IBodyClassAdapter
from zope.interface import implementer


@implementer(IBodyClassAdapter)
class DocpoolBodyClasses:
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def get_classes(self, template, view):
        """Custom body classes adapter."""
        body_classes = []
        if IDPDocument.providedBy(self.context):
            state = api.content.get_state(obj=self.context)
            body_classes.append("docstate-" + state)
        if is_admin(self.context) or is_contentadmin(self.context):
            body_classes.append("user-is-admin-or-contentadmin")
        return body_classes
