from docpool.doksys import _
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


@implementer(IVocabularyFactory)
class Duration:

    def __call__(self, context=None):
        items = [
            ('1a', _('1a')),
            ('1Mo', _('1Mo')),
            ('1d', _('1d')),
            ('2h', _('2h')),
            ('1h', _('1h')),
            ('10Min', _('10Min')),
        ]
        terms = [SimpleTerm(value, value, title)
                 for value, title in items]
        return SimpleVocabulary(terms)


DurationFactory = Duration()
