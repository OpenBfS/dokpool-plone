from docpool.doksys import _
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


@implementer(IVocabularyFactory)
class LegalBase:

    def __call__(self, context=None):
        items = [
            ('AVV IMIS', _('AVV IMIS')),
            ('EURDEP', _('EURDEP')),
            ('IRMIS', _('IRMIS')),
            ('DENSE', _('DENSE')),
            ('KFÜ', _('KFÜ')),
            ('Land', _('Land')),
            ('SPARSE', _('SPARSE')),
            ('REI-E', _('REI-E')),
            ('REI-I', _('REI-I')),
        ]
        terms = [SimpleTerm(value, value, title)
                 for value, title in items]
        return SimpleVocabulary(terms)


LegalBaseFactory = LegalBase()
