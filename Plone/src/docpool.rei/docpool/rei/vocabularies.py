# - * - coding: utf - 8 -*-
from AccessControl.SecurityInfo import allow_module
from datetime import date
from plone.app.vocabularies.terms import safe_simplevocabulary_from_values
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


@implementer(IVocabularyFactory)
class AuthorityVocabulary(object):
    """
    """

    def __call__(self, context=None):
        return safe_simplevocabulary_from_values([
            u'Kein Wert',
            u'Baden-Württemberg',
            u'Bayern',
            u'Berlin',
            u'Endlager (Bundesaufsicht)',
            u'Brandenburg',
            u'Bremen',
            u'Hamburg',
            u'Hessen',
            u'Mecklenburg-Vorpommern',
            u'Niedersachsen',
            u'Nordrhein-Westfalen',
            u'Rheinland-Pfalz',
            u'Saarland',
            u'Sachsen',
            u'Sachsen-Anhalt',
            u'Schleswig-Holstein',
            u'Thüringen',
        ])


AuthorityVocabularyFactory = AuthorityVocabulary()


@implementer(IVocabularyFactory)
class ReiLegalBaseVocabulary(object):
    """
    """

    def __call__(self, context=None):
        return safe_simplevocabulary_from_values([
            u'REI-E',
            u'REI-I',
        ])


ReiLegalBaseVocabularyFactory = ReiLegalBaseVocabulary()


@implementer(IVocabularyFactory)
class MediumVocabulary(object):
    """
    """

    def __call__(self, context=None):
        return safe_simplevocabulary_from_values([
            u'Fortluft',
            u'Abwasser',
            u'Abwasser/Fortluft',
        ])


MediumVocabularyFactory = MediumVocabulary()


@implementer(IVocabularyFactory)
class PeriodVocabulary(object):
    """
    """

    def __call__(self, context):
        items = [
            (u'Y', u'Jahr'),
            (u'H1', u'1. Halbjahr'),
            (u'H2', u'2. Halbjahr'),
            (u'Q1', u'1. Quartal'),
            (u'Q2', u'2. Quartal'),
            (u'Q3', u'3. Quartal'),
            (u'Q4', u'4. Quartal'),
            (u'M1', u'Januar'),
            (u'M2', u'Februar'),
            (u'M3', u'März'),
            (u'M4', u'April'),
            (u'M5', u'Mai'),
            (u'M6', u'Juni'),
            (u'M7', u'Juli'),
            (u'M8', u'August'),
            (u'M9', u'September'),
            (u'M10', u'Oktober'),
            (u'M11', u'November'),
            (u'M12', u'Dezember'),
        ]
        terms = [SimpleTerm(code, code, title) for code, title in items]
        return SimpleVocabulary(terms)

PeriodVocabularyFactory = PeriodVocabulary()


@implementer(IVocabularyFactory)
class PDFVersionVocabulary(object):
    """
    """

    def __call__(self, context=None):
        return safe_simplevocabulary_from_values([
            u'PDF/A-1b',
            u'PDF/A-1a',
            u'PDF/A-2a',
            u'PDF/A-2b',
            u'PDF/A-2u',
            u'PDF/A-3a',
            u'PDF/A-3b',
            u'PDF/A-3u',
        ])


PDFVersionVocabularyFactory = PDFVersionVocabulary()


@implementer(IVocabularyFactory)
class MStIDVocabulary(object):
    """
    """

    def __call__(self, context=None):
        items = [
            (u'01002', u'SH-LDZ-Kiel'),
            (u'01010', u'SH-MST2-Geesthacht'),
            (u'01011', u'SH-KTA-Geesthacht'),
            (u'01020', u'SH-MST1-Kiel'),
            (u'01051', u'SH-KTA-Krümmel'),
            (u'01062', u'shldz1'),
            (u'01071', u'SH-KTA-Brunsbüttel'),
            (u'01081', u'SH-KTA-Brokdorf'),
            (u'01181', u'SH-KTA-Brokdorf_SZL'),
            (u'01551', u'SH-KTA-Krümmel_SZL'),
            (u'02002', u'HH-MIN-Hamburg'),
            (u'02010', u'HH-MST1-Hamburg'),
            (u'02020', u'(HH-MST2-Hamburg)'),
            (u'02032', u'HH-LDZ-Hamburg'),
            (u'02041', u'HH-ML-Hamburg'),
            (u'03010', u'NI-MST3-Braunschweig'),
            (u'03040', u'NI-MST1-Hildesheim'),
            (u'03050', u'NI-MST6-Hannover'),
            (u'03060', u'NI-MST2-Hildesheim'),
            (u'03070', u'NI-MST7-Oldenburg'),
            (u'03080', u'NI-MST5-Oldenburg'),
            (u'03090', u'NI-MST4-Cuxhaven'),
            (u'03102', u'NI-LDZ-Hildesheim'),
            (u'03122', u'MStZ'),
            (u'03132', u'NI-MIN-Hannover'),
            (u'03141', u'NI-KTA-Lingen_KKW'),
            (u'03151', u'NI-KTA-Stade'),
            (u'03161', u'NI-KTA-Unterweser'),
            (u'03171', u'NI-KTA-Grohnde'),
            (u'03191', u'NI-KTA-Lippe-Ems'),
            (u'03201', u'NI-KTA-Gorleben'),
            (u'03211', u'NI-KTA-Konrad'),
            (u'03221', u'NI-KTA-Lingen_ANF'),
            (u'03231', u'NI-KTA-Lingen_SZL'),
            (u'03561', u'NI-KTA-Unterweser_SZL'),
            (u'03571', u'NI-KTA-Grohnde_SZL'),
            (u'04002', u'HB-MIN-Bremen'),
            (u'04020', u'HB-MST1-Bremen'),
            (u'04032', u'HB-LDZ-Bremen'),
            (u'05010', u'NW-MST3-Dortmund'),
            (u'05020', u'NW-MST1-Düsseldorf'),
            (u'05030', u'NW-MST2-Düsseldorf'),
            (u'05050', u'NW-ML-Köln'),
            (u'05070', u'NW-MST5-Münster'),
            (u'05080', u'NW-MST6-Münster_LUFA'),
            (u'05090', u'NW-MST7-Dortmund_MPA'),
            (u'05091', u'NW-KTA-Jülich_FZJ'),
            (u'05092', u'NW-KTA-Jülich_AVR'),
            (u'05100', u'NW-MST4-Detmold'),
            (u'05112', u'NW-MIN-Düsseldorf'),
            (u'05122', u'NW-LDZ-Essen'),
            (u'05141', u'NW-KTA-Würgassen'),
            (u'05151', u'NW-KTA-Hamm'),
            (u'05161', u'(NW-KTA-Kalkar)'),
            (u'05171', u'NW-KTA-Ahaus'),
            (u'05181', u'NW-KTA-Gronau'),
            (u'06010', u'HE-MST2-Kassel'),
            (u'06020', u'(HE-MST4-Wiesbaden)'),
            (u'06040', u'(HE-MST6-Gießen)'),
            (u'06050', u'(HE-MST7-Kassel)'),
            (u'06060', u'HE-MST3-Darmstadt'),
            (u'06101', u'HE-KTA-Biblis'),
            (u'06112', u'HE-LDZ-Kassel'),
            (u'06122', u'HE-MIN-Wiesbaden'),
            (u'06501', u'HE-KTA-Biblis_SZL'),
            (u'07002', u'RP-LDZ-Mainz'),
            (u'07010', u'RP-MST1-Mainz'),
            (u'07020', u'RP-MST4-Mainz'),
            (u'07030', u'RP-MST2-Speyer'),
            (u'07040', u'RP-MST5-Speyer'),
            (u'07050', u'(RP-MST3-Trier)'),
            (u'07071', u'(RP-KTA-Mainz)'),
            (u'07081', u'RP-KTA-Mülheim-Kärlich'),
            (u'08002', u'BW-MIN1-Stuttgart'),
            (u'08010', u'BW-MST1-Karlsruhe'),
            (u'08020', u'BW-MST2-Fellbach'),
            (u'08031', u'BW-ML-Stuttgart'),
            (u'08041', u'BW-KTA-Karlsruhe'),
            (u'08050', u'(BW-MST4-Karlsruhe)'),
            (u'08061', u'BW-MST5-Wangen'),
            (u'08070', u'BW-MST3-Freiburg'),
            (u'08082', u'(BW-LDZ-Karlsruhe)'),
            (u'08083', u'BW-MIN2-Stuttgart_REIAB'),
            (u'08101', u'BW-KTA-Obrigheim'),
            (u'08106', u'BW-ML-EggensteinLeopoldshafen_KIT'),
            (u'08111', u'BW-KTA-Neckarwestheim'),
            (u'08121', u'BW-KTA-Philippsburg'),
            (u'08131', u'BW-KTA-Heidelberg'),
            (u'08201', u'BW-MST4-Weingarten'),
            (u'08210', u'LFS BW'),
            (u'08211', u'BW-MM-CBRN'),
            (u'08221', u'BW-ML-EggensteinLeopoldshafen_KHG'),
            (u'08511', u'BW-KTA-Neckarwestheim_SZL'),
            (u'08521', u'BW-KTA-Philippsburg_SZL'),
            (u'09010', u'(BY-MST1-Augsburg)'),
            (u'09011', u'BY-MST7-Kulmbach'),
            (u'09020', u'(BY-MST2-Augsburg)'),
            (u'09030', u'BY-MST3-Augsburg'),
            (u'09040', u'(BY-MST6-Oberschleißheim)'),
            (u'09051', u'BY-ML-Oberschleißheim_01'),
            (u'09052', u'BY-ML-Oberschleißheim_02'),
            (u'09060', u'(BY-MST5-Erlangen)'),
            (u'09070', u'(BY-MST4-München)'),
            (u'09081', u'BY-ML-Nürnberg'),
            (u'09091', u'BY-MST8-Kempten'),
            (u'09111', u'BY-KTA-Garching'),
            (u'09121', u'BY-KTA-Isar'),
            (u'09131', u'BY-KTA-Grafenrheinfeld'),
            (u'09141', u'BY-KTA-Gundremmingen'),
            (u'09151', u'BY-KTA-Kahl'),
            (u'09161', u'BY-KTA-Erlangen_Siemens'),
            (u'09162', u'BY-KTA-Erlangen_Framatome'),
            (u'09171', u'BY-KTA-Karlstein_01'),
            (u'09181', u'BY-KTA-Karlstein_02'),
            (u'09192', u'BY-LDZ-Augsburg'),
            (u'09212', u'BY-MIN1-München'),
            (u'09222', u'BY-MIN2-München'),
            (u'09231', u'BY-ML-München'),
            (u'09301', u'BY-MST-Regensburg'),
            (u'09521', u'BY-KTA-Isar_SZL'),
            (u'09531', u'BY-KTA-Grafenrheinfeld_SZL'),
            (u'09541', u'BY-KTA-Gundremmingen_SZL'),
            (u'10002', u'SL-MIN-Saarbrücken'),
            (u'10010', u'SL-MST1-Saarbrücken'),
            (u'10022', u'10-Min'),
            (u'10030', u'SL-MST2-Saarbrücken'),
            (u'10042', u'SL-LDZ-Saarbrücken'),
            (u'11010', u'BE-MST1-Berlin'),
            (u'11042', u'BE-LDZ-Berlin'),
            (u'11061', u'BE-KTA-Berlin'),
            (u'12002', u'BB-MIN-Potsdam'),
            (u'12010', u'BB-MST1-Oranienburg'),
            (u'12020', u'BB-MST2-FrankfurtOder'),
            (u'12032', u'BB-LDZ-FrankfurtOder'),
            (u'13002', u'MV-MIN-Schwerin'),
            (u'13010', u'MV-MST1-Stralsund'),
            (u'13020', u'(MV-MST2-Schwerin)'),
            (u'13031', u'(MV-KTA-Rubenow)'),
            (u'13032', u'MV-LDZ-Stralsund'),
            (u'13033', u'MV-KTA-Lubmin'),
            (u'14002', u'SN-MIN-Dresden'),
            (u'14010', u'SN-MST1-Radebeul'),
            (u'14020', u'SN-MST2-Chemnitz'),
            (u'14032', u'SN-LDZ-Radebeul'),
            (u'14040', u'SN-ML-Radeberg'),
            (u'14041', u'SN-KTA-Rossendorf'),
            (u'15002', u'ST-MIN-Magdeburg'),
            (u'15010', u'ST-MST1-HalleSaale'),
            (u'15020', u'ST-MST2-Osterburg'),
            (u'15032', u'ST-LDZ-Magdeburg'),
            (u'15041', u'ST-KTA-Morsleben'),
            (u'16002', u'TH-MIN-Erfurt'),
            (u'16010', u'TH-MST1-Jena'),
            (u'16020', u'TH-MST2-Gera'),
            (u'16032', u'TH-LDZ-Jena'),
            (u'17001', u'BUW-München'),
            (u'17002', u'BUW-Kiel'),
            (u'17003', u'BUW-Koblenz'),
            (u'18001', u'EL-KTA-Morsleben'),
            (u'18002', u'EL-KTA-Aufsicht'),
            (u'18003', u'EL-KTA-Asse'),
            (u'19001', u'BfS-MST1-Schulung'),
            (u'19002', u'BfS-MST2-Schulung.extern'),
            (u'20000', u'BfS-ZdB'),
            (u'20001', u'(BfS-ZdB-PARK)'),
            (u'20010', u'DWD'),
            (u'20020', u'BfG'),
            (u'20030', u'BSH'),
            (u'20040', u'LST-TI-Bremerhaven'),
            (u'20050', u'MRI'),
            (u'20060', u'BfS  LSt TW...'),
            (u'20070', u'BFE'),
            (u'20080', u'BfS - Kontaktstelle internat. Datenaustausch'),
            (u'20090', u'BfS - ODL Messnetz-Zentrale'),
            (u'20100', u'PTB'),
            (u'20110', u'BfS  LSt AB'),
            (u'20120', u'BfS-Spur-Freiburg_01'),
            (u'30000', u'Min'),
            (u'30011', u'PTB'),
            (u'30012', u'Min'),
            (u'30021', u'BfS-Berlin'),
            ]
        terms = [SimpleTerm(code, code, u'{} - {}'.format(code, title))
                 for code, title in items]
        return SimpleVocabulary(terms)


MStIDVocabularyFactory = MStIDVocabulary()


@implementer(IVocabularyFactory)
class OriginVocabulary(object):
    """
    """

    def __call__(self, context=None):
        return safe_simplevocabulary_from_values([
            u'Genehmigungsinhaber',
            u'unabhängige Messstelle',
        ])


OriginVocabularyFactory = OriginVocabulary()


@implementer(IVocabularyFactory)
class YearVocabulary(object):
    """
    """

    def __call__(self, context=None):
        items = []
        today = date.today()
        year = today.year
        while year > 1986:
            items.append(
                SimpleVocabulary.createTerm(
                    year, str(year), str(year)))
            year = year - 1

        return SimpleVocabulary(items)


YearVocabularyFactory = YearVocabulary()


@implementer(IVocabularyFactory)
class NuclearInstallationVocabulary(object):
    """
    """

    def __call__(self, context=None):
        return safe_simplevocabulary_from_values([
            u'UCHL KTA Leibstadt mit Beznau und Villigen',
            u'UELA Endlager für radioaktive Abfälle Asse',
            u'UELM Endlager für radioaktive Abfälle Morsleben (ERAM)',
            u'UFRC KKW Cattenom',
            u'UFRF KKW Fessenheim',
            u'U01A Helmholtz-Zentrum Geesthacht',
            u'U01B KKW Krümmel',
            u'U01C KKW Brunsbüttel',
            u'U01D KKW Brokdorf',
            u'U01I Interimslager Krümmel',
            u'U01K Standortzwischenlager Krümmel',
            u'U01L Standortzwischenlager Brunsbüttel',
            u'U01M Standortzwischenlager Brokdorf',
            u'U03A Standortzwischenlager Grohnde',
            u'U03B Brennelementefertigungsanl. Lingen',
            u'U03C Standortzwischenlager Unterweser',
            u'U03E KKW Emsland',
            u'U03G KKW Grohnde',
            u'U03K Endlager Konrad',
            u'U03L KKW Lingen',
            u'U03P BGZ - Betrieb Gorleben',
            u'U03S KKW Stade',
            u'U03U KKW Unterweser',
            u'U03Z Standortzwischenlager Lingen',
            u'U05B BGZ - Brennelement-Zwischenl. Ahaus',
            u'U05F Forschungszentrum Jülich',
            u'U05G AVR-Versuchskernkraftwerk Jülich',
            u'U05K KKW Würgassen',
            u'U05T Thorium-Hochtemp.reakt. Hamm-Uentrop',
            u'U05U Urananreicherungsanlage Gronau',
            u'U06B KKW Biblis und BE-Zwischenlager',
            u'U07M KKW Mülheim-Kärlich',
            u'U07U Uni Mainz',
            u'U08H DKFZ Heidelberg',
            u'U08K Karlsruher Institut für Technologie - Campus Nord (Einrichtungen am Standort)',
            u'U08M Abraumhalde Menz.',
            u'U08N EnKK Neckarwestheim',
            u'U08O EnKK Obrigheim',
            u'U08P EnKK Philippsburg',
            u'U08W KKW Wyhl',
            u'U09A KKW Isar 1+2',
            u'U09B KKW Isar1',
            u'U09C KKW Isar2',
            u'U09D KKW Grafenrheinfeld',
            u'U09E KKW Gundremmingen Block B/C',
            u'U09F Versuchs-AKW Kahl a.M.',
            u'U09G Forschungsreaktor München',
            u'U09H Siemens Brennelementewerk Hanau, Standort Karlstein',
            u'U09I Siemens AG, Karlstein',
            u'U09J Framatome GmbH, Forschungszentrum Erlangen-Süd (FZE)',
            u'U09K Forschungsneutronenquelle Heinz Maier-Leibnitz',
            u'U11B Experimentierreakt. II Berlin',
            u'U12R KKW Rheinsberg',
            u'U13A KKW Lubmin/Greifswald',
            u'U13B Zwischenlager Nord',
            u'U14R Forschungszentrum Rossendorf',
            u'U15M nicht benutzen, jetzt UELM, Endlager für radioaktive Abfälle Morsleben (ERAM)',
        ])


NuclearInstallationVocabularyFactory = NuclearInstallationVocabulary()


allow_module("docpool.rei.vocabularies")
