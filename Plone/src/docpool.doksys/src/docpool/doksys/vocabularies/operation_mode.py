from docpool.doksys import _
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary


@implementer(IVocabularyFactory)
class OperationMode:
    """ """

    def __call__(self, context=None):
        # Just an example list of content for our vocabulary,
        # this can be any static or dynamic data, a catalog result for example.
        items = [
            ("Routine", _("Routine")),
            ("Intensiv", _("Intensiv")),
        ]
        terms = [SimpleTerm(value, value, title) for value, title in items]
        return SimpleVocabulary(terms)


OperationModeFactory = OperationMode()
