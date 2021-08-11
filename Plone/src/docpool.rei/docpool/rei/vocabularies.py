# - * - coding: utf - 8 -*-
from AccessControl.SecurityInfo import allow_module
from collections import OrderedDict
from datetime import date
from docpool.base.utils import simplevoc_from_dict
from plone.app.vocabularies.terms import safe_simplevocabulary_from_values
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary

AUTHORITIES = OrderedDict([
    (u'', u'Select a value ...'),
    (u'de_bw', u'Baden-Württemberg'),
    (u'de_by', u'Bayern'),
    (u'de_be', u'Berlin'),
    (u'de_bb', u'Brandenburg'),
    (u'de_hb', u'Bremen'),
    (u'de_el', u'Endlager (Bundesaufsicht)'),
    (u'de_hh', u'Hamburg'),
    (u'de_he', u'Hessen'),
    (u'de_mv', u'Mecklenburg-Vorpommern'),
    (u'de_ni', u'Niedersachsen'),
    (u'de_nw', u'Nordrhein-Westfalen'),
    (u'de_rp', u'Rheinland-Pfalz'),
    (u'de_sl', u'Saarland'),
    (u'de_sn', u'Sachsen'),
    (u'de_st', u'Sachsen-Anhalt'),
    (u'de_sh', u'Schleswig-Holstein'),
    (u'de_th', u'Thüringen'),
])
AUTHORITIES_VOCABULARY = simplevoc_from_dict(AUTHORITIES)

@implementer(IVocabularyFactory)
class AuthorityVocabulary(object):
    """
    """

    def __call__(self, context=None):
        return AUTHORITIES_VOCABULARY


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

    def __call__(self, context=None):
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
            u'keine Angabe',
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
            (u'00000', u'ESN Sicherheit und Zertifizierung GmbH'),
            (u'00001', u'Ministerium für Wirtschaft, Innovation,  Digitalisierung und Energie des Landes NRW'),
            (u'01002', u'Ministerium für Energiewende, Landwirtschaft, Umwelt, Natur und Digitalisierung des Landes Schleswig-Holstein (SH)'),
            (u'01010', u'Landesmessstelle Schleswig-Holstein - LMst 2 Geesthacht'),
            (u'01011', u'Helmholtz-Zentrum Geesthacht'),
            (u'01020', u'Landesmessstelle Schleswig-Holstein - LMst 1 Kiel'),
            (u'01051', u'Kernkraftwerk Krümmel (KKK)'),
            (u'01071', u'Kernkraftwerk Brunsbüttel(KKB)'),
            (u'01081', u'Kernkraftwerk Brokdorf (KBR)'),
            (u'01181', u'SH-KTA-Brokdorf_SZL'),
            (u'01551', u'SH-KTA-Krümmel_SZL'),
            (u'03020', u'Universität Göttingen'),
            (u'03040', u'Landesmessstelle Niedersachsen - LMst 1 Hildesheim'),
            (u'03060', u'Landesmessstelle Niedersachsen - LMst 2 Hildesheim'),
            (u'03102', u'Landeszentrale Niedersachsen (NI)'),
            (u'03132', u'Niedersächsisches Ministerium für Umwelt, Energie, Bauen und Klimaschutz (MU)'),
            (u'03141', u'Kernkraftwerk Lingen GmbH'),
            (u'03151', u'PreussenElektra GmbH Kernkraftwerk Stade'),
            (u'03161', u'PreussenElektra GmbH Kernkraftwerk Unterweser '),
            (u'03171', u'PreussenElektra GmbH Gemeinschaftskernkraftwerk Grohnde'),
            (u'03191', u'Kernkraftwerke Lippe-Ems GmbH Kernkraftwerk Emsland'),
            (u'03201', u'BGZ Gesellschaft für Zwischenlagerung mbH Betrieb Gorleben'),
            (u'03211', u'Konrad Schacht II'),
            (u'03221', u'Advanced Nuclear Fuels GmbH'),
            (u'03231', u'NI-KTA-Lingen_SZL'),
            (u'03561', u'NI-KTA-Unterweser_SZL'),
            (u'03571', u'NI-KTA-Grohnde_SZL'),
            (u'04020', u'Landesmessstelle Bremen - LMst 1 Bremen'),
            (u'04032', u'Landeszentrale Bremen (BR)'),
            (u'05020', u'Landesmessstelle Nordrhein-Westfalen - LMst 1 Duisburg'),
            (u'05030', u'Landesmessstelle Nordrhein-Westfalen - LMst 2 Düsseldorf'),
            (u'05040', u'Ruhrverband Ruhrtalsperrverein'),
            (u'05050', u'TüV Rheinland - Köln'),
            (u'05060', u'Staatliches Veterinäruntersuchungsamt'),
            (u'05080', u'Landwirtschaftliche Untersuchungs- und Forschungsanstalt'),
            (u'05090', u'Materialprüfungsamt des Landes NRW'),
            (u'05091', u'Forschungszentrum Jülich (FZJ)'),
            (u'05092', u'Arbeitsgemeinschaft Versuchsreaktor GmbH (AVR)'),
            (u'05141', u'Kernkraftwerk Würgassen(KWW)'),
            (u'05151', u'Prototypenkraftwerk Hamm-Uentrop (THTR-300)'),
            (u'05161', u'SNR-Versuchskraftwerk Kalkar (SNR-300)'),
            (u'05171', u'BGZ Gesellschaft für Zwischenlagerung mbH Brennelement-Zwischenlager Ahaus GmbH'),
            (u'05181', u'Urananreicherungsanlage Gronau (UAG)'),
            (u'06060', u'Landesmessstelle Hessen - LMst 3 Darmstadt'),
            (u'06101', u'Kernkraftwerk Biblis'),
            (u'06122', u'Hessisches Ministerium für Umwelt, Klimaschutz, Landwirtschaft und Verbraucherschutz (HMUKLV)'),
            (u'06501', u'HE-KTA-Biblis_SZL'),
            (u'07002', u'Ministerium für Umwelt, Energie, Ernährung und Forsten Rheinland-Pfalz (RP) / Landeszentrale Rheinland-Pfalz (RP)'),
            (u'07010', u'Landesmessstelle Rheinland-Pfalz - LMst 1 Mainz'),
            (u'07020', u'Landesmessstelle Rheinland-Pfalz - LMst 4 Mainz'),
            (u'07030', u'Landesmessstelle Rheinland-Pfalz - LMst 2 Speyer'),
            (u'07040', u'Landesmessstelle Rheinland-Pfalz - LMst 5 Speyer'),
            (u'07071', u'Johannes Gutenberg Universität'),
            (u'07081', u'Anlage Mülheim-Kärlich (KMK)'),
            (u'08002', u'Ministerium für Umwelt,  Klima und Energiewirtschaft Baden-Württemberg (BW)'),
            (u'08010', u'Landesmessstelle Baden-Württemberg - LMst 1 Karlsruhe'),
            (u'08031', u'Universität Hohenheim'),
            (u'08041', u'Karlsruher Institut für Technologie - Campus Nord stellvertretend für alle Betreiber von Anlagen und Einrichtungen am Standort (Kerntechnische Entsorgung Karlsruhe GmbH, Europäische Kommission - Joint Research Centre Karlsruhe, Zyklotron AG)'),
            (u'08061', u'Staatliche milchwirtschaftliche Lehr- und Forschungsanstalt'),
            (u'08082', u'Landeszentrale Baden-Württemberg (BW)'),
            (u'08101', u'Kernkraftwerk Obrigheim'),
            (u'08111', u'EnBW Kernkraft GmbH Kernkraftwerk Neckarwestheim'),
            (u'08121', u'EnBW Kernkraft GmbH Kernkraftwerk Philippsburg'),
            (u'08131', u'Deutsches Krebsforschungszentrum Heidelberg'),
            (u'08201', u'Fachhochschule Ravensburg-Weingarten'),
            (u'08210', u'Landesfeuerwehrschule Baden-Württemberg'),
            (u'08221', u'Kerntechnische Hilfsdienst GmbH'),
            (u'08511', u'BW-KTA-Neckarwestheim_SZL'),
            (u'08521', u'BW-KTA-Philippsburg_SZL'),
            (u'09030', u'Landesmessstelle Bayern - LMst 3 Augsburg'),
            (u'09051', u'Helmholtz Zentrum München Deutsches Forschungszentrum für Gesundheit und Umwelt (GmbH)'),
            (u'09081', u'Landesgewerbeanstalt Bayern'),
            (u'09082', u'Bayerisches Geologisches Landesamt'),
            (u'09111', u'Technische Universität München'),
            (u'09121', u'Kernkraftwerk Isar1+2 GmbH'),
            (u'09122', u'Kernkraftwerk Isar 1 GmbH'),
            (u'09123', u'Bayernwerk AG'),
            (u'09131', u'Kernkraftwerk Grafenrheinfeld (KKG)'),
            (u'09141', u'Kernkraftwerk Gundremmingen (KRB)'),
            (u'09151', u'Versuchsatomkraftwerk Kahl GmbH (VAK)'),
            (u'09161', u'Siemens AG'),
            (u'09162', u'Framatome GmbH'),
            (u'09171', u'Siemens AG'),
            (u'09181', u'Siemens AG Brennelementewerk Hanau'),
            (u'09192', u'Landeszentrale Bayern (BY)'),
            (u'09231', u'Technischer Überwachungsverein e.V.'),
            (u'09300', u'Universitäten in Bayern'),
            (u'09521', u'BY-KTA-Isar_SZL'),
            (u'09531', u'BY-KTA-Grafenrheinfeld_SZL'),
            (u'09541', u'BY-KTA-Gundremmingen_SZL'),
            (u'10010', u'Landesmessstelle Saarland - LMst 1 Saarbrücken'),
            (u'10030', u'Landesmessstelle Saarland - LMst 1 Saarbrücken'),
            (u'10042', u'Landeszentrale Saarland (SL)'),
            (u'11010', u'Landesmessstelle Berlin - LMst 1 Berlin'),
            (u'11020', u'Freie Universität Berlin'),
            (u'11042', u'Senatsverwaltung für Umwelt, Verkehr und Klimaschutz (BE) / Landeszentrale Berlin (BE)'),
            (u'11061', u'Helmholtz-Zentrum Berlin für Materialien und Energie (BERII)'),
            (u'12010', u'Landesmessstelle Brandenburg - LMst 1 Oranienburg'),
            (u'12032', u'Landeszentrale Brandenburg (BB)'),
            (u'12041', u'Energiewerke Nord GmbH - Kernkraftwerk Rheinsberg'),
            (u'13002', u'Ministerium für Inneres und Europa Mecklenburg-Vorpommern (M-V)'),
            (u'13010', u'Landesmessstelle Mecklenburg-Vorpommern - Stralsund'),
            (u'13031', u'EWN Entsorgungswerk für Nuklearanlagen GmbH '),
            (u'13032', u'Landeszentrale Mecklenburg-Vorpommern (MV)'),
            (u'13033', u'Energiewerke Nord GmbH - Zwischenlager Nord'),
            (u'14002', u'Sächsisches Staatsministerium für Energie, Klimaschutz, Umwelt und Landwirtschaft (SMEKUL)'),
            (u'14010', u'Landesmessstelle Sachsen - LMst 1 Radebeul'),
            (u'14032', u'Landeszentrale Sachsen (SN)'),
            (u'14040', u'IAF-Radioökologie GmbH'),
            (u'14041', u'Forschungszentrum Rossendorf e.V'),
            (u'15010', u'Landesmessstelle Sachsen-Anhalt - LMst 1 Halle/Saale'),
            (u'18001', u'Endlager für radioaktive Abfälle Morsleben (ERAM)'),
            (u'18002', u'Bundesamt für Kerntechnische Entsorgungssicherheit Atomrechtliche Aufsicht'),
            (u'18003', u'KTA Asse'),
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
        items = [
            ('UCHL', u'KTA Leibstadt mit Beznau und Villigen'),
            ('UELA', u'Endlager für radioaktive Abfälle Asse'),
            ('UELM', u'Endlager für radioaktive Abfälle Morsleben (ERAM)'),
            ('UFRC', u'KKW Cattenom'),
            ('UFRF', u'KKW Fessenheim'),
            ('U01A', u'Helmholtz-Zentrum Geesthacht'),
            ('U01B', u'KKW Krümmel'),
            ('U01C', u'KKW Brunsbüttel'),
            ('U01D', u'KKW Brokdorf'),
            ('U01I', u'Interimslager Krümmel'),
            ('U01K', u'Standortzwischenlager Krümmel'),
            ('U01L', u'Standortzwischenlager Brunsbüttel'),
            ('U01M', u'Standortzwischenlager Brokdorf'),
            ('U03A', u'Standortzwischenlager Grohnde'),
            ('U03B', u'Brennelementefertigungsanl. Lingen'),
            ('U03C', u'Standortzwischenlager Unterweser'),
            ('U03E', u'KKW Emsland'),
            ('U03G', u'KKW Grohnde'),
            ('U03K', u'Endlager Konrad'),
            ('U03L', u'KKW Lingen'),
            ('U03P', u'BGZ - Betrieb Gorleben'),
            ('U03S', u'KKW Stade'),
            ('U03U', u'KKW Unterweser'),
            ('U03Z', u'Standortzwischenlager Lingen'),
            ('U05B', u'BGZ - Brennelement-Zwischenl. Ahaus'),
            ('U05F', u'Forschungszentrum Jülich'),
            ('U05G', u'AVR-Versuchskernkraftwerk Jülich'),
            ('U05K', u'KKW Würgassen'),
            ('U05T', u'Thorium-Hochtemp.reakt. Hamm-Uentrop'),
            ('U05U', u'Urananreicherungsanlage Gronau'),
            ('U06B', u'KKW Biblis und BE-Zwischenlager'),
            ('U07M', u'KKW Mülheim-Kärlich'),
            ('U07U', u'Uni Mainz'),
            ('U08H', u'DKFZ Heidelberg'),
            ('U08K', u'Karlsruher Institut für Technologie - Campus Nord (Einrichtungen am Standort)'),
            ('U08M', u'Abraumhalde Menz.'),
            ('U08N', u'EnKK Neckarwestheim'),
            ('U08O', u'EnKK Obrigheim'),
            ('U08P', u'EnKK Philippsburg'),
            ('U08W', u'KKW Wyhl'),
            ('U09A', u'KKW Isar 1+2'),
            ('U09B', u'KKW Isar1'),
            ('U09C', u'KKW Isar2'),
            ('U09D', u'KKW Grafenrheinfeld'),
            ('U09E', u'KKW Gundremmingen Block B/C'),
            ('U09F', u'Versuchs-AKW Kahl a.M.'),
            ('U09G', u'Forschungsreaktor München'),
            ('U09H', u'Siemens Brennelementewerk Hanau, Standort Karlstein'),
            ('U09I', u'Siemens AG, Karlstein'),
            ('U09J', u'Framatome GmbH, Forschungszentrum Erlangen-Süd (FZE)'),
            ('U09K', u'Forschungsneutronenquelle Heinz Maier-Leibnitz'),
            ('U11B', u'Experimentierreakt. II Berlin'),
            ('U12R', u'KKW Rheinsberg'),
            ('U13A', u'KKW Lubmin/Greifswald'),
            ('U13B', u'Zwischenlager Nord'),
            ('U14R', u'Forschungszentrum Rossendorf'),
            ('U15M', u'nicht benutzen, jetzt UELM, Endlager für radioaktive Abfälle Morsleben (ERAM)'),
        ]
        terms = [SimpleTerm(code, code, u'{} {}'.format(code, title))
                 for code, title in items]
        return SimpleVocabulary(terms)


NuclearInstallationVocabularyFactory = NuclearInstallationVocabulary()


allow_module("docpool.rei.vocabularies")
