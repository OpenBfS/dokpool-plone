from docpool.doksys import _
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


@implementer(IVocabularyFactory)
class Status:
    """
    """

    def __call__(self, context=None):
        items = [
            ('geprueft', _('geprueft')),
            ('nicht geprueft', _('nicht geprueft')),
        ]
        terms = [SimpleTerm(value, value, title)
                 for value, title in items]
        return SimpleVocabulary(terms)


StatusFactory = Status()
