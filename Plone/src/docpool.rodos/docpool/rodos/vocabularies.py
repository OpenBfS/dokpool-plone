from AccessControl.SecurityInfo import allow_module
from docpool.rodos import DocpoolMessageFactory as _
from zope.interface import implements
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary


class VocabItem(object):
    def __init__(self, token, value):
        self.token = token
        self.value = value


class PrognosisTypesVocabulary(object):
    """
    """

    implements(IVocabularyFactory)

    def __call__(self, context):
        items = [
            VocabItem(u'RODOS Prognose', _(u'RODOS Prognose')),
            VocabItem(u'RODOS Diagnose', _(u'RODOS Diagnose')),
            VocabItem(u'DWD Prognose', _(u'DWD Prognose')),
        ]

        return SimpleVocabulary(items)


PrognosisTypesVocabularyFactory = PrognosisTypesVocabulary()


class PrognosisFormsVocabulary(object):
    """
    """

    implements(IVocabularyFactory)

    def __call__(self, context):
        items = [
            VocabItem(u'Einzeldokument', _(u'Einzeldokument')),
            VocabItem(u'RODOS Lauf', _(u'RODOS Lauf')),
        ]

        return SimpleVocabulary(items)


PrognosisFormsVocabularyFactory = PrognosisFormsVocabulary()


class ReleaseSitesVocabulary(object):
    """
    """

    implements(IVocabularyFactory)

    def __call__(self, context):
        items = [
            VocabItem(u'ISAR', _(u'ISAR')),
            VocabItem(u'GUNDREMMINGEN', _(u'GUNDREMMINGEN')),
            VocabItem(u'PHILIPSBURG', _(u'PHILIPPSBURG')),
            VocabItem(u'NECKARWESTHEIM', _(u'NECKARWESTHEIM')),
            VocabItem(u'EMSLAND', _(u'EMSLAND')),
            VocabItem(u'GROHNDE', _(u'GROHNDE')),
            VocabItem(u'BROKDORF', _(u'BROKDORF')),
            VocabItem(u'FR-MUENCHEN', _(u'FR-MUENCHEN')),
            VocabItem(u'FR-BERLIN', _(u'FR-BERLIN')),
            VocabItem(u'LEIBSTADT', _(u'LEIBSTADT')),
            VocabItem(u'GOESGEN', _(u'GOESGEN')),
            VocabItem(u'BEZNAU', _(u'BEZNAU')),
            VocabItem(u'MUEHLEBERG', _(u'MUEHLEBERG')),
            VocabItem(u'CATTENOM', _(u'CATTENOM')),
            VocabItem(u'FESSENHEIM', _(u'FESSENHEIM')),
            VocabItem(u'CHOOZ', _(u'CHOOZ')),
            VocabItem(u'TIHANGE', _(u'TIHANGE')),
            VocabItem(u'TEMELIN', _(u'TEMELIN')),
            VocabItem(u'mobiler Standort', _(u'mobiler Standort')),
        ]

        return SimpleVocabulary(items)


ReleaseSitesVocabularyFactory = ReleaseSitesVocabulary()


allow_module("docpool.rodos.vocabularies")
