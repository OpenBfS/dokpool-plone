from AccessControl.SecurityInfo import allow_module
from plone.app.vocabularies.terms import safe_simplevocabulary_from_values
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory


@implementer(IVocabularyFactory)
class PrognosisTypesVocabulary:
    """ """

    def __call__(self, context):
        return safe_simplevocabulary_from_values(
            [
                "Potenziell betroffene Gebiete",
                "RODOS Prognose",
                "DWD Ausbreitungsrechnung ab Quelle",
                "LASAIR/LASAT",
                "Sonstige Ausbreitungsrechnung",
            ]
        )


PrognosisTypesVocabularyFactory = PrognosisTypesVocabulary()


@implementer(IVocabularyFactory)
class PrognosisFormsVocabulary:
    """ """

    def __call__(self, context):
        return safe_simplevocabulary_from_values(
            [
                "Routinerechnung",
                "Einzelrechnung",
            ]
        )


PrognosisFormsVocabularyFactory = PrognosisFormsVocabulary()
