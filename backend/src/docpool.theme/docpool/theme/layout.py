from docpool.base.content.dpdocument import IDPDocument
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
        return body_classes
