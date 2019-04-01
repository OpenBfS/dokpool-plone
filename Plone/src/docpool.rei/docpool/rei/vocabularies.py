#- * - coding: utf - 8 -*-
from zope.interface import implements
from zope.schema.interfaces import IVocabularyFactory, IBaseVocabulary
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import SimpleTerm
from zope.site.hooks import getSite
from Products.CMFCore.utils import getToolByName
from docpool.rei import DocpoolMessageFactory as _
from AccessControl.SecurityInfo import allow_module, allow_class
from Products.Archetypes.utils import shasattr
from zope.component import getMultiAdapter
from datetime import date

class VocabItem(object):
    def __init__(self, token, value):
        self.token = token
        self.value = value


class FederalStateVocabulary(object):
    """
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        items = [
            VocabItem(u'Schleswig-Holstein', _(u'Schleswig-Holstein')),
            VocabItem(u'Hamburg', _(u'Hamburg')),
            VocabItem(u'Niedersachsen', _(u'Niedersachsen')),
            VocabItem(u'Bremen', _(u'Bremen')),
            VocabItem(u'Nordrhein-Westfalen', _(u'Nordrhein-Westfahlen')),
            VocabItem(u'Hessen', _(u'Hessen')),
            VocabItem(u'Rheinland-Pfalz', _(u'Rheinland-Pfalz')),
            VocabItem(u'Baden-Württemberg', _(u'Baden-Württemberg')),
            VocabItem(u'Bayern', _(u'Bayern')),
            VocabItem(u'Saarland', _(u'Saarland')),
            VocabItem(u'Berlin', _(u'Berlin')),
            VocabItem(u'Brandenburg', _(u'Brandenburg')),
            VocabItem(u'Mecklenburg-Vorpommern', _(u'Mecklenburg-Vorpommern')),
            VocabItem(u'Sachsen', _(u'Sachsen')),
            VocabItem(u'Sachsen-Anhalt', _(u'Sachsen-Anhalt')),
            VocabItem(u'Thüringen', _(u'Thüringen')),
        ]

        return SimpleVocabulary(items)

FederalStateVocabularyFactory = FederalStateVocabulary()

class OperatorVocabulary(object):
    """
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        items = [
            VocabItem(u'Schleswig-Holstein', _(u'Schleswig-Holstein')),
            VocabItem(u'Hamburg', _(u'Hamburg')),
            VocabItem(u'Niedersachsen', _(u'Niedersachsen')),
            VocabItem(u'Bremen', _(u'Bremen')),
            VocabItem(u'Nordrhein-Westfalen', _(u'Nordrhein-Westfahlen')),
            VocabItem(u'Hessen', _(u'Hessen')),
            VocabItem(u'Rheinland-Pfalz', _(u'Rheinland-Pfalz')),
            VocabItem(u'Baden-Württemberg', _(u'Baden-Württemberg')),
            VocabItem(u'Bayern', _(u'Bayern')),
            VocabItem(u'Saarland', _(u'Saarland')),
            VocabItem(u'Berlin', _(u'Berlin')),
            VocabItem(u'Brandenburg', _(u'Brandenburg')),
            VocabItem(u'Mecklenburg-Vorpommern', _(u'Mecklenburg-Vorpommern')),
            VocabItem(u'Sachsen', _(u'Sachsen')),
            VocabItem(u'Sachsen-Anhalt', _(u'Sachsen-Anhalt')),
            VocabItem(u'Thüringen', _(u'Thüringen')),
        ]

        return SimpleVocabulary(items)

OperatorVocabularyFactory = OperatorVocabulary()

class ReiLegalBaseVocabulary(object):
    """
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        items = [
            VocabItem(u'REI-E', _(u'REI-E')),
            VocabItem(u'REI-I', _(u'REI-I')),
            VocabItem(u'REI-E/REI-I', _(u'REI-E/REI-I')),
        ]

        return SimpleVocabulary(items)

ReiLegalBaseVocabularyFactory = ReiLegalBaseVocabulary()

class MediaVocabulary(object):
    """
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        items = [
            VocabItem(u'Fortluft', _(u'Fortluft')),
            VocabItem(u'Abwasser', _(u'Abwasser')),
            VocabItem(u'Fortluft/Abwasser', _(u'Fortluft/Abwasser')),
                    ]

        return SimpleVocabulary(items)

MediaVocabularyFactory = MediaVocabulary()

class PeriodVocabulary(object):
    """
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        items = [
            VocabItem(u'1. Quartal', _(u'1. Quartal')),
            VocabItem(u'2. Quartal', _(u'2. Quartal')),
            VocabItem(u'3. Quartal', _(u'3. Quartal')),
            VocabItem(u'4. Quartal', _(u'4. Quartal')),
            VocabItem(u'Jahr', _(u'Jahrl')),
        ]

        return SimpleVocabulary(items)

PeriodVocabularyFactory = PeriodVocabulary()

class PdfVersionVocabulary(object):
    """
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        items = [
            VocabItem(u'PDF/A-1b', _(u'PDF/A-1b')),

        ]

        return SimpleVocabulary(items)

PdfVersionVocabularyFactory = PdfVersionVocabulary()

class YearVocabulary(object):
    """
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        items = []
        today = date.today()
        year = today.year
        while year > 1999:
            items.append(SimpleVocabulary.createTerm(year, str(year)))
            year = year - 1
        # items = [
        #      VocabItem(u'2013', _(u'2013')),
        #      VocabItem(u'2014', _(u'2014')),
        #      VocabItem(u'2015', _(u'2015')),
        #      VocabItem(u'2016', _(u'2016')),
        #      VocabItem(u'2017', _(u'2017')),
        #      VocabItem(u'2018', _(u'2018')),
        #      VocabItem(u'2019', _(u'2019')),
        #      VocabItem(u'2020', _(u'2020')),
        #]

        return SimpleVocabulary(items)

YearVocabularyFactory = YearVocabulary()

class NuclearInstallationVocabulary(object):
    """
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        items = [
            VocabItem(u'UCHL KTA Leibstadt mit Beznau und Villigen ',
                      _(u'UCHL KTA Leibstadt mit Beznau und Villigen ')),
            VocabItem(u'UELA Endlager für radioaktive Abfälle Asse ',
                      _(u'UELA Endlager für radioaktive Abfälle Asse ')),
            VocabItem(u'UELM Endlager für radioaktive Abfälle Morsleben (ERAM) ',
                      _(u'UELM Endlager für radioaktive Abfälle Morsleben (ERAM) ')),
            VocabItem(u'UFRC KKW Cattenom ', _(u'UFRC KKW Cattenom ')),
            VocabItem(u'UFRF KKW Fessenheim ', _(u'UFRF KKW Fessenheim ')),
            VocabItem(u'U01A Helmholtz-Zentrum Geesthacht ', _(u'U01A Helmholtz-Zentrum Geesthacht ')),
            VocabItem(u'U01B KKW Krümmel ', _(u'U01B KKW Krümmel ')),
            VocabItem(u'U01C KKW Brunsbüttel ', _(u'U01C KKW Brunsbüttel ')),
            VocabItem(u'U01D KKW Brokdorf ', _(u'U01D KKW Brokdorf ')),
            VocabItem(u'U01I Interimslager Krümmel ', _(u'U01I Interimslager Krümmel ')),
            VocabItem(u'U01K Standortzwischenlager Krümmel ', _(u'U01K Standortzwischenlager Krümmel ')),
            VocabItem(u'U01L Standortzwischenlager Brunsbüttel ', _(u'U01L Standortzwischenlager Brunsbüttel ')),
            VocabItem(u'U01M Standortzwischenlager Brokdorf ', _(u'U01M Standortzwischenlager Brokdorf ')),
            VocabItem(u'U03A Standortzwischenlager Grohnde ', _(u'U03A Standortzwischenlager Grohnde ')),
            VocabItem(u'U03B Brennelementefertigungsanl. Lingen ', _(u'U03B Brennelementefertigungsanl. Lingen ')),
            VocabItem(u'U03C Standortzwischenlager Unterweser ', _(u'U03C Standortzwischenlager Unterweser ')),
            VocabItem(u'U03E KKW Emsland ', _(u'U03E KKW Emsland ')),
            VocabItem(u'U03G KKW Grohnde ', _(u'U03G KKW Grohnde ')),
            VocabItem(u'U03K Endlager Konrad ', _(u'U03K Endlager Konrad ')),
            VocabItem(u'U03L KKW Lingen ', _(u'U03L KKW Lingen ')),
            VocabItem(u'U03P BGZ - Betrieb Gorleben ', _(u'U03P BGZ - Betrieb Gorleben ')),
            VocabItem(u'U03S KKW Stade ', _(u'U03S KKW Stade ')),
            VocabItem(u'U03U KKW Unterweser ', _(u'U03U KKW Unterweser ')),
            VocabItem(u'U03Z Standortzwischenlager Lingen ', _(u'U03Z Standortzwischenlager Lingen ')),
            VocabItem(u'U05B BGZ - Brennelement-Zwischenl. Ahaus ', _(u'U05B BGZ - Brennelement-Zwischenl. Ahaus ')),
            VocabItem(u'U05F Forschungszentrum Jülich ', _(u'U05F Forschungszentrum Jülich ')),
            VocabItem(u'U05G AVR-Versuchskernkraftwerk Jülich ', _(u'U05G AVR-Versuchskernkraftwerk Jülich ')),
            VocabItem(u'U05K KKW Würgassen ', _(u'U05K KKW Würgassen ')),
            VocabItem(u'U05T Thorium-Hochtemp.reakt. Hamm-Uentrop ', _(u'U05T Thorium-Hochtemp.reakt. Hamm-Uentrop ')),
            VocabItem(u'U05U Urananreicherungsanlage Gronau ', _(u'U05U Urananreicherungsanlage Gronau ')),
            VocabItem(u'U06B KKW Biblis und BE-Zwischenlager ', _(u'U06B KKW Biblis und BE-Zwischenlager ')),
            VocabItem(u'U07M KKW Mülheim-Kärlich ', _(u'U07M KKW Mülheim-Kärlich ')),
            VocabItem(u'U07U Uni Mainz ', _(u'U07U Uni Mainz ')),
            VocabItem(u'U08H DKFZ Heidelberg ', _(u'U08H DKFZ Heidelberg ')),
            VocabItem(u'U08K Karlsruher Institut für Technologie - Campus Nord (Einrichtungen am Standort) ',
                      _(u'U08K Karlsruher Institut für Technologie - Campus Nord (Einrichtungen am Standort) ')),
            VocabItem(u'U08M Abraumhalde Menz. ', _(u'U08M Abraumhalde Menz. ')),
            VocabItem(u'U08N EnKK Neckarwestheim ', _(u'U08N EnKK Neckarwestheim ')),
            VocabItem(u'U08O EnKK Obrigheim ', _(u'U08O EnKK Obrigheim ')),
            VocabItem(u'U08P EnKK Philippsburg ', _(u'U08P EnKK Philippsburg ')),
            VocabItem(u'U08W KKW Wyhl ', _(u'U08W KKW Wyhl ')),
            VocabItem(u'U09A KKW Isar 1+2 ', _(u'U09A KKW Isar 1+2 ')),
            VocabItem(u'U09B KKW Isar1 ', _(u'U09B KKW Isar1 ')),
            VocabItem(u'U09C KKW Isar2 ', _(u'U09C KKW Isar2 ')),
            VocabItem(u'U09D KKW Grafenrheinfeld ', _(u'U09D KKW Grafenrheinfeld ')),
            VocabItem(u'U09E KKW Gundremmingen Block B/C ', _(u'U09E KKW Gundremmingen Block B/C ')),
            VocabItem(u'U09F Versuchs-AKW Kahl a.M. ', _(u'U09F Versuchs-AKW Kahl a.M. ')),
            VocabItem(u'U09G Forschungsreaktor München ', _(u'U09G Forschungsreaktor München ')),
            VocabItem(u'U09H Siemens Brennelementewerk Hanau, Standort Karlstein ',
                      _(u'U09H Siemens Brennelementewerk Hanau, Standort Karlstein ')),
            VocabItem(u'U09I Siemens AG, Karlstein ', _(u'U09I Siemens AG, Karlstein ')),
            VocabItem(u'U09J Framatome GmbH, Forschungszentrum Erlangen-Süd (FZE) ',
                      _(u'U09J Framatome GmbH, Forschungszentrum Erlangen-Süd (FZE) ')),
            VocabItem(u'U09K Forschungsneutronenquelle Heinz Maier-Leibnitz ',
                      _(u'U09K Forschungsneutronenquelle Heinz Maier-Leibnitz ')),
            VocabItem(u'U11B Experimentierreakt. II Berlin ', _(u'U11B Experimentierreakt. II Berlin ')),
            VocabItem(u'U12R KKW Rheinsberg ', _(u'U12R KKW Rheinsberg ')),
            VocabItem(u'U13A KKW Lubmin/Greifswald ', _(u'U13A KKW Lubmin/Greifswald ')),
            VocabItem(u'U13B Zwischenlager Nord ', _(u'U13B Zwischenlager Nord ')),
            VocabItem(u'U14R Forschungszentrum Rossendorf ', _(u'U14R Forschungszentrum Rossendorf ')),
            VocabItem(u'U15M nicht benutzen, jetzt UELM, Endlager für radioaktive Abfälle Morsleben (ERAM) ', _(u'U15M nicht benutzen, jetzt UELM, Endlager für radioaktive Abfälle Morsleben (ERAM) ')),

        ]

        return SimpleVocabulary(items)

NuclearInstallationVocabularyFactory = NuclearInstallationVocabulary()



allow_module("docpool.rei.vocabularies")
