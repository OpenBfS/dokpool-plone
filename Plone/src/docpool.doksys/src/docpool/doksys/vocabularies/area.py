from docpool.doksys import _
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


@implementer(IVocabularyFactory)
class Area:

    def __call__(self, context=None):
        items = [
            ('D', _('D')),
            ('EU', _('EU')),
            ('ME', _('ME')),
            ('World', _('World')),
        ]
        terms = [SimpleTerm(value, value, title)
                 for value, title in items]
        return SimpleVocabulary(terms)


AreaFactory = Area()
