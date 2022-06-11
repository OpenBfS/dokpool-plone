from docpool.doksys import _
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary


@implementer(IVocabularyFactory)
class Purpose:
    def __call__(self, context=None):
        items = [
            ("Standard-Info Bundesmessnetze", _("Standard-Info Bundesmessnetze")),
            ("Standard-Info DWD", _("Standard-Info DWD")),
        ]

        terms = [SimpleTerm(value, value, title) for value, title in items]
        return SimpleVocabulary(terms)


PurposeFactory = Purpose()
