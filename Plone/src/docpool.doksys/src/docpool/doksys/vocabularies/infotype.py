from docpool.doksys import _
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


@implementer(IVocabularyFactory)
class InfoType:

    def __call__(self, context=None):
        items = [
            ('vorwaerts', _('vorwaerts')),
            ('rueckwaerts', _('rueckwaerts')),
            ('brutto', _('brutto')),
            ('netto', _('netto')),
            ('nass', _('nass')),
            ('trocken', _('trocken')),
            ('Messergebnisse', _('Messergebnisse')),
            ('Ueberblick', _('Ueberblick')),
            ('Soll-Ist-Vergleich', _('Soll-Ist-Vergleich')),
        ]
        terms = [SimpleTerm(value, value, title)
                 for value, title in items]
        return SimpleVocabulary(terms)


InfoTypeFactory = InfoType()
