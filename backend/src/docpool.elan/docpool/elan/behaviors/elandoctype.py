from docpool.base.interfaces import IDocTypeExtension
from plone.autoform.interfaces import IFormFieldProvider
from zope.interface import provider


@provider(IFormFieldProvider)
class IELANDocType(IDocTypeExtension):
    pass


class ELANDocType:
    def __init__(self, context):
        self.context = context

    def categories(self):
        return []
