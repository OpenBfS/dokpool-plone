from docpool.doksys import _
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary


@implementer(IVocabularyFactory)
class NetworkOperators:
    def __call__(self, context=None):
        items = [
            ("Schleswig-Holstein", _("Schleswig-Holstein")),
            ("Hamburg", _("Hamburg")),
            ("Niedersachsen", _("Niedersachsen")),
            ("Bremen", _("Bremen")),
            ("Nordrhein-Westfalen", _("Nordrhein-Westfalen")),
            ("Hessen", _("Hessen")),
            ("Rheinland-Pfalz", _("Rheinland-Pfalz")),
            ("Baden-Wuerttemberg", _("Baden-Wuerttemberg")),
            ("Bayern", _("Bayern")),
            ("Saarland", _("Saarland")),
            ("Berlin", _("Berlin")),
            ("Brandenburg", _("Brandenburg")),
            ("Mecklenburg-Vorpommern", _("Mecklenburg-Vorpommern")),
            ("Sachsen", _("Sachsen")),
            ("Sachsen-Anhalt", _("Sachsen-Anhalt")),
            ("Thueringen", _("Thueringen")),
            ("Bundeswehr", _("Bundeswehr")),
            ("Endlager (Bundesaufsicht)", _("Endlager (Bundesaufsicht)")),
            ("ZdB-Testnetz", _("ZdB-Testnetz")),
            ("BfS (Spuren)", _("BfS (Spuren)")),
            ("vTI", _("vTI")),
            ("BfS/ZdB", _("BfS/ZdB")),
            ("BfE", _("BfE")),
            ("FhG", _("FhG")),
            ("BfG", _("BfG")),
            ("BSH", _("BSH")),
            ("BfS (LSt. AB)", _("BfS (LSt. AB)")),
            ("BfS (LSt. TW ...)", _("BfS (LSt. TW ...)")),
            ("BMU", _("BMU")),
            ("MRI", _("MRI")),
            ("Park", _("Park")),
            ("Sonstige", _("Sonstige")),
            ("PTB", _("PTB")),
            ("BfS (ABI)", _("BfS (ABI)")),
            ("DWD", _("DWD")),
            ("auslaend. Messnetze", _("auslaend. Messnetze")),
            ("BfS (ODL)", _("BfS (ODL)")),
        ]
        terms = [SimpleTerm(value, value, title) for value, title in items]
        return SimpleVocabulary(terms)


NetworkOperatorsFactory = NetworkOperators()
