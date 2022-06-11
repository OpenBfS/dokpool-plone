"""Common configuration constants
"""
from AccessControl import ClassSecurityInfo
from Acquisition import aq_inner
from docpool.base import DocpoolMessageFactory as _
from docpool.base.browser.flexible_view import FlexibleView
from docpool.base.interfaces import IDocumentExtension
from docpool.example import DocpoolMessageFactory as _
from docpool.example.config import EXAMPLE_APP
from plone.autoform.directives import read_permission, write_permission
from plone.autoform.interfaces import IFormFieldProvider
from zope import schema
from zope.interface import provider


@provider(IFormFieldProvider)
class IExampleDoc(IDocumentExtension):
    example_attribute = schema.TextLine(
        title=_("label_example_attribute", default="Example Attribute"),
        description=_("description_example_attribute", default=""),
        required=False,
    )
    read_permission(example_attribute="docpool.example.AccessExample")
    write_permission(example_attribute="docpool.example.AccessExample")


class ExampleDoc(FlexibleView):
    __allow_access_to_unprotected_subobjects__ = 1

    security = ClassSecurityInfo()

    appname = EXAMPLE_APP

    def __init__(self, context):
        self.context = context
        self.request = context.REQUEST

    def _get_example_attribute(self):
        return self.context.example_attribute

    def _set_example_attribute(self, value):
        if not value:
            return
        context = aq_inner(self.context)
        context.example_attribute = value

    example_attribute = property(_get_example_attribute, _set_example_attribute)

    def isClean(self):
        """
        Is this document free for further action like publishing or transfer?
        @return:
        """
        # TODO: define if necessary. Method MUST be present in Doc behavior.
        return True
