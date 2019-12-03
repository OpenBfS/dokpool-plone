from AccessControl.SecurityInfo import allow_module
from plone.app.vocabularies.terms import safe_simplevocabulary_from_values
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory


@implementer(IVocabularyFactory)
class PrognosisTypesVocabulary(object):
    """
    """

    def __call__(self, context):
        return safe_simplevocabulary_from_values([
            u'RODOS Prognose',
            u'RODOS Diagnose',
            u'DWD Prognose',
        ])


PrognosisTypesVocabularyFactory = PrognosisTypesVocabulary()


@implementer(IVocabularyFactory)
class PrognosisFormsVocabulary(object):
    """
    """

    def __call__(self, context):
        return safe_simplevocabulary_from_values([
            u'Einzeldokument',
            u'RODOS Lauf',
        ])


PrognosisFormsVocabularyFactory = PrognosisFormsVocabulary()


@implementer(IVocabularyFactory)
class ReleaseSitesVocabulary(object):
    """
    """

    def __call__(self, context):
        return safe_simplevocabulary_from_values([
            u'ISAR',
            u'GUNDREMMINGEN',
            u'PHILIPSBURG',
            u'NECKARWESTHEIM',
            u'EMSLAND',
            u'GROHNDE',
            u'BROKDORF',
            u'FR-MUENCHEN',
            u'FR-BERLIN',
            u'LEIBSTADT',
            u'GOESGEN',
            u'BEZNAU',
            u'MUEHLEBERG',
            u'CATTENOM',
            u'FESSENHEIM',
            u'CHOOZ',
            u'TIHANGE',
            u'TEMELIN',
            u'mobiler Standort',
        ])


ReleaseSitesVocabularyFactory = ReleaseSitesVocabulary()


allow_module("docpool.rodos.vocabularies")
