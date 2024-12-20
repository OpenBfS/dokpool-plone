from docpool.rodos import DocpoolMessageFactory as _
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


@implementer(IVocabularyFactory)
class PrognosisTypesVocabulary:
    """ """

    def __call__(self, context):
        values = [
            (None, _("Select a value ...")),
            ("Sonstige Ausbreitungsrechnung", _("Sonstige Ausbreitungsrechnung")),
            ("Potenziell betroffene Gebiete", _("Potenziell betroffene Gebiete")),
            ("RODOS Prognose", _("RODOS Prognose")),
            (
                "DWD Ausbreitungsrechnung ab Quelle",
                _("DWD Ausbreitungsrechnung ab Quelle"),
            ),
            ("LASAIR/LASAT", _("LASAIR/LASAT")),
        ]
        return SimpleVocabulary(
            [SimpleTerm(value, value, title) for value, title in values]
        )


PrognosisTypesVocabularyFactory = PrognosisTypesVocabulary()


@implementer(IVocabularyFactory)
class PrognosisFormsVocabulary:
    """ """

    def __call__(self, context):
        values = [
            ("Routinerechnung", _("Routinerechnung")),
            ("Einzelrechnung", _("Einzelrechnung")),
        ]
        return SimpleVocabulary(
            [SimpleTerm(value, value, title) for value, title in values]
        )


PrognosisFormsVocabularyFactory = PrognosisFormsVocabulary()
