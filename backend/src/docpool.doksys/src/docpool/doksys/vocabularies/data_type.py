from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


@implementer(IVocabularyFactory)
class DataType:
    def __call__(self, context=None):
        values = [
            "ONMON",
            "LADA",
            "EURDEP",
        ]
        return SimpleVocabulary(
            [SimpleTerm(value=value, token=value, title=value) for value in values]
        )


DataTypeFactory = DataType()
