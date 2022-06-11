from docpool.doksys import _
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


@implementer(IVocabularyFactory)
class MeasuringProgram:

    def __call__(self, context=None):
        items = [
            ('Intensivmessprogramm', _('Intensivmessprogramm')),
            ('Routinemessprogramm', _('Routinemessprogramm')),
            ('REI', _('REI')),
            ('Spontanproben Bund', _('Spontanproben Bund')),
        ]
        terms = [SimpleTerm(value, value, title)
                 for value, title in items]
        return SimpleVocabulary(terms)


MeasuringProgramFactory = MeasuringProgram()
