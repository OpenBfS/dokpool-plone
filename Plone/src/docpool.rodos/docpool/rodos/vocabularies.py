from AccessControl.SecurityInfo import allow_module
from plone.app.vocabularies.terms import safe_simplevocabulary_from_values
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory


@implementer(IVocabularyFactory)
class PrognosisTypesVocabulary:
    """
    """

    def __call__(self, context):
        return safe_simplevocabulary_from_values([
            'RODOS Prognose',
            'RODOS Diagnose',
            'DWD Prognose',
        ])


PrognosisTypesVocabularyFactory = PrognosisTypesVocabulary()


@implementer(IVocabularyFactory)
class PrognosisFormsVocabulary:
    """
    """

    def __call__(self, context):
        return safe_simplevocabulary_from_values([
            'Einzeldokument',
            'RODOS Lauf',
        ])


PrognosisFormsVocabularyFactory = PrognosisFormsVocabulary()


@implementer(IVocabularyFactory)
class ReleaseSitesVocabulary:
    """
    """

    def __call__(self, context):
        return safe_simplevocabulary_from_values([
            'ISAR',
            'GUNDREMMINGEN',
            'PHILIPSBURG',
            'NECKARWESTHEIM',
            'EMSLAND',
            'GROHNDE',
            'BROKDORF',
            'FR-MUENCHEN',
            'FR-BERLIN',
            'LEIBSTADT',
            'GOESGEN',
            'BEZNAU',
            'MUEHLEBERG',
            'CATTENOM',
            'FESSENHEIM',
            'CHOOZ',
            'TIHANGE',
            'TEMELIN',
            'mobiler Standort',
        ])


ReleaseSitesVocabularyFactory = ReleaseSitesVocabulary()


allow_module("docpool.rodos.vocabularies")
